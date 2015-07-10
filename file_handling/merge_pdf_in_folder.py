# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:22:55 2012

@author: VHOEYS
"""

import os
import sys
import glob
from pyPdf import PdfFileWriter, PdfFileReader


def MergePDFinFolder(pathin):
    '''
    Merges all pdf files together from a folder,
    make sure the path is in double brackets if it contains spaces
    '''
    path = pathin
    output = PdfFileWriter()
    
    for infile in glob.glob(os.path.join(path, '*.pdf') ):
        print "current file merged is: " + infile    
        inputpdf = PdfFileReader(file(infile, "rb"))
        output.addPage(inputpdf.getPage(0))

    outputStream = file(os.path.join(path,'all_out.pdf'), "wb")       
    output.write(outputStream)
    outputStream.close() 



if __name__ == '__main__':
    print 'Merge all pdf files in folder %s' %sys.argv[1]
    if os.path.exists(os.path.join(sys.argv[1],'all_out.pdf')):
        raise Exception('all_out.pdf already exists')
    MergePDFinFolder(sys.argv[1])
    print 'Merge files finished, merged file all_out.pdf created'

 