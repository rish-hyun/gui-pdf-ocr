from PIL import ImageTk, Image
from pdf2image import convert_from_path

from tkinter.ttk import Separator
from tkinter import Tk, LabelFrame, Label, Frame, Button, Text
from tkinter.filedialog import askopenfilename

from ocr import OCR


class GPO(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1000x600')
        self.title('PDF OCR')
        # self.resizable(False, False)
        self.init_frame()
        self.img = None

    # --------------------------------------------------------------------------------------

    def set_text(self, ocr_text):
        self.ocr_text.config(state='normal')
        self.ocr_text.delete(1.0, 'end')
        self.ocr_text.insert('insert', ocr_text)
        self.ocr_text.config(state='disabled')

    # --------------------------------------------------------------------------------------

    def set_image(self, img):
        h = self.pdf_label.winfo_height()
        w = self.pdf_label.winfo_width()

        tk_image = ImageTk.PhotoImage(img.resize((w,h), Image.ANTIALIAS))
        self.pdf_label.configure(image=tk_image)
        self.pdf_label.image = tk_image

    # --------------------------------------------------------------------------------------

    def open_file(self):
        self.pdf_label.configure(text='please wait. . .')
        file_path = askopenfilename(
            title='Select a PDF...',
            filetypes=(('PDF', '*.PDF'),))

        if file_path:
            self.pdf_label.configure(text=f'{file_path} loading . .')
            self.update()

            self.img = convert_from_path(file_path, dpi=400)[0]
            self.set_image(self.img)

        else:
            self.pdf_label.configure(text='PDF not loaded, try loading it again')

    # --------------------------------------------------------------------------------------

    def get_ocr(self):
        self.set_text('Please wait . . .')
        self.update()

        if self.img is None:
            text = 'Load a PDF first'
        else:
            img,text = OCR().apply_ocr(self.img)
            self.img = Image.fromarray(img)
            self.set_image(self.img)

        self.set_text(text)

    # --------------------------------------------------------------------------------------

    def clear_file(self):
        self.img = None
        self.init_pdf_frame()
        self.init_ocr_frame()

    # --------------------------------------------------------------------------------------

    def init_frame(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame = Frame(self)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1, uniform=1)
        self.frame.columnconfigure(1, weight=1, uniform=1)
        self.frame.grid(column=0, row=0, sticky='news', padx=10, pady=10)

        self.init_pdf_frame()
        self.init_ocr_frame()

    # --------------------------------------------------------------------------------------

    def init_pdf_frame(self):
        image_viewer = LabelFrame(self.frame, text="PDF")
        image_viewer.rowconfigure(2, weight=1)
        image_viewer.columnconfigure(0, weight=1)
        image_viewer.grid(column=0, row=0, sticky='news')

        options = Frame(image_viewer)
        options.columnconfigure(0, weight=1)
        options.columnconfigure(1, weight=1)
        options.columnconfigure(2, weight=1)
        options.grid(column=0, row=0, padx=5, pady=10, sticky='news')

        open_button = Button(options, text='Open', command=self.open_file)
        open_button.grid(column=0, row=0, padx=10, sticky='news')

        clear_button = Button(options, text='Clear', command=self.clear_file)
        clear_button.grid(column=1, row=0, padx=10, sticky='news')

        resize_button = Button(options, text='Resize Image', command=lambda: self.set_image(self.img))
        resize_button.grid(column=2, row=0, padx=10, sticky='news')

        line = Separator(image_viewer, orient='horizontal')
        line.grid(row=1, column=0, sticky='ew')

        self.pdf_label = Label(image_viewer, text="PDF result appears here")
        self.pdf_label.grid(row=2, column=0, padx=10, pady=10, sticky='news')

    # --------------------------------------------------------------------------------------

    def init_ocr_frame(self):
        ocr_frame = LabelFrame(self.frame, text="OCR")
        ocr_frame.rowconfigure(2, weight=1)
        ocr_frame.columnconfigure(0, weight=1)
        ocr_frame.grid(column=1, row=0, sticky='news')

        options = Frame(ocr_frame)
        options.columnconfigure(0, weight=1)
        options.grid(column=0, row=0, padx=5, pady=10, sticky='news')

        ocr_button = Button(options, text='OCR', command=self.get_ocr)
        ocr_button.grid(column=0, row=0, padx=10, sticky='news')

        line = Separator(ocr_frame, orient='horizontal')
        line.grid(row=1, column=0, sticky='ew')

        self.ocr_text = Text(ocr_frame)
        self.set_text('OCR text appears here')
        self.ocr_text.grid(row=2, column=0, padx=10, pady=10, sticky='news')


if __name__ == '__main__':
    GPO().mainloop()
