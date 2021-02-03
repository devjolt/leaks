#from pdfrw import PdfReader
import pypdftk

def make_dict():

    PDF_PATH = 'l_a_r.pdf'
    pdf = PdfReader(PDF_PATH)

    print(pdf.Info)
    #print(pdf)

    pdf_fields = {}
    pdf_field_list = []

    for field in pdf.Root.AcroForm.Fields:
        #print(f"'{field.T[ 1:-1]}':form.cleaned_data['{field.T[ 1:-1]}'],")
        pdf_fields[field.T[1:-1]] = field.V
        pdf_field_list.append(field.T[1:-1])

    #print(pdf_field_list)
    #print(pdf_fields)

def fill_form(data_dict, out_file):
    PDF_PATH = 'leaks/l_a_r.pdf'
    out_file = out_file
    generated_pdf = pypdftk.fill_form(
        pdf_path = PDF_PATH,
        datas = data_dict,
        out_file = out_file,
    )

