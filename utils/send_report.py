# send report by email
from pathlib import Path
from decouple import config

import sendgrid
from sendgrid.helpers.mail import *

import base64

from .renderEmail import render_template


# from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

SENDGRID_ID = config("SENDGRID_ID", cast=str)


def send_report(email, HTMLcontent):

    fromTpl = render_template(title="Car Report for DATE", body=HTMLcontent)
    print("FROM TPL:", fromTpl)
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_ID)
    from_email = Email("FARM@freethrow.rs")
    to_email = To(email)
    subject = "FARM Cars daily report"
    content = Content(
        "text/plain", "this is dynamic text, potentially coming from our database"
    )
    # html_content = fromTpl
    mail = Mail(from_email, to_email, subject, content, html_content=fromTpl)

    cwd = Path.cwd()

    filepath = Path.joinpath(cwd, "utils", "charts", "tree.html")
    print("Email path:", filepath)

    try:

        with open(filepath, "rb") as f:
            data = f.read()
            f.close()
            encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName("ReportMap.html"),
            FileType("text/html"),
            Disposition("attachment"),
        )
        mail.attachment = attachedFile
    except Exception as e:
        print(e)
        print("Could not attach report")

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response)
        print("Sending email")
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e)
        print("Could not send email")
