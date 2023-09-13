import PyPDF2
import PyPDF2 as pp2

path = './data/1686895448707.pdf'
with open(path, 'rb') as file:
    reader = pp2.PdfReader(file)
    writer = PyPDF2.PdfWriter()
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page.merge_page(reader.pages[page_num])
        writer.add_page(page)
    writer.removeLinks()
    writer.removeAnnotations()
    writer.encrypt('')
    writer.write(open('./data/output.pdf', 'wb'))
