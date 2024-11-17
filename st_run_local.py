"""Run this file to kick off streamlit frontend locally on your browser"""

import sys
from os import path

from streamlit.web import cli as stcli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", path.join("streamlit_ui.py")]
    # sys.argv = ["streamlit", "run", path.join("testtimer.py")]
    sys.exit(stcli.main())
