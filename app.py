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

INTERVAL_OUTPUT_TIMER = "interval-output-timer"
INTERVAL_STATS = "interval-stats"


proc = None
buf_stdout = ""
suggest_running = False
halt_loop = True


def code_ify(text):
    return f"```none\n{text}\n```"


app.layout = dhtml.Div(
    [
        dhtml.Div(
            [
                dhtml.Span("URL"),
                dcc.Input(type="url", size="80", id=INPUT_URL, required=True),
            ]
        ),
        dhtml.Div(
            [
                dhtml.Span("Search Term"),
                dcc.Input(type="text", size="45", id=INPUT_SEARCH, required=True),
            ]
        ),
        dhtml.Button("Search", id=BTN_SEARCH),
        dcc.Interval(id=INTERVAL_OUTPUT_TIMER, interval=300, disabled=True),
        dhtml.Div("", id=INTERVAL_STATS),
        dcc.Markdown(
            code_ify("Awaiting input..."),
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
    dash.Output(INTERVAL_OUTPUT_TIMER, "disabled"),
    dash.Output(INTERVAL_STATS, "children"),
    dash.Input(BTN_SEARCH, "n_clicks"),
    dash.Input(INPUT_URL, "n_submit"),
    dash.Input(INPUT_SEARCH, "n_submit"),
    dash.Input(INTERVAL_OUTPUT_TIMER, "n_intervals"),
    dash.State(INPUT_URL, "value"),
    dash.State(INPUT_SEARCH, "value"),
    dash.State(RESULT_DISPLAY, "children"),
)
def run_suggest(
    n_clicks,
    n_submit_url,
    n_submit_search,
    n_timer_intervals,
    url_value,
    search_value,
    result_text,
):
    global proc, buf_stdout, suggest_running, halt_loop

    if halt_loop:
        halt_loop = False
        return (code_ify("Awaiting search..."), True, "Halted")

    if not suggest_running:
        # suggest operation is not running, so we should start it
        if url_value is None or search_value is None:
            # Don't start the search process if either input is missing; disabled=True
            return (result_text, True, f"Off ({n_timer_intervals})")

        buf_stdout += "\nStarting proc"
        proc = sp.Popen(
            ["sphobjinv", "suggest", "-uas", str(url_value), str(search_value)],
            stdout=sp.PIPE,
            stderr=sp.STDOUT,
            text=True,
        )
        suggest_running = True
        halt_loop = False

        # Turn on the Interval; set disabled to False
        return (
            code_ify(buf_stdout + proc.stdout.read()),
            False,
            f"On ({n_timer_intervals})",
        )

    else:
        # suggest operation IS running, which means we should update it
        rc = proc.poll()
        # buf_stdout += data

        if rc:
            suggest_running = False
            halt_loop = True
            if rc != 0:
                return (
                    code_ify(f"{buf_stdout}\n\nIt errored ({rc=})"),
                    True,
                    f"Off ({n_timer_intervals})",
                )
            else:
                return (code_ify(buf_stdout), True, f"Off ({n_timer_intervals})")
        else:
            suggest_running = True
            halt_loop = False
            buf_stdout += proc.communicate()[0]
            return (code_ify(buf_stdout), False, f"On ({n_timer_intervals})")

        # if url_value and search_value:
        #     return f"```none\n{result.stderr}\n{result.stdout}\n```"
        # else:
        #     return f"```none\nEnter search values\n```"


if __name__ == "__main__":
    app.run_server(debug=True)
