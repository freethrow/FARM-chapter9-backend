import plotly.express as px
import pandas as pd
import numpy as np

from pathlib import Path


# draw treemap and save it
def draw_treemap(data, filename="tree.html"):

    cwd = Path.cwd()

    df = pd.DataFrame(data)
    print(df.head())
    df["avg_price"] = df.groupby(["brand", "make"])["price"].transform("mean")
    df["avg_km"] = df.groupby(["brand", "make"])["km"].transform("mean")
    df["count"] = 1

    print("Drawing treemap...")

    fig = px.treemap(
        df,
        path=[px.Constant("All cars"), "brand", "make"],
        values="count",
        color="avg_price",
        hover_data=["avg_km"],
        color_continuous_scale="RdBu_r",
    )

    fig.update_layout(margin=dict(t=2, l=2, r=2, b=2))
    try:
        image_path = Path.joinpath(cwd, "utils", "charts", filename)
        # fig.write_image(image_path)
        fig.write_html(image_path)
        print("Written image file ", filename)
    except Exception as e:
        print(e)

    return filename
