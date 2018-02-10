import sys
from os.path import dirname, abspath, sep

directory = dirname(dirname(abspath(__file__)))
assert directory.split(sep)[-1].lower() == __name__
sys.path.append(directory)
