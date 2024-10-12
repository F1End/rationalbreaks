import sys
import os.path as path

from streamlit.web import cli as stcli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", path.join("streamlit_UI.py")]
    # sys.argv = ["streamlit", "run", path.join("testtimer.py")]
    sys.exit(stcli.main())