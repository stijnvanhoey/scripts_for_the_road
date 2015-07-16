# -*- coding: utf-8 -*-
"""
Bibtex export from Mendely cleanup

Following fields are not needed to incorporate when exporting to bibtex (however default by Mendeley):
 - file
 - issn
 - isbn
 - pmid
 - keywords
 - url
 - month
 - annote
 - language
 - abstract
 - mendeley-tags

@author: stvhoey
"""

import sys

def remove_fields(infile, outfile, fields):
    '''
    Remove the lines containing any of the fields listed

    infile : str
        file to modify
    outfile : str
        new file to create
    fields : list of str
        fields for which lines need to be removed
    '''
    # Check extension
    if infile[-3:] != 'bib':
        raise Exception('file for modification is not a .bib file')

    bibfile = open(infile, "r")
    newbibfile = open(outfile, "w")
    for line in bibfile.readlines():
        # check for all fields if present
        if not sum([line.startswith(field) for field in fields]) > 0:
            newbibfile.write(line)
    bibfile.close()
    newbibfile.close()


def main(argv=None):
    """

    """
    fields = ['file', 'issn', 'isbn', 'pmid', 'keywords', 'url', 'month',
              'annote', 'language', 'abstract', 'mendeley-tags']

    # argv[0] is always the file name itself
    sourcefile = sys.argv[1]
    outfile = sys.argv[2]
    remove_fields(sourcefile, outfile, fields)

if __name__ == "__main__":
    sys.exit(main())
