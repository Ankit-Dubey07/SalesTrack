/**
 * SalesTrack enquiry form handler (Google Apps Script web app)
 *
 * What it does, for each valid enquiry posted from salestrack.co.in:
 *   1. Saves the enquiry as a new row in the "Enquiries" tab of the SalesTrack Google Sheet
 *   2. Sends a thank-you email to the customer
 *   3. Sends a notification email to info@salestrack.co.in with the full details
 *   4. Returns { ok: true } so the website can show a confirmation message
 *
 * Setup: see apps-script/SETUP.md. Written for SalesTrack; no third-party code.
 */

// ---------------------------------------------------------------- settings
var SHEET_ID = '1HDdBLWH6CuXfXcMysnxecfts74y-0jqQYubXtJnUy70';
var SHEET_TAB = 'Enquiries';
var BUSINESS_EMAIL = 'info@salestrack.co.in';
var BUSINESS_NAME = 'SalesTrack';
var WEBSITE = 'https://salestrack.co.in';
var NOTICE_VERSION = 'Privacy Notice version 3, 13 November 2026';
var SERVICES = {
  'lead-generation': 'Lead Generation',
  'b2c-sales': 'B2C Sales Solutions',
  'live-transfer': 'Live Transfer Solutions',
  'bpo': 'BPO Services',
  'not-sure': 'Not sure yet'
};
var HEADERS = ['Received (IST)', 'Name', 'Email', 'Phone', 'Company', 'Service', 'Message',
               'Consent', 'Marketing opt-in', 'Page', 'Reference'];

// ---------------------------------------------------------------- validation (mirrors the website's rules)
var URL_RE = /(https?:\/\/|ftp:\/\/|www\.|\b[a-z0-9-]+(\.[a-z0-9-]+)*\.(com|net|org|in|co|io|ai|uk|us|info|biz|xyz|online|site|store|shop|app|dev|me|ly|tv|gg|link|click|top|club|live|pro|tech|cloud|digital|agency|blog|website|space|today)\b)/i;

function clean_(v) { return String(v == null ? '' : v).replace(/\s+/g, ' ').trim(); }

function validate_(p) {
  var errors = {};
  var name = clean_(p.name), email = String(p.email || '').trim(), phone = String(p.phone || '').trim();
  var company = clean_(p.company), service = String(p.service || ''), message = String(p.message || '').trim();

  if (!/^[A-Za-z]+(?: [A-Za-z]+)*$/.test(name) || name.replace(/ /g, '').length < 2) errors.name = 'Invalid name';
  if (email.length > 100 || /\.\./.test(email) ||
      !/^[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9_%+-])?@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,24}$/.test(email)) errors.email = 'Invalid email';
  var digits = phone.replace(/\D/g, '');
  if (!/^\+?[0-9\s\-()]+$/.test(phone) || (phone.match(/\+/g) || []).length > 1 ||
      digits.length < 10 || digits.length > 15 || /^(\d)\1+$/.test(digits)) errors.phone = 'Invalid phone';
  if (company.length < 2 || company.length > 100 || !/^[A-Za-z0-9][A-Za-z0-9 &.,'()\/-]*$/.test(company) ||
      !/[A-Za-z]/.test(company) || URL_RE.test(company)) errors.company = 'Invalid company';
  if (!SERVICES.hasOwnProperty(service)) errors.service = 'Invalid service';
  if (message.length < 15 || message.length > 2000 || URL_RE.test(message)) errors.message = 'Invalid message';
  if (p.consent !== 'yes') errors.consent = 'Consent required';

  return {
    ok: Object.keys(errors).length === 0, errors: errors,
    data: { name: name, email: email, phone: phone, company: company, service: SERVICES[service] || service,
            message: message, marketing: p.marketing === 'yes', page: clean_(p.page).slice(0, 200) }
  };
}

// ---------------------------------------------------------------- web app entry points
function doPost(e) {
  var p = (e && e.parameter) || {};
  try {
    // Spam trap: real visitors never fill the hidden "website" field.
    if (p.website) return json_({ ok: true });

    var v = validate_(p);
    if (!v.ok) return json_({ ok: false, error: 'validation', fields: Object.keys(v.errors) });
    var d = v.data;

    // Rate limit: one enquiry per email address every 2 minutes, and at most 20 per hour overall.
    var cache = CacheService.getScriptCache();
    var key = 'e:' + Utilities.base64EncodeWebSafe(d.email.toLowerCase());
    if (cache.get(key)) return json_({ ok: false, error: 'too_soon' });
    var count = Number(cache.get('hour') || 0);
    if (count >= 20) return json_({ ok: false, error: 'busy' });

    var lock = LockService.getScriptLock();
    lock.waitLock(20000);
    var ref, received;
    try {
      var sheet = getSheet_();
      received = Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyyy-MM-dd HH:mm:ss');
      ref = 'ST-' + Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyMMdd') + '-' + (sheet.getLastRow()).toString().padStart(4, '0');
      sheet.appendRow([received, d.name, d.email, "'" + d.phone, d.company, d.service, d.message,
                       'Yes (' + NOTICE_VERSION + ')', d.marketing ? 'Yes' : 'No', d.page, ref]);
    } finally {
      lock.releaseLock();
    }
    cache.put(key, '1', 120);
    cache.put('hour', String(count + 1), 3600);

    sendNotification_(d, ref, received);
    sendThankYou_(d, ref);
    return json_({ ok: true, ref: ref });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'server' });
  }
}

function doGet() {
  return json_({ ok: true, service: 'SalesTrack enquiry form' });
}

// ---------------------------------------------------------------- helpers
function getSheet_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(SHEET_TAB) || ss.insertSheet(SHEET_TAB);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function esc_(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/** Sends an email as "SalesTrack" from the Google account that deployed this script,
 *  with replies going to info@salestrack.co.in (or to the customer, for notifications).
 *  To send from the info@salestrack.co.in address itself, see "Sending from info@" in SETUP.md. */
function send_(to, subject, text, html, replyTo) {
  MailApp.sendEmail(to, subject, text, { name: BUSINESS_NAME, htmlBody: html, replyTo: replyTo || BUSINESS_EMAIL });
}

function sendNotification_(d, ref, received) {
  var rows = [['Reference', ref], ['Received (IST)', received], ['Name', d.name], ['Email', d.email],
              ['Phone', d.phone], ['Company', d.company], ['Service', d.service],
              ['Marketing opt-in', d.marketing ? 'Yes' : 'No'], ['Consent', 'Yes (' + NOTICE_VERSION + ')'], ['Page', d.page]];
  var text = 'New website enquiry\n\n' + rows.map(function (r) { return r[0] + ': ' + r[1]; }).join('\n') +
             '\n\nMessage:\n' + d.message + '\n\nReply to this email to answer the customer directly.';
  var html = '<div style="font-family:Arial,sans-serif;font-size:14px;color:#0e2559">' +
    '<h2 style="margin:0 0 12px">New website enquiry</h2><table cellpadding="6" style="border-collapse:collapse">' +
    rows.map(function (r) { return '<tr><td style="color:#4c5a78">' + esc_(r[0]) + '</td><td><b>' + esc_(r[1]) + '</b></td></tr>'; }).join('') +
    '</table><p style="margin:16px 0 4px;color:#4c5a78">Message</p><p style="white-space:pre-wrap;margin:0">' + esc_(d.message) + '</p>' +
    '<p style="margin-top:16px;color:#4c5a78">Reply to this email to answer the customer directly.</p></div>';
  send_(BUSINESS_EMAIL, 'New enquiry: ' + d.service + ' from ' + d.name + ' (' + d.company + ') [' + ref + ']', text, html, d.email);
}

function sendThankYou_(d, ref) {
  // Deliberately does not repeat the visitor's message, so the form can't be used to send other people's text.
  var text = 'Hi ' + d.name + ',\n\n' +
    'Thank you for contacting SalesTrack about ' + d.service + '. We have received your enquiry (reference ' + ref + ').\n\n' +
    'Our team will reply during our working hours: Monday to Friday, 2:30 PM to 11:00 PM IST.\n\n' +
    'If you did not send this enquiry, or you would like us to delete your details, reply to this email with the subject "Privacy request".\n\n' +
    'Regards,\nSalesTrack\nLead. Connect. Grow.\n' + WEBSITE;
  var html = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.6;color:#0e2559;max-width:560px">' +
    '<p>Hi ' + esc_(d.name) + ',</p>' +
    '<p>Thank you for contacting <b>SalesTrack</b> about <b>' + esc_(d.service) + '</b>. We have received your enquiry (reference <b>' + esc_(ref) + '</b>).</p>' +
    '<p>Our team will reply during our working hours: <b>Monday to Friday, 2:30 PM to 11:00 PM IST</b>.</p>' +
    '<p style="color:#4c5a78;font-size:13px">If you did not send this enquiry, or you would like us to delete your details, reply to this email with the subject "Privacy request". ' +
    'See our <a href="' + WEBSITE + '/privacy.html">Privacy Notice</a>.</p>' +
    '<p>Regards,<br><b>SalesTrack</b><br><span style="color:#27b217">Lead. Connect. Grow.</span><br><a href="' + WEBSITE + '">salestrack.co.in</a></p></div>';
  send_(d.email, 'Thank you for contacting SalesTrack [' + ref + ']', text, html, BUSINESS_EMAIL);
}

/** Run once from the Apps Script editor to create the header row and approve permissions. */
function setup() {
  getSheet_();
  Logger.log('Sheet ready. Emails left today: ' + MailApp.getRemainingDailyQuota());
}
