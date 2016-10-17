#! /usr/bin/env python2
import binascii
import sys
import re
import logging
import pprint
def unhex(line):
    # (1) '00000000  47 45 54 20 2f 20 48 54  54 50 2f 31 2e 31 0d 0a  GET / HT TP/1.1..'
    # (2) '47 45 54 20 2f 20 48 54 54 50 2f 31 2e 31 0d 0a'
    # (3) GET / HTTP/1.1\r\n
    return binascii.unhexlify(" ".join(line.split("  ")[1:3]).replace(" ",""))

def node(line, tree, block, prev_node):
    if line.startswith("\t"):
        node = 1
    else:
        node = 0
        
    if node == 0 and prev_node == 1:
        block = block + 1
        logging.debug("Incremented block %s => %s" % (block-1, block))
        tree["blocks"].append({ "0": {"lines":[], "bytes":[]}, "1":{"lines":[], "bytes":[]}})

    tree["blocks"][block][str(node)]["lines"].append(line.strip())
    tree["blocks"][block][str(node)]["bytes"].append(unhex(line.strip()))
    return block, node, tree

def add_node(line, tree, block):
    print line # Node 0: 172.17.0.2:44506
    r = r'^Node (\d): (.*)$'
    m = re.search(r, line)
    if m:
        logging.debug("Node '%s' has name '%s', adding to tree" % (m.group(1), m.group(2)))
        node = {}
        node["name"] = m.group(2)
        tree[m.group(1)] = node
        if m.group(1) > 0:
            block = 0
            tree["blocks"] = []
            tree["blocks"].append({ "0": {"lines":[], "bytes":[]}, "1":{"lines":[], "bytes":[]}})
            
        return tree, block
    else:
        logging.fatal("Found Node-line that did not match regexp(%s): %s" % (r, line))
        sys.exit(1)

def parse_lines(line):
    tree = {}
    block = -1
    prev_node = 0
    with open(sys.argv[1], "r") as file:
        for line in file:
            # https://www.wireshark.org/docs/man-pages/tshark.html
            if line.startswith("\t") or line.startswith("0"):
                block, prev_node, tree = node(line, tree, block, prev_node)
                pass
            elif line.startswith("="):
                pass # splitter
            elif line == "":
                pass # empty line
            elif line.startswith("Node "):
                print "Metadata: %s" %(line,)
                tree, block = add_node(line, tree, block)
            else:
                print "Metadata: %s" %(line,)
    return tree

def print_tree(tree):
    names = [tree[str(0)]["name"],tree[str(1)]["name"]]
    for block in tree["blocks"]:
        print "%s => %s" % ( names[0], names[1])
        try:
            print block["0"]["bytes"][0]
        except IndexError:
            print "<no data>"
        print ""
        print "%s => %s" % ( names[1], names[0])
        try:
            print block["1"]["bytes"][0]
        except IndexError:
            print "<no data>"
        print ""

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    tree = parse_lines(sys.argv[1])
    #logging.debug("TREE:\n" + pprint.pformat(tree, 4))
    print_tree(tree)
