from .report_query import make_query

from .send_report import send_report
from .complex_charts import draw_treemap
from uuid import uuid4


def report_pipeline(email, cars_number):

    # make the query - get the data and some HTML
    try:
        query_data = make_query(cars_number)
    except Exception as e:
        print(e)
        print("Couldn't make the query")

    # create the chart
    try:
        chart_html = draw_treemap(query_data["results"])

    except Exception as e:
        print(e)
        print("Couldn't draw chart")

    try:
        send_report(email=email, HTMLcontent=query_data["HTML"])

    except Exception as e:
        print(e)
