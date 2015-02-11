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
        count, _, _ = key.partition(',')
        count = int(count)

        # If we got graph structure information
        if value.startswith("*"):
            # Strip the tagging character
            value = value[1:]
            # If this node has converged, we are done
            if value.startswith("C"):
                sys.stdout.write("%s\t%s\n" % (key, value))
                return
            # The current rank is now the previous rank
            old, _, data = value.partition(",")
            # Get the rank term used for power extrapolation
            power_ext, _, _ = data.partition(",")
            old = float(old)
            power_ext = float(power_ext)
            # Ignore the rank before the now previous rank, store the children
            _, _, children = data.partition(",")

        else:
            # Otherwise, we got a rank contribution
            current += float(value)

    # perform power extrapolation for d = 6
    if count == 8:
        current = (1 / .15) * (current - (.85 ^ 6) * power_ext)
    # otherwise scale normally with alpha, and add 1 - alpha
    else:
        current = 0.85 * current + 0.15
    # store rank after second iteration to use for power extrapolation
    if count == 2:
        power_ext = str(current)

    # Write the updated line, along with a convergence flag
    sys.stdout.write("%s\t%s,%f,%f,%f,%s\n" %
        (key, "C" * (abs(current - old) / current <= EPSILON), current,
         old, power_ext, children))

if __name__ == "__main__":
    main(sys.argv)
