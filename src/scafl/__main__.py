import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))

import scafl.main

scafl.main.main()
