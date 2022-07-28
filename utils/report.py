from .report_query import make_query
from .create_report import create_report
from .send_report import send_report
from .complex_charts import draw_treemap
from uuid import uuid4


def report_pipeline(email, cars_number):
    report_name = "Report" + str(uuid4())[:5] + ".docx"

    # make the query
    try:
        results = make_query(cars_number)
    except Exception as e:
        print(e)
        print("Couldn't make the query")

    # create the chart
    try:
        chart_name = draw_treemap(results)

    except Exception as e:
        print(e)
        print("Couldn't draw chart")

    # create the report
    try:
        report = create_report(username="Marko", cars=results, report_name=report_name)

    except Exception as e:
        print(e)
        print("Couldn't create report")

    # try:
    #     send_report(email, report_name)

    # except Exception as e:
    #     print(e)
