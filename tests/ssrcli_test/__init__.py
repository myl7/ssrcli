import sys
import os
import pathlib

pkg_dir = pathlib.Path(os.getcwd()).parent
sys.path.append(str(pkg_dir))
