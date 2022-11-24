import re
import subprocess as sp

import dash
import dash_bootstrap_components as dbc
import dash_bootstrap_templates as dbt
from dash import Dash, dcc, html as dhtml
from setuptools_scm import get_version


dbt.load_figure_template("cosmo")

app = Dash(
    __name__,
    title="sphobjinv suggest",
    update_title="Searching...",
    external_stylesheets=[dbc.themes.COSMO],
)

GH_URL_TEMPLATE = "https://github.com/bskinn/soi-app/tree/{}"
VERSION = get_version(local_scheme="node-and-timestamp")

INPUT_URL = "input-url"
INPUT_SEARCH = "input-search"
INPUT_THRESHOLD = "input-threshold"

CHKLIST_INDEX_SCORE = "checklist-index-score"
INCLUDE_SCORE = "Include Score"
INCLUDE_INDEX = "Include Index"

BTN_SEARCH = "button-search"

RESULT_DISPLAY = "result-display"
SPAN_SPINNER = "span-spinner"


def get_source_link():
    """Construct the correct dhtml.A for the link into the source."""
    dirty = re.search("d[0-9]{8}", VERSION) is not None

    if "+g" in VERSION:
        ref_id = re.search("(?<=[+]g)[0-9a-f]+(?=($|[.d]))", VERSION)[0]
    else:
        ref_id = re.search("^.+(?=($|[+]d))", VERSION)[0]

    return dhtml.Span(
        [
            dhtml.A(ref_id, href=GH_URL_TEMPLATE.format(ref_id)),
            " (modified)" if dirty else "",
        ]
    )


app.layout = dhtml.Div(
    [
        dhtml.Div(
            [
                dhtml.H1(
                    [
                        dhtml.Img(src="assets/images/soi-logo.png"),
                        dhtml.Code("sphobjinv suggest"),
                        " as a Service",
                        dhtml.Img(src="assets/images/soi-logo.png"),
                    ]
                ),
            ]
        ),
        dhtml.H2(
            [
                "Bringing the ",
                dhtml.Code("sphobjinv suggest"),
                " CLI to the the browser",
            ]
        ),
        dhtml.Div(
            "Paste any URL from a Sphinx docset, enter the desired search term, "
            "select your options, and go!"
        ),
        dhtml.Br(),
        dhtml.Div(
            [
                dhtml.Span(className="input-label", children="URL:"),
                dcc.Input(type="url", size="80", id=INPUT_URL),
            ]
        ),
        dhtml.Div(
            [
                dhtml.Span(className="input-label", children="Search Term:"),
                dcc.Input(type="text", size="45", id=INPUT_SEARCH),
            ]
        ),
        dhtml.Div(
            dcc.Checklist(
                id=CHKLIST_INDEX_SCORE,
                options=[INCLUDE_SCORE, INCLUDE_INDEX],
                value=[INCLUDE_SCORE],
                inline=True,
                labelClassName="input-label",
            )
        ),
        dhtml.Div(
            [
                dcc.Input(
                    type="number",
                    size="2",
                    id=INPUT_THRESHOLD,
                    required=True,
                    debounce=True,
                    value=75,
                    min=0,
                    max=100,
                ),
                dhtml.Span(className="input-label", children="Score Threshold"),
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
            children="```\nLoading...\n```",
            id=RESULT_DISPLAY,
            className="sphobjinv-output",
        ),
        dhtml.Div(
            className="footer",
            children=[
                dhtml.Div(
                    [
                        (
                            "© Copyright 2022 Brian Skinn. "
                            "Site content is licensed under "
                        ),
                        dhtml.A(
                            "CC BY 4.0",
                            href="http://creativecommons.org/licenses/by/4.0/",
                        ),
                        ".",
                    ]
                ),
                dhtml.Div(
                    [
                        f"Version {VERSION}, source at ",
                        get_source_link(),
                    ]
                ),
            ],
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
    dash.State(INPUT_THRESHOLD, "value"),
    dash.State(CHKLIST_INDEX_SCORE, "value"),
)
def run_suggest(
    n_clicks,
    n_submit_url,
    n_submit_search,
    url_value,
    search_value,
    threshold_value,
    chklist_values,
):
    option_str = "-ua"

    if INCLUDE_SCORE in chklist_values:
        option_str += "s"

    if INCLUDE_INDEX in chklist_values:
        option_str += "i"

    option_str += f"t{threshold_value}"

    result = sp.run(
        [
            "sphobjinv",
            "suggest",
            option_str,
            str(url_value),
            str(search_value),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode > 1:
        return ("It errored", " ")

    if url_value and search_value:
        return (f"```none\n{result.stderr}\n{result.stdout}\n```", " ")
    else:
        return ("```none\n(Enter search values)\n```", " ")


if __name__ == "__main__":
    app.run_server(debug=True)
