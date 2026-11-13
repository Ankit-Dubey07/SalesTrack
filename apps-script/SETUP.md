# Connecting the enquiry form to Google Sheets and email

When this is set up, every valid enquiry from salestrack.co.in:

1. is saved as a new row in the **Enquiries** tab of the SalesTrack Google Sheet;
2. triggers a **thank-you email** to the customer;
3. triggers a **notification email** to info@salestrack.co.in with all the details. Press Reply to answer the customer directly;
4. shows the customer a **confirmation message** on the website, with a reference number (for example ST-261113-0001).

Until it's set up, the form keeps working as before: it opens the visitor's email app.

## Step 1: Add the script to the Sheet (about 5 minutes)

Sign in to the Google account that **owns** the SalesTrack Google Sheet, then:

1. Open the Sheet and go to **Extensions → Apps Script**.
2. Delete the sample code, paste in the whole of `apps-script/Code.gs`, and click **Save**. Name the project **SalesTrack Enquiries**.
3. In the function menu at the top, choose **setup** and click **Run**.
4. Google asks for permission. Click **Review permissions** and choose the account.
5. You'll see "Google hasn't verified this app". This is normal for a script you wrote yourself. Click **Advanced**, then **Go to SalesTrack Enquiries**, then **Allow**.
   - The script asks for two permissions: **see and edit this spreadsheet**, and **send email as you**. It can't read your inbox.
6. An **Enquiries** tab with a header row appears in the Sheet.

## Step 2: Publish it as a web app

1. Click **Deploy → New deployment**.
2. Click the gear icon next to "Select type" and choose **Web app**.
3. Fill in the settings:
   - **Description:** SalesTrack enquiry form
   - **Execute as:** Me
   - **Who has access:** Anyone. This lets the website send enquiries to it; nobody gets access to the Sheet.
4. Click **Deploy** and copy the **Web app URL**. It ends in `/exec`.
5. Send that URL to the developer. It goes into `FORM_ENDPOINT` in `build.py`, and the site is rebuilt and pushed.

After that, submit one test enquiry using your own email address and check that you get:
- a new row in the Sheet;
- the thank-you email;
- the notification at info@salestrack.co.in.

## Sending from info@salestrack.co.in

By default the emails are sent by the Google account that deployed the script. They show the sender name **SalesTrack**, and replies go to **info@salestrack.co.in**.

info@salestrack.co.in is a GoDaddy mailbox, so Google can only send as that exact address if one of these is set up:

- **Option A: Gmail "Send mail as".** In the Gmail account that owns the script, go to **Settings → Accounts → Send mail as → Add another email address**. Add info@salestrack.co.in using the outgoing (SMTP) server details from your GoDaddy email account, and confirm the verification email. Then ask the developer to switch `send_()` in Code.gs to `GmailApp` with `from: info@salestrack.co.in`. Google will then ask for wider Gmail permissions.
- **Option B: Google Workspace.** Move salestrack.co.in email to Google Workspace. This is a paid plan and needs DNS changes.

## Things to know

- **Daily email limit.** Google limits how many emails a script can send per day, and each enquiry sends two. A free Gmail account allows far fewer than Google Workspace. Check Google's current Apps Script quotas if you expect many enquiries.
- **Spam protection:**
  - The script checks every field again, using the same rules as the website.
  - It ignores entries from spam bots, which fill a hidden field that people never see.
  - It accepts one enquiry per email address every 2 minutes, and at most 20 per hour.
  - The thank-you email never repeats the visitor's message, so the form can't be used to send messages to strangers.
- **Changing the script later.** After editing, go to **Deploy → Manage deployments**, edit the existing deployment, and choose **New version**. Don't create a new deployment, or the URL will change.
- **Privacy.** The Privacy Notice switches automatically to version 3 once `FORM_ENDPOINT` is set. Version 3 names Google as the place enquiry records are kept. Delete enquiry rows when they're no longer needed (see PRIVACY-COMPLIANCE.md).
