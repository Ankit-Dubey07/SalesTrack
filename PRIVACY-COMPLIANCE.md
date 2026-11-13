# SalesTrack website: DPDP compliance review

Reviewed: 13 November 2026
Scope: salestrack.co.in (all pages, form, scripts and hosting setup)
Laws considered: Digital Personal Data Protection Act, 2023 (DPDP Act) and the Digital Personal Data Protection Rules, 2025 (notified 14 November 2025).

This is a technical review, not legal advice. It does not certify compliance. The items in section 5 need review by a qualified legal adviser.

**Timing.** The Rules were notified on 14 November 2025 and apply in phases. Most obligations on businesses (notice, security, breach reporting, retention, rights handling) take effect **18 months after notification, around May 2027**. Adopting them now prepares the site early.

## 1. Where the website handles personal data

| Point | Personal data | Where it goes | Stored on website? |
|---|---|---|---|
| Contact form (contact.html) | Name, email, phone, company, service of interest, message (all required); optional marketing choice; consent record | Opens the visitor's own email app; sent to info@salestrack.co.in (GoDaddy email) | No |
| Email links (all pages) | Whatever the visitor writes | info@salestrack.co.in (GoDaddy email) | No |
| Website hosting | IP address and basic connection data | GitHub Pages server logs, under GitHub's terms | No (held by GitHub) |
| Cookies, analytics, trackers, browser storage | None | n/a | n/a |
| Outside content (fonts, scripts, embeds) | None: fonts are self-hosted, and there are no third-party scripts | n/a | n/a |

## 2. Gaps found and fixes made

| # | Requirement (DPDP Act / Rules) | Gap before | Fix made |
|---|---|---|---|
| 1 | Notice at or before consent, itemising data and purpose (s.5; Rule 3) | The form had only a tick box linking to the policy | Added a short **"How we use your details"** notice above the consent box: purpose, where data goes, how to withdraw, and a link to the full notice |
| 2 | Consent must be specific, informed and given by a clear affirmative act (s.6(1)) | One combined tick box | Required consent box now names the purpose. **Marketing has its own optional box, never pre-ticked** |
| 3 | Fiduciary must be able to prove consent (s.6(10)) | No record | The enquiry email now includes the consent text, notice version, marketing choice and a timestamp |
| 4 | Withdrawing consent must be as easy as giving it (s.6(4)) | Not stated clearly | Notice and policy explain withdrawal by email. A pre-filled "Privacy request" email link is provided |
| 5 | Notice must explain rights and how to complain to the Data Protection Board (s.5(1)) | GDPR-style rights only | Policy now lists DPDP rights: access summary (s.11), correction and erasure (s.12), withdrawal, grievance redressal (s.13), nomination (s.14), and complaint to the Board |
| 6 | Publish a contact for data protection questions (s.8(9); Rule 9) | General email only | Policy names the contact route: info@salestrack.co.in, subject "Privacy request". **Legal review: designate a named person** (section 5) |
| 7 | Respond to rights requests in time (Rules; 90 days per the PIB explainer) | No commitment | Policy commits to responding within 90 days |
| 8 | Erase data when the purpose is served or consent is withdrawn (s.8(7)) | Vague | Policy has a retention table per data type and an erasure statement |
| 9 | Security safeguards and breach intimation (s.8(5)–(6); Rules 6–7) | Not covered | Policy states HTTPS-only, reasonable safeguards, and breach notification to individuals and the Board |
| 10 | Notice in English or an Eighth Schedule language (s.5(3)) | Not addressed | Policy offers other languages on request. **Legal review: whether a translated version is needed** |
| 11 | Children's data (s.9; Rule 10) | Brief mention | Policy states the site is not for under-18s, and that a child's data received without verifiable parental consent will be deleted |
| 12 | Cookies and trackers | None used | Confirmed. Policy says so explicitly |

Website design and functionality are unchanged. The form works as before, with the notice and one optional checkbox added.

## 3. What the business must do (outside the website)

These can't be fixed in code. They depend on how SalesTrack works day to day.

- [ ] Secure the info@salestrack.co.in mailbox: strong password, two-step verification, and access only for staff who handle enquiries.
- [ ] Set a retention rule and follow it, for example by deleting enquiry emails that didn't lead to work after a fixed period. Then tell me the period so the policy can state it.
- [ ] Keep marketing opt-ins separate, and send updates only to people who ticked the box. Honour unsubscribes promptly.
- [ ] Keep a simple log of privacy requests: date received, what was asked, date answered.
- [ ] Prepare a breach plan: who decides, how affected people and the Data Protection Board are told, and within what time.
- [ ] Check the GoDaddy and GitHub terms for data processing and for storage outside India.
- [ ] Bring client and lead data handled in your sales and BPO work (calling lists, CRM data) under the same rules. That data is outside this website and was not reviewed.

## 4. Third parties

| Provider | Role | Data | Notes |
|---|---|---|---|
| GoDaddy | Business email hosting (processes for SalesTrack) | Enquiry emails | Check data processing terms and server locations |
| GitHub (Microsoft) | Website hosting | IP and connection logs | Processes under its own privacy terms; may be outside India |
| Visitor's email provider | Sends the enquiry | The visitor's own email | Chosen by the visitor; outside SalesTrack's control |

## 5. Items requiring legal review

1. Whether SalesTrack must designate a named person as the published data protection contact (Rule 9), rather than a role email.
2. The legal basis for GitHub's server logs, and whether GitHub acts as SalesTrack's processor or as its own Data Fiduciary for that data.
3. Whether any Third Schedule retention class or the 48-hour pre-erasure intimation (Rule 8) applies to SalesTrack. These generally target large platforms.
4. Whether a translated notice is needed for SalesTrack's audience (s.5(3)).
5. The 90-day response commitment and the identity-verification step for rights requests.
6. Cross-border transfer: confirm no provider stores data in a country restricted under s.16.
7. Whether the consent-record approach (consent text and timestamp in the email) is sufficient evidence under s.6(10).
8. How the DPDP Act applies to SalesTrack's core work: lead generation, calling and live transfers to third-party data principals. This is the largest compliance area, and it is outside the website.
9. Data minimisation (s.6(1), s.8): phone and company became **required** on 13 November 2026 at the owner's request. Confirm that both are needed to handle an enquiry.
10. The wording of the Privacy Notice as a whole, and its interaction with UK GDPR and EU GDPR for overseas clients.

## Sources

- [DPDP Rules, 2025: key highlights (SCC Online, 26 Dec 2025)](https://www.scconline.com/blog/post/2025/12/26/digital-personal-data-protection-rules-2025-key-highlights/)
- [PIB explainer on the DPDP Rules, 2025 (Nov 2025)](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf)

## Change log

- **13 Nov 2026:** All enquiry fields made required, except the optional marketing box, which must stay optional. Validation added: names letters and spaces only; strict email format; phone 10–15 digits with optional +; company letters, numbers and basic punctuation; website links blocked in every field. The Privacy Notice table was updated to match.
