/**
 * Excel Pest — website lead capture.
 *
 * Appends every estimate-form submission from the website to a Google Sheet the
 * business owns, so a lead is never lost even if email delivery has an error.
 *
 * SETUP (one time, ~3 min):
 *  1. Create a Google Sheet (e.g. "Excel Pest — Website Leads").
 *  2. Extensions → Apps Script. Delete the sample, paste this whole file, Save.
 *  3. Deploy → New deployment → type "Web app".
 *       - Description: lead capture
 *       - Execute as: Me
 *       - Who has access: Anyone
 *     Deploy, authorize when prompted, and COPY the Web app URL (ends in /exec).
 *  4. Send that /exec URL back and it gets wired into the site
 *     (LEAD_SHEET_ENDPOINT in tools/build.py).
 *
 * The site already emails office@ via FormSubmit, so leave NOTIFY_EMAIL blank to
 * avoid duplicate emails — the Sheet is the durable backup record. If you'd rather
 * this script ALSO email (and drop FormSubmit entirely), set NOTIFY_EMAIL below.
 */

var NOTIFY_EMAIL = "";  // e.g. "office@excelpest-lawncontrol.com" to also email; "" = Sheet only

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("Leads") || ss.insertSheet("Leads");
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["Timestamp", "Name", "Email", "Phone", "Zip",
                       "Help with", "Message", "Page"]);
      sheet.setFrozenRows(1);
    }
    var p = (e && e.parameter) ? e.parameter : {};
    var row = [
      p._ts || new Date().toISOString(),
      p.name || "", p.email || "", p.phone || "",
      p.zip || p.city || "", p.service || "", p.message || "", p._page || ""
    ];
    sheet.appendRow(row);

    if (NOTIFY_EMAIL) {
      MailApp.sendEmail(NOTIFY_EMAIL,
        "New estimate lead — " + (p.name || "website"),
        "A new request came in from the website:\n\n" +
        "Name: " + (p.name || "") + "\n" +
        "Email: " + (p.email || "") + "\n" +
        "Phone: " + (p.phone || "") + "\n" +
        "Zip: " + (p.zip || p.city || "") + "\n" +
        "Help with: " + (p.service || "") + "\n" +
        "Message: " + (p.message || "") + "\n\n" +
        "Logged: " + row[0]);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    // Still return 200 so the site's fire-and-forget call never surfaces an error.
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    try { lock.releaseLock(); } catch (e2) {}
  }
}

// Lets you open the /exec URL in a browser to confirm it's deployed.
function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true, service: "Excel Pest lead capture" }))
    .setMimeType(ContentService.MimeType.JSON);
}
