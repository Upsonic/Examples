# --- Simulated Inbox for Email Classification Agent ---

EMAILS = {
    1: ("Ministry of Finance - Audit Department", """
Dear Operations Team,

We are requesting detailed account statements for the last six months regarding the following customer.
Please include all transaction records, account balance history, and any associated documents.

This request is made in accordance with the Financial Supervision Act.
Sincerely,
Ministry of Finance - Audit Department
"""),

    2: ("Tax Collection Office", """
To Whom It May Concern,

Please be advised that a lien has been placed on the following bank account pursuant to the court order No. 2025/482.
All transactions from this account should be temporarily frozen until further notice.

Best regards,
Tax Collection Office
"""),

    3: ("Central Bank Compliance Division", """
Dear Compliance Officer,

We have received reports indicating potential irregular activity in one of your merchant accounts.
Please review and provide a suspicious activity report (SAR) within 48 hours.

Thank you,
Central Bank Compliance Division
"""),

    4: ("Financial Conduct Authority", """
Good afternoon,

This is a reminder that all partner institutions are required to submit quarterly audit summaries
under the revised Financial Transparency Act, effective immediately.

Please upload your institution’s Q3 statement package to the secure portal by November 15.

Regards,
Financial Conduct Authority
"""),

    5: ("National Fraud Investigation Unit", """
Attention Operations Team,

We are initiating a fraud investigation regarding recent unauthorized transactions.
Kindly confirm whether the following account remains active and provide all transaction logs
for the period of August 1 to September 15.

Sincerely,
National Fraud Investigation Unit
"""),

    6: ("Customer Service Department", """
Hi Team,

Please update the KYC records for customer ID #544329. The client has submitted a new proof of address document.
Once verified, kindly mark the profile as compliant.

Best,
Customer Service Department
"""),

    7: ("High Court Clerk’s Office", """
This notice serves to inform you that pursuant to case #2048/19, a temporary injunction
has been issued against the following business account. The account should not process outgoing
transactions until lifted by the court.

High Court Clerk’s Office
"""),

    8: ("Internal Revenue Service (IRS)", """
Dear Sir or Madam,

We request clarification on the reported interest income for the fiscal year 2024.
Please provide supporting account summaries and statement copies within 7 days.

Best regards,
IRS Compliance Division
"""),
}
