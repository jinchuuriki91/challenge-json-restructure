#!/usr/bin/python3

import sys
import getopt
import json


class Node:
    
    def __init__(self, obj_id, title, level, parent_id):
        self.obj_id = obj_id
        self.title = title
        self.level = level
        self.parent_id = parent_id
        self.children = []
    
    def __repr__(self):
        return "<%s(%s) --> %s>" % (self.title, self.obj_id, self.level)

    def to_dict(self, children=[]):
        return {
            "id": self.obj_id,
            "title": self.title,
            "level": self.level,
            "parent_id": self.parent_id,
            "children": children
        }

    def insert(self, node):
        if self.obj_id == node.parent_id:
            self.children.append(node)
        else:
            for child in self.children:
                child.insert(node)

    def display(self):
        if self.children:
            children = []
            for child in self.children:
                children.append(child.display())
            return self.to_dict(children)
        else:
            return self.to_dict()


def main(argv):
    input_dir = None
    try:
        opts, args = getopt.getopt(argv,"i:",["input="])
    except getopt.GetoptError:
        print('script.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--input"):
            input_dir = arg

    try:
        with open(input_dir, "r") as fp:
            input_dict = json.loads(fp.read())
            head_node = Node(None, None, None, None)
            for level in sorted(input_dict):
                # get the nodes at this level
                for value in input_dict[level]:
                    node = Node(value["id"], value["title"], value["level"], value["parent_id"])
                    head_node.insert(node)
            print(json.dumps(head_node.display()["children"], indent=4))
    except Exception:
        print("Entry a valid input json file path")
    

if __name__ == "__main__":
    main(sys.argv[1:])