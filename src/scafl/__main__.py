import sys
from os.path import dirname, abspath

module_dir = dirname(dirname(abspath(__file__)))
if sys.path[0] != module_dir:
    sys.path.insert(0, module_dir)

import scafl

scafl.main()
