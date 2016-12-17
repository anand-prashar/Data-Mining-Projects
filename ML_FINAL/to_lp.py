#!/usr/bin/env python3

# convert the problem to an ILP problem format which gurobi can recognize

from __future__ import print_function

import sys

if len(sys.argv) != 2:
    print('''
Usage:
    {} [input-file|- (for stdin)]
    '''.format(sys.argv[0]).strip())
    sys.exit()

from load_graph import load_graph

file_in = None

if sys.argv[1] == '-':
    file_in = sys.stdin
else:
    file_in = open(sys.argv[1])

vertices, edges = load_graph(file_in)

if sys.argv[1] != '-':
    file_in.close()

# a minimization problem
print('Minimize')
print('  ', end = '')

for i in range(len(vertices)):
    print('{:+} v{}'.format(vertices[i], i + 1), end = ' ')

print('')

print('Subject to')
# all edges must be covered
for e in edges:
    print('  v{} + v{} >= 1'.format(e[0], e[1]))

# variables are all boolean
print('Binary')
print('  ', end = '')
for i in range(len(vertices)):
    print('v{}'.format(i + 1), end = ' ')

print('')
print('End')
