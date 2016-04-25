import re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from pylint import lint
from pylint.reporters.text import TextReporter

SCORE_PATTERN = r"([\d\.]+)\/"


def get_global_score(paths, rcfile=None):
    extra = ["--rcfile={}".format(rcfile)] if rcfile else []
    sio = StringIO()
    lint.Run(paths + extra, reporter=TextReporter(sio), exit=False)
    # filter out empty lines
    lines = [l for l in sio.getvalue().split("\n") if l]
    # last line should contain global score
    global_score_msg = lines[-1:][0]
    score_match = re.findall(SCORE_PATTERN, global_score_msg)[0]
    return float(score_match)
