from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class MusicMagpie:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.musicmagpie.co.uk/start-selling/')
        self.driver.find_element_by_class_name('sellMedia').click()

    def add_barcode(self, barcode):
        barcode_box = self.driver.find_element_by_class_name('mediaValTextbox')
        barcode_box.send_keys(barcode)
        barcode_box.send_keys(Keys.ENTER)

    def results(self):
        r = []
        for row in self.driver.find_elements_by_class_name('rowDetails_Media'):
            barcode = row.find_element_by_class_name('col_Code').text
            name = row.find_element_by_class_name('col_Title').text
            price = float(row.find_element_by_class_name('col_Price').text)
            r.append((barcode, name, price))
        return r


class Ziffit:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.ziffit.com/en-gb/basket')

    def add_barcode(self, barcode):
        barcode_box = self.driver.find_element_by_name('barcode')
        barcode_box.send_keys(barcode)
        barcode_box.send_keys(Keys.ENTER)


class WeBuyBooks:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.webuybooks.co.uk/')


class Zapper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://zapper.co.uk/list-page/')


class Momox:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.momox.co.uk/')
