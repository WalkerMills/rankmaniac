#! /usr/bin/env python

import sys

def main(argv):
    # While we have a line to process
    for line in sys.stdin:
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        key, _, value = line.partition("\t")
        # Parse data in the form current_rank,old_rank,children
        data = value.split(",")
        current = float(data[0])
        try:
            children = [int(n) for n in data[2:]]
            # Distribute the rank of this node among its children
            inheritance = current / len(children)
            for node in children:
                sys.stdout.write("NodeId:%s\t%s\n" % (node, inheritance))
        except (ValueError, ZeroDivisionError):
            sys.stdout.write("%s\t%s\n" % (key, current))
        # Continue passing local graph information
        sys.stdout.write("%s\t*%s\n" % (key, value))

if __name__ == "__main__":
    main(sys.argv)
