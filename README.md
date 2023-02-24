# `sphobjinv suggest` Dash App

[`sphobjinv`][soi docs] is a toolkit for manipulating and inspecting Sphinx
`objects.inv` inventory files. It's my most popular open source project by a
considerable margin.

While I can't tell from the analytics I have access to, I suspect that the
majority of people are using it for the 'suggest' CLI functionality, rather than
the 'convert' CLI or API. If nothing else, 'suggest' is definitely the feature I
use the most.

It's not always convenient to install a PyPI or OS-distributed package to get
access to a tool you need. So, I've been thinking for a while about figuring out
a way to provide `sphobjinv suggest` as a web app. I explored
[Wooey][wooey docs] briefly a while ago, since it's specifically made to wrap a
webapp around a CLI. But, not having much web dev experience at the time, I
found it pretty cumbersome, and gave up the attempt.

Enter [Plotly Dash][dash docs]. I picked it up as part of work on another side
project, and realized that I might be able to use it as a platform for a
`sphobjinv suggest` web app. It's almost certainly not the most *efficient* way
to implement the thing, but it *works*, and it works in a pretty attractive way.

So, here is "`sphobjinv suggest` as a Service" (... SSaaS?). As of now (Nov
2022), it's built on Dash and `sphobjinv`, hosted at
[PythonAnywhere][pythonanywhere], and does all of the inventory downloading and
object searching server-side. If it gets popular, my next step is to try to
leverage PyScript to move the `suggest` portion client-side, so that I can keep
the number of PythonAnywhere workers to a minimum. One thing at a time, though.

Please report any problems with the app (or let me know that you like it!) on
the [Github issue tracker][issue tracker], on Twitter ([@btskinn][twitter]), or
on Mastodon ([@btskinn@fosstodon.org][mastodon]).

If you find yourself using the app quite a bit, please consider chipping in to
cover the hosting costs. Right now I'm set up to receive contributions via
GitHub Sponsors...any amount greatly appreciated.

Enjoy!


----

Copyright (c) Brian Skinn 2022

Website copy and docstrings are licensed under [CC BY 4.0][CC BY].

App code is released under the [MIT License][MIT License]. See [`LICENSE.txt`][GH License] for full license terms.



[CC BY]: http://creativecommons.org/licenses/by/4.0/
[dash docs]: https://plotly.com/dash/
[GH License]: https://github.com/bskinn/soi-app/blob/main/LICENSE.txt
[issue tracker]: https://github.com/bskinn/soi-app/issues
[mastodon]: https://fosstodon.org/@btskinn
[MIT License]: https://opensource.org/licenses/MIT
[pythonanywhere]: https://pythonanywhere.com
[soi docs]: https://sphobjinv.readthedocs.io/en/stable
[soi repo]: https://github.com/bskinn/sphobjinv
[twitter]: https://twitter.com/btskinn
[wooey docs]: https://wooey.readthedocs.io/en/latest/
[invisible change for testing]: https://google.com
