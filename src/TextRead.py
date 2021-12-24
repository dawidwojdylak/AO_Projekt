import pytesseract

class TextRead:
    def __init__(self,im):
        self.text = pytesseract.image_to_string(im)

    def __str__(self):
        """
        This method is called when print() or str() function is invoked on an object.
        """
        return self.text
