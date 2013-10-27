#!/usr/bin/env python

import sys
import os.path

try:
	from buildtool import runner
except ImportError:
	sys.path.append(os.path.abspath("."))
	from buildtool import runner

if __name__ == '__main__':
	runner.run()
