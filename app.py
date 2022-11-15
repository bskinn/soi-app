import itertools as itt
import subprocess as sp

import dash
import dash_bootstrap_components as dbc
import dash_bootstrap_templates as dbt

# import sphobjinv as soi
from dash import Dash, dcc, html as dhtml

dbt.load_figure_template("cosmo")

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

INPUT_URL = "input-url"
INPUT_SEARCH = "input-search"

BTN_SEARCH = "button-search"

RESULT_DISPLAY = "result-display"
SPAN_SPINNER = "span-spinner"


app.layout = dhtml.Div(
    [
        dhtml.Div(
            [
                dhtml.Span("URL"),
                dcc.Input(type="url", size="80", id=INPUT_URL),
            ]
        ),
        dhtml.Div(
            [
                dhtml.Span("Search Term"),
                dcc.Input(type="text", size="45", id=INPUT_SEARCH),
            ]
        ),
        dhtml.Div(
            [
                dhtml.Button("Search", id=BTN_SEARCH),
                dcc.Loading(
                    type="circle", children=dhtml.Span(id=SPAN_SPINNER, children=" ")
                ),
            ],
        ),
        dcc.Markdown(
            "```\nLoading...\n```",
            id=RESULT_DISPLAY,
            style={
                "font-family": "monospace",
                "font-size": "smaller",
                "margin-top": "20px",
            },
        ),
    ],
)


@app.callback(
    dash.Output(RESULT_DISPLAY, "children"),
    dash.Output(SPAN_SPINNER, "children"),
    dash.Input(BTN_SEARCH, "n_clicks"),
    dash.Input(INPUT_URL, "n_submit"),
    dash.Input(INPUT_SEARCH, "n_submit"),
    dash.State(INPUT_URL, "value"),
    dash.State(INPUT_SEARCH, "value"),
)
def run_suggest(n_clicks, n_submit_url, n_submit_search, url_value, search_value):
    result = sp.run(
        ["sphobjinv", "suggest", "-uas", str(url_value), str(search_value)],
        capture_output=True,
        text=True,
    )

    if result.returncode > 1:
        return ("It errored", " ")

    if url_value and search_value:
        return (f"```none\n{result.stderr}\n{result.stdout}\n```", " ")
    else:
        return (f"```none\nEnter search values\n```", " ")


if __name__ == "__main__":
    app.run_server(debug=True)
