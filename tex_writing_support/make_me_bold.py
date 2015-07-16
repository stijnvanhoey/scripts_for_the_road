#
# Copyright (c) 2015 by Stijn Van Hoey. All Rights Reserved.
#
"""
Script to make all entries of a bibtex-file  which matchees your name bold,
specificly useful for CV-styling
"""

import sys

def make_me_bold(input_file_path, output_file_path,
                 firstname='Stijn', lastname='Van Hoey'):
    """
    """
    with open(input_file_path, 'r') as inputfile:
        with open(output_file_path, 'w') as outputfile:
            for line in inputfile:
                # current assumption: texbf only for highlight own name
                if 'textbf' not in line and lastname in line:
                    splitline = line.partition(lastname)
                    # replace last name
                    boldlast = splitline[1].replace(lastname, ''.join(['\\textbf{', lastname, '}']))
                    # replace first name or initial
                    if splitline[2].find(firstname) != -1:
                        boldfirst = splitline[2].replace(firstname, ''.join(['\\textbf{', firstname, '}']), 1)
                    else:
                        first_initial =  ''.join([firstname[0],'.'])
                        boldfirst = splitline[2].replace(first_initial, ''.join(['\\textbf{', first_initial, '}']), 1)
                    line = [splitline[0], boldlast, boldfirst]
                outputfile.write(''.join(line))


def main(argv=None):
    """
    """
    # argv[0] is always the file name itself
    sourcefile = sys.argv[1]
    outfile = sys.argv[2]
    first = sys.argv[3]
    last = sys.argv[4]
    make_me_bold(sourcefile, outfile, first, last)

if __name__ == "__main__":
    sys.exit(main())
