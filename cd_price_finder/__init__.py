# -*- coding: utf-8 -*-
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class MusicMagpie:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.name = "MusicMagpie"

    def login(self, email, password):
        self.driver.get('https://www.musicmagpie.co.uk/login/')
        self.driver.find_element_by_css_selector('input[type=email]').send_keys(email)
        p = self.driver.find_element_by_css_selector('input[type=password]')
        p.send_keys(password)
        p.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 10).until(cond.url_contains('my-account'))

    def add_barcode(self, barcode):
        if 'start-selling' not in self.driver.current_url:
            self.driver.get('https://www.musicmagpie.co.uk/start-selling/')
            self.driver.find_element_by_class_name('sellMedia').click()
        barcode_box = self.driver.find_element_by_class_name('mediaValTextbox')
        barcode_box.send_keys(barcode)
        barcode_box.send_keys(Keys.ENTER)

    def remove_barcode(self, barcode):
        for row in self.driver.find_elements_by_class_name('rowDetails_Media'):
            if row.find_element_by_class_name('col_Code').text == barcode:
                row.find_element_by_id('btnDelete').click()
                return
        raise RuntimeError("Barcode not found")

    def results(self):
        r = []
        for row in self.driver.find_elements_by_class_name('rowDetails_Media'):
            barcode = row.find_element_by_class_name('col_Code').text
            name = row.find_element_by_class_name('col_Title').text
            price = float(row.find_element_by_class_name('col_Price').text)
            r.append((barcode, name, price))
        return r

    def save_order(self):
        self.driver.find_element_by_id('btnSaveOrder').click()
        WebDriverWait(self.driver, 10).until(cond.url_contains('saved-orders'))


class Ziffit:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.name = "Ziffit"

    def login(self, email, password):
        self.driver.get('https://www.ziffit.com/en-gb/log-in')
        self.driver.find_element_by_css_selector('button.cookiebtn').click()
        self.driver.find_element_by_id('email').send_keys(email)
        p = self.driver.find_element_by_id('password')
        p.send_keys(password)
        p.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 10).until(cond.url_contains('myaccount'))

    def add_barcode(self, barcode):
        if 'basket' not in self.driver.current_url:
            self.driver.get('https://www.ziffit.com/en-gb/basket')
        barcode_box = self.driver.find_element_by_name('barcode')
        barcode_box.send_keys(barcode)
        barcode_box.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 10).until(cond.visibility_of_element_located((By.CSS_SELECTOR, 'div.alert')))

    def remove_barcode(self, barcode):
        for row in self.driver.find_elements_by_css_selector('.ziffittable tbody tr'):
            _, barcode_elem, _, _, delete = row.find_elements_by_tag_name('th')
            if barcode_elem.text == barcode:
                delete.click()
                return
        raise RuntimeError("Barcode not found")

    def results(self):
        r = []
        for row in self.driver.find_elements_by_css_selector('.ziffittable tbody tr'):
            name, barcode, _, price, _ = [e.text for e in row.find_elements_by_tag_name('th')]
            price = float(price.strip('£'))
            r.append((barcode, name, price))
        return r

    def save_order(self):
        self.driver.find_element_by_css_selector('button[value="Save Trade for Later"]').click()


class WeBuyBooks:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.name = "WeBuyBooks"

    def _close_popups(self):
        close_buttons = self.driver.find_elements_by_class_name('cc-dismiss')
        close_buttons += self.driver.find_elements_by_css_selector('button[data-dismiss=toast]')
        for button in close_buttons:
            try:
                if button.is_displayed():
                    WebDriverWait(self.driver, 10).until(cond.visibility_of(button))
                    button.click()
            except TimeoutException:
                import ipdb
                ipdb.set_trace()

    def login(self, email, password):
        self.driver.get('https://www.webuybooks.co.uk/log-in/')
        self._close_popups()
        self.driver.find_element_by_id('customer_email').send_keys(email)
        p = self.driver.find_element_by_id('password')
        p.send_keys(password)
        p.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 10).until(cond.url_contains('my-account'))

    def add_barcode(self, barcode):
        if 'selling-basket' not in self.driver.current_url:
            self.driver.get('https://www.webuybooks.co.uk/selling-basket')
        self._close_popups()

        barcode_box = self.driver.find_element_by_name('isbn')
        barcode_box.send_keys(barcode)
        barcode_box.send_keys(Keys.ENTER)
        modal = WebDriverWait(self.driver, 10).until(cond.visibility_of_element_located((By.CSS_SELECTOR, '.modal.show#error_modal')))
        modal.find_element_by_class_name('button').click()

    def remove_barcode(self, barcode):
        if 'selling-basket' not in self.driver.current_url:
            self.driver.get('https://www.webuybooks.co.uk/selling-basket')
        self._close_popups()
        for row in self.driver.find_elements_by_class_name('trrow'):
            barcode = row.find_element_by_class_name('tdisbn').text
            if barcode == barcode:
                row.find_element_by_class_name('rejectOffer').click()
                return
        raise RuntimeError("Failed to find barcode")

    def results(self):
        if 'selling-basket' not in self.driver.current_url:
            self.driver.get('https://www.webuybooks.co.uk/selling-basket')
        self._close_popups()
        r = []
        for row in self.driver.find_elements_by_class_name('trrow'):
            name = row.find_element_by_class_name('tdtitle').text
            barcode = row.find_element_by_class_name('tdisbn').text
            price = float(row.find_element_by_class_name('tdval').text.strip('Â£'))
            r.append((barcode, name, price))
        return r

    def save_order(self):
        pass


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
