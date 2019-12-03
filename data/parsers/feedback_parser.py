# -*- coding: UTF-8 -*-
import os
import string
import datetime
import urllib3
import logging
from random import choice
from pprint import pprint
from time import sleep
from ast import literal_eval

from progressbar import progressbar
from selenium.webdriver import Chrome, ActionChains, ChromeOptions
from selenium.common.exceptions import (
    NoSuchElementException,
    JavascriptException,
)


class Parser(object):
    """Feedbacks parser"""

    __slots__ = (
        'driver',
        'result_dir',
        '_headless',
        'db_callback',
        'logger'
    )

    def __init__(self, executable_path, db_callback, result_dir='result', headless=False):
        """Init"""

        # Logger
        self.logger = logging.getLogger('parser')
        self.logger.setLevel(logging.WARNING)

        self.db_callback = db_callback
        self._headless = headless
        self.driver = self.get_driver(executable_path=executable_path)
        self.result_dir = result_dir
        # self.create_data_structure(result_dir=result_dir)

    @staticmethod
    def create_data_structure(result_dir):
        """Create structure of output files"""
        os.makedirs(f'{result_dir}/good', exist_ok=True)
        os.makedirs(f'{result_dir}/bad', exist_ok=True)
        os.makedirs(f'{result_dir}/neutral', exist_ok=True)
        open(f'{result_dir}/data_file.json', 'w+').close()

    def get_driver(self, executable_path: str) -> Chrome:
        """Get and setup chrome driver

        :param executable_path: pth to chrome driver
        :return: Chrome driver instance
        """

        capabilities = {
            "browserName": "chrome",
            "version": "72.0",
            "screenResolution": "1200x800x8",
            "enableVNC": True,
            "enableVideo": False,
            "pageLoadStrategy": "none",
            "chromeOptions": {
                'args': [
                    # '--blink-settings=imagesEnabled=false',
                    # '--disk-cache-size=33554432',
                    '--start-maximized',
                    '--incognito',
                    '--disable-notifications',
                    '--disable-logging',
                    '--disable-infobars',
                    '--disable-extensions',
                    '--disable-web-security',
                    '--no-sandbox',
                    '--disable-gpu',
                    '--silent',
                    '--disable-popup-blocking',
                    '--lang=ru',
                    '--ignore-certificate-errors',
                    '--log-level=3',
                    # f'--user-agent={random.choice(self.user_agents)}'
                ]
            }
        }

        options = ChromeOptions()
        options.add_argument('--log-level=3')
        if self._headless:
            options.add_argument('--headless')

        driver = Chrome(executable_path=executable_path,
                        desired_capabilities=capabilities,
                        options=options)
        return driver

    @staticmethod
    def generator(size: int = 8) -> str:
        """Generate random string"""
        chars = string.ascii_letters + string.digits
        return ''.join([choice(chars) for _ in range(size)])

    @staticmethod
    def write_json(file_name, result_dir, mark=2):
        """Append feedback information into json file"""
        date = datetime.datetime.now()

        add = {
            "student_name": "Dasha Anora",
            "student_group": 651,
            "student_number": 0,
            "Data source": "http://firms.turizm.ru/otzyv/6053/",
            "date": f'{date.day}_{date.month}_{date.year}',
            "category": mark,
            "filename": f'{result_dir}/{file_name}'
        }

        # Open to read
        with open(f"{result_dir}/data_file.json", "r") as write_file:
            try:
                data = write_file.read()
                data = literal_eval(data)
            except SyntaxError:
                data = []

        # Open to write
        with open(f"{result_dir}/data_file.json", "w") as write_file:
            data.append(add)
            pprint(data, stream=write_file, indent=4)

    def process_page(self, page_url: str) -> None:
        """Open all tabs in single page and then parse all feedbacks"""
        driver = self.driver

        # Open needed page
        driver.get(page_url)
        sleep(7)

        more_btns = driver.find_elements_by_class_name('about__more-span')

        # Open all closed tabs in page
        for btn in more_btns:
            try:
                action = ActionChains(driver)
                sleep(.2)
                action.move_to_element(btn).perform()
                btn.click()
            except JavascriptException:
                self.logger.info('Ошибка JavaScript')

        marks = {
            'Великолепно': 'good',
            'Ужасно': 'bad',
            'Плохо': 'bad',
            'Хорошо': 'neutral',
            'Отлично': 'good'
        }

        review_cont = driver.find_elements_by_class_name('hcr__review')
        for i, feedback in enumerate(review_cont):
            # Pass through all feedback containers to get text and review
            sleep(1)
            self.logger.info('Text', i, 'from', len(review_cont))
            try:
                review = feedback.find_element_by_class_name('hcr__rate-review-text')
                text_el = feedback.find_element_by_class_name('hcr__text')

                name = f'{marks.get(str(review.text))}/{self.generator()}.txt'
                text = text_el.text
                text_words = text.split()

                # Validate
                if len(text_words) > 1000:
                    self.logger.info('> 1000 words')
                    try:
                        text = ' '.join(text_words[:1000])
                    except IndexError:
                        self.logger.info('Error in text convertation')

                # TODO: Change it
                # if review.text in marks:
                #     try:
                #         with open(f'{self.result_dir}/{name}', 'w+') as f:
                #             f.write(text)
                #     except UnicodeEncodeError:
                #         print('Encode error')
                #         continue
                # else:
                #     print(review.text)

                if marks.get(str(review.text)) == 'good':
                    mark = 1
                elif marks.get(str(review.text)) == 'bad':
                    mark = -1
                else:
                    mark = 0

                # TODO: Add in db
                # self.write_json(file_name=name, mark=mark)
                self.db_callback(text=text, mark=mark)
            except NoSuchElementException:
                self.logger.info('No such element')

    def run(self, page_count=1) -> None:
        """Main parser method"""

        base_url = 'https://firms.turizm.ru/firms_otzyv/page_{page_num}/'

        # Proceed pages
        for page in progressbar(range(1, page_count+1)):
            self.process_page(page_url=base_url.format(page_num=page))
