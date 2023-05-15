#!/usr/bin/env python3
"""Run the generator on example data."""

import sys
from os.path import join
import runpy


sys.path.insert(0, join('..', '..'))

sys.argv = ['', 'test-terminal-table.sqlite']
sys.argv += ['--styles', 'styles-template.css']
runpy.run_module('qet_terminal_tables', run_name='__main__')
