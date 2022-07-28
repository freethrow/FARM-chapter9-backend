# function to create a report in docx

from os.path import exists
from os import scandir, remove

from pathlib import Path

from docxtpl import DocxTemplate, InlineImage


def create_report(username, cars, report_name):

    # delete all files in /reports
    cwd = Path.cwd()
    reports_dir = Path.joinpath(cwd, "utils", "reports")

    # for file in scandir(reports_dir):
    #     remove(file.path)

    # create a document object
    doc = DocxTemplate("ReportTemplate.docx")

    # create the context:
    context = {
        "username": username,
        "cars": cars,
        "num_car": len(cars),
        "chart": InlineImage(doc, "./utils/charts/latest.png"),
    }

    # render context into the document object
    doc.render(context)

    # save the document object as a word file
    filepath = Path.joinpath(cwd, "utils", "reports", report_name)
    doc.save(filepath)

    if exists(filepath):
        print(report_name, " exists! Proceed to send.")
        return True
