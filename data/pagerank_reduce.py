#! /usr/bin/env python

import sys

# Convergence threshold
EPSILON = .005

def main(argv):
    key = str()
    current = float()
    old = float()
    children = str()
    power_ext = str()
    # While we have a line to process
    for line in sys.stdin:
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        key, _, value = line.partition("\t")
        # Get the count from the key
        count, _, _ = key.partition("_")
        count = int(count)
        # If we got graph structure information
        if value.startswith("*"):
            # Strip the tagging character
            value = value[1:]
            # value now reads [C , current , old , children ; power_ext]
            # If this node has converged, we are done
            if value.startswith("C"):
                sys.stdout.write("%s\t%s\n" % (key, value))
                return
            # The current rank is now the previous rank
            old, _, data = value.partition(",")
            # data reads [old , children ; power_ext]
            old = float(old)
            # Ignore the rank before the now previous rank, store the children
            _, _, children = data.partition(",")
            children, _, _ = children.partition(";")
            # Get the rank term used for power extrapolation
            _, _, power_ext = data.partition(";")
        else:
            # Otherwise, we got a rank contribution
            current += float(value)
    # Update this node's rank
    current = 0.85 * current + 0.15

    # Perform power extrapolation for d = 6
    #if count == 8:
    #    power_ext = float(power_ext)
    #    current = (1 / (1 - .15 ** 6)) * (current - (.85 ** 6) * power_ext)
    #    power_ext = str(power_ext)
    # Store rank after second iteration to use for power extrapolation
    if count == 2:
        power_ext = str(current)

    # Write the updated line, along with a convergence flag
    #*** change epsilon convergence
    sys.stdout.write("%s\t%s,%f,%f,%s;%s\n" %
        (key, "C" * (abs(current - old) / current <= EPSILON), current,
         old, children, power_ext))

if __name__ == "__main__":
    main(sys.argv)
