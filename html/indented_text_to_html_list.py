#!/usr/bin/env python
"""Convert an indented list of text to nested html lists

example input:
    Main level item 1
        Indented level item 1
        Indented level item 2
            Double-indented level item 1
    Main level item 2
output:
    <ul>
        <li>Main level item 1
        <ul>
            <li>Indented level item 1</li>
            <li>Indented level item 2
            <ul>
                <li>Double-indented level item 1</li>
            </ul>
            </li>
        </ul>
        </li>
        <li>Main level item 2</li>
    </ul>

Version 0.1
2018-09-29
"""
import re
import argparse

def get_line_generator(file):
    with open(file, 'r') as fr:
        for line in fr:
            yield line.rstrip('\n')

indent_spaces_re = re.compile(r'^ +')

class Node:
    def __init__(self, content, parent=None):
        self.content = content
        self.children = list()
        self.parent = parent
        self.depth = 0
        if parent is None:
            pass
        else:
            parent.children.append(self)
            p = self
            while p.parent:
                p = p.parent
                self.depth += 1

    def to_html(self):
        if not self.children:
            return '{}<li>{}</li>'.format(
                ' '*4*self.depth,
                self.content,
            )
        children = '{spaces}<ul>\n{children}\n{spaces}</ul>'.format(
            spaces=' '*4*self.depth,
            children='\n'.join(c.to_html() for c in self.children),
        )
        if not self.parent:
            return children
        return '''{spaces}<li>{content}\n{children}\n{spaces}</li>'''.format(
            spaces=' '*4*self.depth,
            children=children,
            content=self.content
        )

def lines_depth_calculator(lines):
    last_level = 0
    for line in lines:
        if not line.strip():
            continue
        indent_spaces = indent_spaces_re.match(line)
        level = 0 if indent_spaces is None else int(len(indent_spaces.group(0))/4)

        depth_change = level - last_level

        yield depth_change, line.strip()

        last_level = level

def run_main():
    args = parse_cl_args()

    line_generator = get_line_generator(args.file)

    # children = []
    last_node = last_parent = root = parent = Node(None)

    for depth_change, line in lines_depth_calculator(line_generator):
        if depth_change == 0:
            node = Node(content=line, parent=last_parent)
        elif depth_change > 0:
            parent = last_node
            node = Node(content=line, parent=parent)
        elif depth_change < 0:
            parent = last_node.parent
            for i in range(abs(depth_change)):
                parent = parent.parent
            node = Node(content=line, parent=parent)

        last_parent = node.parent
        last_node = node

    print(root.to_html())

    success = True
    return success

def parse_cl_args():
    argParser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argParser.add_argument(
        'file', nargs='?', default='/dev/stdin'
    )

    args = argParser.parse_args()
    return args


if __name__ == '__main__':
    success = run_main()
    exit_code = 0 if success else 1
    exit(exit_code)


