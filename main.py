import os
import fitz  # this is pymupdf
import tkinter
from tkinter import filedialog

sciezka_do_pliku = r"C:"
sciezka_do_zapisu = r"C:"

def find_location_id(text):
    x = text.find("Location ID : ")
    end = text.find("\n", x)  # koniec ID
    return int(text[x + 14:end])


def find_dealer_return_nbr(text):
    x = text.find("Dealer Return Nbr : ")
    end = text.find("\n", x) - 2  # koniec ID
    return text[x + len('Dealer Return Nbr : '):end]


def split_pdf():
    file_path = sciezka_do_pliku
    print(f'File exist: {os.path.isfile(file_path)}')

    with fitz.open(file_path) as doc:
        start_page = 0
        first_page = doc.load_page(0)
        text = first_page.get_text()
        previouse_numer_id = find_location_id(text)
        previouse_dealer_return_nbr = find_dealer_return_nbr(text)

        for iteration, page in enumerate(doc):
            text = page.get_text()
            number_id = find_location_id(text)
            dealer_return_nbr = find_dealer_return_nbr(text)
            if (previouse_numer_id != number_id) or (previouse_dealer_return_nbr != dealer_return_nbr):
                doc2 = fitz.open()
                doc2.insert_pdf(doc, from_page=start_page, to_page=iteration - 1)  # first 10 pages
                print(fr'{sciezka_do_zapisu}{previouse_numer_id}_'
                          fr'{previouse_dealer_return_nbr[:len(previouse_dealer_return_nbr)]}.pdf')
                doc2.save(fr'{sciezka_do_zapisu}{previouse_numer_id}_'
                          fr'{previouse_dealer_return_nbr[:len(previouse_dealer_return_nbr)]}.pdf')
                start_page = iteration
                previouse_numer_id = number_id
                previouse_dealer_return_nbr = dealer_return_nbr
                print(f'Nowy plik')
            print(f'Strona={iteration + 1}, ID={number_id}, Dealer nr={dealer_return_nbr}')


def open_broweser():
    global sciezka_do_pliku
    print('Search')
    filetypes = (
        ('PDF files', '*.pdf'),
        ('All files', '*.*')
    )

    sciezka_do_pliku = filedialog.askopenfilename(
        title='Choose file',
        initialdir='/',
        filetypes=filetypes)

    print(sciezka_do_pliku)
    odczyt_label.set('Location Packing Slips: ' + sciezka_do_pliku)


def save_file():
    global sciezka_do_zapisu
    sciezka_do_zapisu = filedialog.askdirectory()
    sciezka_do_zapisu += '/'
    print(sciezka_do_zapisu)
    zapis_label.set('Save Location: ' + sciezka_do_zapisu)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Split Packing Slips")

    root = tkinter.Tk()
    root.geometry('400x220')
    root.title("Split Packing Slips")

    b = tkinter.Button(root, text='Select Packing Slips', command=open_broweser)
    b.pack(pady=(10, 10))

    b1 = tkinter.Button(root, text='Select save location', command=save_file)
    b1.pack(pady=(1, 10))

    b2 = tkinter.Button(root, text='Split Packing Slips', command=split_pdf)
    b2.pack(side='bottom', pady=(1, 60))

    odczyt_label = tkinter.StringVar()
    odczyt_label.set('Location Packing Slips: ')
    l4 = tkinter.Label(root, textvariable=odczyt_label)
    l4.pack(side='bottom', pady=2)

    zapis_label = tkinter.StringVar()
    zapis_label.set('Save Location: ')
    l1 = tkinter.Label(root, textvariable=zapis_label)
    l1.pack(side='bottom', pady=3)

    root.mainloop()
