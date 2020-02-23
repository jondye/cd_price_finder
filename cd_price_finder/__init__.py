# -*- coding: utf-8 -*-
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait


class MusicMagpie:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def add_barcode(self, barcode):
        if 'start-selling' not in self.driver.current_url:
            self.driver.get('https://www.musicmagpie.co.uk/start-selling/')
            self.driver.find_element_by_class_name('sellMedia').click()
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

    def add_barcode(self, barcode):
        if 'basket' not in self.driver.current_url:
            self.driver.get('https://www.ziffit.com/en-gb/basket')
        barcode_box = self.driver.find_element_by_name('barcode')
        barcode_box.send_keys(barcode)
        barcode_box.send_keys(Keys.ENTER)

    def results(self):
        r = []
        for row in self.driver.find_elements_by_css_selector('.ziffittable tbody tr'):
            name, barcode, _, price, _ = row.text.split('\n')
            price = float(price.strip('£'))
            r.append((barcode, name, price))
        return r


class WeBuyBooks:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def add_barcode(self, barcode):
        if 'selling-basket' not in self.driver.current_url:
            self.driver.get('https://www.webuybooks.co.uk/selling-basket')

        barcode_box = self.driver.find_element_by_name('isbn')
        barcode_box.send_keys(barcode)
        barcode_box.send_keys(Keys.ENTER)

    def results(self):
        try_again_buttons = [b for b in self.driver.find_elements_by_class_name('button') if 'Try Again' in b.text]
        if try_again_buttons:
            try_again_buttons[0].click()  # dismiss modal
        r = []
        for row in self.driver.find_elements_by_class_name('trrow'):
            name, barcode = row.find_element_by_class_name('tdtitle').text.split('\n\n')
            price = float(row.find_element_by_class_name('tdval').text.strip('£'))
            r.append((barcode, name, price))
        return r


class Zapper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://zapper.co.uk/list-page/')
        # turn of "recycling"
        self.driver.find_element_by_class_name('react-switch').click()

    def add_bacdode(self, barcode):
        barcode_box = self.driver.find_element_by_id('form-field-name')
        barcode_box.send_keys(barcode)
        barcode_box.send_keys(Keys.ENTER)


class Momox:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.momox.co.uk/')


def load_barcodes_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]
