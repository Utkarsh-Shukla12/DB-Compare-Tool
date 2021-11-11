# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 15:21:29 2021

@author: Utkarsh Shukla
"""

from fpdf import FPDF


# save FPDF() class into a 
# variable pdf
pdf = FPDF(orientation = 'L', unit = 'mm', format='A4')
  
# Add a page
pdf.add_page()
  

# set style and size of font 
# that you want in the pdf
pdf.set_font("Arial", size = 15)
  
# create a cell
pdf.cell(200, 10, txt = "Utkarsh Shukla", 
         ln = 1, align = 'C')
  
# add another cell
pdf.cell(200, 10, txt = "List of Comparision Source and Table.",
         ln = 2, align = 'C')
  



def dfToPdf(DF, file_name):
    pdf = FPDF(orientation = 'L', unit = 'mm', format='A4')
    pdf.set_author('Utkarsh Shukla')
    pdf.add_page()
    pdf.set_font('arial', 'B', 11)
    pdf.cell(60)
    pdf.cell(75, 10, 'Utkarsh Shukla', 0, 2, 'C')
    pdf.cell(90, 10, ' ', 0, 2, 'C')
    pdf.cell(-55)
    columnNameList = list(DF.columns)
    for header in columnNameList[:-1]:
        pdf.cell(35, 10, columnNameList[-1], 1, 0, 'C')
    pdf.cell(35, 10, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-140)
    pdf.set_font('arial', '', 11)
    for row in range(0, len(DF)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                pdf.cell(35,10, str(DF['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(35,10, str(DF['%s' % (col_name)].iloc[row]), 1, 2, 'C')  
                pdf.cell(-140)
    pdf.output(file_name+'.pdf', 'F')
    print('File has been Created')

"""def dataFrameToPDF(DF, file_name):
    pdf.add_page()
    # save the pdf with name .pdf
    f = open('dfc.html','w')
    a = DF.to_html()
    f.write(a)
    f.close()
    weasyprint.HTML('dfc.html').write_pdf('GFG.pdf')
    print('Written to PDF')
    #pdfkit.from_file('dfc.html', 'GFG.pdf')  
    """
