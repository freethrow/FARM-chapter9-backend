# function to render a jinja template into html

import os
import jinja2


def render_template(title, body):
    """renders a Jinja template into HTML"""
    # check if template exists

    templateLoader = jinja2.FileSystemLoader(searchpath="./utils")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template("template.html")
    return templ.render(title=title, body=body)
