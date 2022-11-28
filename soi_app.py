r"""`soi-app` *app definition module*.

`soi-app` is a Dash app encapsulating the 'suggest' functionality
of `sphobjinv` (https://sphobjinv.readthedocs.io/en/stable/cli/suggest.html)

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    14 Nov 2022

**Copyright**
    \(c) Brian Skinn 2022

**Source Repository**
    https://github.com/bskinn/soi-app

**License**
    Content: CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/)

    Code: MIT License

    See LICENSE.txt for full license terms.

"""


import datetime
import re
import subprocess as sp
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import dash_bootstrap_templates as dbt
import sphobjinv as soi
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
VERSION = get_version(local_scheme="node-and-timestamp", version_scheme="post-release")

INPUT_URL = "input-url"
INPUT_SEARCH = "input-search"
INPUT_THRESHOLD = "input-threshold"

CHKLIST_INDEX_SCORE = "checklist-index-score"
CHKBX_INCLUDE_SCORE = "Include Score"
CHKBX_INCLUDE_INDEX = "Include Index"

BTN_SEARCH = "button-search"

DIV_RESULT_DISPLAY = "div-result-display"
SPAN_SPINNER = "span-spinner"

COPYRIGHT_YEARS = (
    "2022" if (YEAR := datetime.datetime.now().year) == 2022 else f"2022-{YEAR}"
)


def get_soi_executable():
    """Return a Path to whichever sphobjinv executable is available.

    env/bin/sphobjinv for POSIX
    env/Scripts/sphobjinv.exe for Windows

    """
    soi_path = Path("env", "bin", "sphobjinv")

    if soi_path.exists():
        return soi_path
    else:
        return Path("env", "Scripts", "sphobjinv.exe")


SOI_EXECUTABLE = get_soi_executable()


def get_source_link():
    """Construct the correct dhtml.A for the link into the source."""
    dirty = re.search("d[0-9]{8}", VERSION) is not None
    at_tag = re.search(r"[.]post", VERSION) is None

    if at_tag:
        ref_id = "v" + re.search("^.+(?=($|[+]d))", VERSION)[0]
    else:
        ref_id = re.search("(?<=[+]g)[0-9a-f]+(?=($|[.]d))", VERSION)[0]

    return dhtml.Span(
        [
            dhtml.A(
                ref_id,
                href=GH_URL_TEMPLATE.format(ref_id),
                target="_blank",
            ),
            " (locally modified)" if dirty else "",
        ],
    )


def code_ify(text, language="none"):
    """Add Markdown backtick code block fences to the input text.

    Default language type is 'none', to suppress syntax highlighting.
    """
    return f"```{language}\n{text}\n```"


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
            [
                "Paste any URL from a Sphinx docset, enter the desired search term, "
                "select your options, and go!",
                dhtml.Br(),
                "See the ",
                dhtml.A(
                    [dhtml.Code("sphobjinv suggest"), " CLI docs"],
                    href="https://sphobjinv.readthedocs.io/en/stable/cli/suggest.html",
                    target="_blank",
                ),
                " for more information.",
            ]
        ),
        dhtml.Div(
            children=(
                "Please report any problems (or delight!) on the ",
                dhtml.A(
                    "issue tracker",
                    href="https://github.com/bskinn/soi-app/issues",
                    target="_blank",
                ),
                ", on Twitter (",
                dhtml.A(
                    "@btskinn", href="https://twitter.com/btskinn", target="_blank"
                ),
                "), or on Mastodon (",
                dhtml.A(
                    "@btskinn@fosstodon.org",
                    href="https://fosstodon.org/@btskinn",
                    target="_blank",
                ),
                ").",
            ),
            className="report-problems",
        ),
        dhtml.Br(),
        dhtml.Div(
            [
                dhtml.Span(className="input-label", children="URL:"),
                dcc.Input(
                    type="url",
                    size="80",
                    id=INPUT_URL,
                    placeholder=(
                        "E.g., https://docs.python.org/3/library/functions.html#eval"
                    ),
                    debounce=True,
                ),
            ]
        ),
        dhtml.Div(
            [
                dhtml.Span(className="input-label", children="Search Term:"),
                dcc.Input(
                    type="text",
                    size="45",
                    id=INPUT_SEARCH,
                    placeholder="E.g., pathlib.Path",
                    debounce=True,
                ),
            ]
        ),
        dhtml.Div(
            dcc.Checklist(
                id=CHKLIST_INDEX_SCORE,
                options=[CHKBX_INCLUDE_SCORE, CHKBX_INCLUDE_INDEX],
                value=[CHKBX_INCLUDE_SCORE],
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
            children=code_ify("Loading..."),
            id=DIV_RESULT_DISPLAY,
            className="sphobjinv-output",
        ),
        dhtml.Div(
            className="footer",
            children=[
                dhtml.Div(
                    [
                        (
                            f"Copyright © {COPYRIGHT_YEARS} Brian Skinn. "
                            "Site content is licensed under "
                        ),
                        dhtml.A(
                            "CC BY 4.0",
                            href="http://creativecommons.org/licenses/by/4.0/",
                            target="_blank",
                        ),
                        ".",
                    ]
                ),
                dhtml.Div(
                    [
                        f"Version {VERSION}, source on GitHub at ",
                        get_source_link(),
                        ".",
                    ]
                ),
                dhtml.Div(
                    [
                        "Hosted on ",
                        dhtml.A(
                            "PythonAnywhere",
                            href="https://www.pythonanywhere.com",
                            target="_blank",
                        ),
                        " via a ",
                        dhtml.A(
                            "FreeDNS",
                            href="https://freedns.afraid.org",
                            target="_blank",
                        ),
                        " subdomain. Built with ",
                        dhtml.A(
                            "Plotly Dash",
                            href="https://dash.plotly.com/",
                            target="_blank",
                        ),
                        f" v{dash.__version__} and ",
                        dhtml.A(
                            "sphobjinv",
                            href="https://sphobjinv.readthedocs.io/en/stable",
                            target="_blank",
                        ),
                        f" v{soi.__version__}.",
                    ]
                ),
            ],
        ),
    ],
)


@app.callback(
    dash.Output(DIV_RESULT_DISPLAY, "children"),
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

    if CHKBX_INCLUDE_SCORE in chklist_values:
        option_str += "s"

    if CHKBX_INCLUDE_INDEX in chklist_values:
        option_str += "i"

    option_str += f"t{threshold_value}"

    result = sp.run(
        [
            SOI_EXECUTABLE,
            "suggest",
            option_str,
            str(url_value),
            str(search_value),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode > 1:
        return (
            code_ify(f"Error during execution:\n\n{result.stderr}\n{result.stdout}"),
            " ",
        )

    if url_value and search_value:
        return (code_ify(f"{result.stderr}\n{result.stdout}"), " ")
    else:
        return (code_ify("(Enter search values)"), " ")


if __name__ == "__main__":
    app.run_server(debug=True)
