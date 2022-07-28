# send report by email
from pathlib import Path
from decouple import config

import sendgrid
from sendgrid.helpers.mail import *

import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

SENDGRID_ID = config("SENDGRID_ID", cast=str)


def send_report(email, file_name):

    print("Starting mail with:", email, file_name)
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_ID)
    from_email = Email("FARM@freethrow.rs")
    to_email = To(email)
    subject = "FARM Cars daily report"
    content = Content(
        "text/plain", "this is dynamic text, potentially coming from our database"
    )
    mail = Mail(from_email, to_email, subject, content)

    cwd = Path.cwd()

    filepath = Path.joinpath(cwd, "utils", "reports", file_name)
    print("Email path:", filepath)

    try:

        with open(filepath, "rb") as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(file_name),
            FileType("application/docx"),
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
