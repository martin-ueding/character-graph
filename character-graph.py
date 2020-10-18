#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2020 Martin Ueding <dev@martin-ueding.de>

import argparse
import pprint
import subprocess

import jinja2

template_src = '''
graph {
overlap = false
splines = true

{% for source, sink in connections %}
"{{ source }}" -- "{{ sink }}"
{% endfor %}
}
'''


def main():
    options = _parse_args()

    characters = {}

    for line in open(options.text):
        line = line.strip()
        if line.startswith(': '):
            names = tuple(prev.split(' / '))
            characters[names] = line
        prev = line

    pprint.pprint(characters)

    connections = set(
        tuple(sorted((source[0], sink[0])))
        for source in characters.keys()
        for name in source
        for sink, text in characters.items()
        if name in text
    )

    pprint.pprint(connections)

    template = jinja2.Template(template_src)
    rendered = template.render(connections=connections)

    with open('characters.dot', 'w') as f:
        f.write(rendered)

    subprocess.run(['neato', 'characters.dot', '-Tpdf', '-o', 'characters.pdf'])
    subprocess.run(['neato', 'characters.dot', '-Tpng', '-o', 'characters.png'])


def _parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('text')
    options = parser.parse_args()

    return options


if __name__ == '__main__':
    main()
