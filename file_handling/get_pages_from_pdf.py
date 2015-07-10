import os
import sys
from pyPdf import PdfFileWriter, PdfFileReader

def Extract_the_page(path, filename,this_page):
    '''  
    this_page = 37
    path = "D:\Download"
    filename = "Bard_Faulkner.pdf"
    '''
    filepath=os.path.join(path, filename)
    pdf_toread = PdfFileReader(file(filepath, "rb"))

    output = PdfFileWriter()
    output.addPage(pdf_toread.getPage(int(this_page)))
    outputStream = file(os.path.join(path,"your_selected_page.pdf"), "wb")
    output.write(outputStream)
    outputStream.close()

if __name__ == '__main__':
    print 'Extracting the page number %s of document %s in path %s...' %(sys.argv[2],sys.argv[3],sys.argv[1])
    print os.path.join(sys.argv[1], sys.argv[3])
    if  not os.path.exists(os.path.join(sys.argv[1], sys.argv[3])):
        raise Exception('File not found, please define path as first argument, pagenumber as second and filename third')
    Extract_the_page(sys.argv[1],sys.argv[3],sys.argv[2])
    print 'Page extracted, file is called your_selected_page.pdf'