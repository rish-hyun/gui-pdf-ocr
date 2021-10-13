import cv2
import numpy as np
from pytesseract import image_to_string, pytesseract


class OCR:
    def __init__(self):
        self.area_threshold = 5000
        self.text_len_thresh = 10
        pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    # --------------------------------------------------------------------------------------

    def show(self, img):
        cv2.imshow('img', cv2.resize(img, (0, 0), fx=0.2, fy=0.2))
        cv2.waitKey(0)

    # --------------------------------------------------------------------------------------

    def pre_processing(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        dilate = cv2.dilate(thresh, kernel, iterations=8) # 8
        opening = cv2.morphologyEx(dilate, cv2.MORPH_OPEN, kernel, iterations=12) # 12

        return opening

    # --------------------------------------------------------------------------------------

    def get_contours(self, img):
        cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # cnts = cv2.findContours(img, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return cnts[0] if len(cnts) == 2 else cnts[1]

    # --------------------------------------------------------------------------------------

    def paragraph_extract(self, ocr_text):
        para_count = 0
        paragraph_list = []

        for text in ocr_text:
            paragraph = text.split('\n\n')
            if len(paragraph) > 1:
                for para in paragraph:
                    para_count += 1
                    paragraph_list.append(f'({para_count}) {para.strip()}\n\n')
            else:
                para_count += 1
                paragraph_list.append(f'({para_count}) {text.strip()}\n\n')

        return paragraph_list

    # --------------------------------------------------------------------------------------

    def apply_ocr(self, img):
        img = np.array(img)
        pre_process_img = self.pre_processing(img)
        contours = self.get_contours(pre_process_img)[::-1]

        ocr_text = []
        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > self.area_threshold:
                x, y, w, h = cv2.boundingRect(cnt)
                text_list = image_to_string(img[y:y + h, x:x + w]).split('\n\n')

                for text in text_list:
                    if len(text.strip()) > self.text_len_thresh:

                        ocr_text.append(text)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

        return img, self.paragraph_extract(ocr_text)

# from pdf2image import convert_from_path
# file_path = 'Samples/test.pdf'
# 
# ocr = OCR()
# img, text = ocr.apply_ocr(convert_from_path(file_path, dpi=400)[0])
# # ocr.show(img)
# # cv2.imwrite('test-ocr.jpg', img)
# 
# print(text)
