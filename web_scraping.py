import logging
import ssl
import traceback
import urllib.request as urllib_request

import pandas as pd
from bs4 import BeautifulSoup

logname = "log/web_scraping.log"
logging.basicConfig(filename=logname,
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('web_scraping')


class WebScraping:
    def __init__(self):
        self.context = ssl.SSLContext()
        self.data_without_filter = None

    def get_data_without_filter(self, url):
        try:
            response = urllib_request.urlopen(url, context=self.context).read()
            soup = BeautifulSoup(response, 'lxml')
            self.data_without_filter = soup
            return True, 200
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            self.data_without_filter = None
            return False, 400

    def __get_data_page_by_table(self, url, index):
        try:
            if not self.data_without_filter:
                self.get_data_without_filter(url)
            tables = self.data_without_filter.find_all('table')
            df = pd.read_html(str(tables))
            return True, df[index]
        except IndexError as ie:
            logger.error(ie)
            logger.error(str(traceback.format_exc()))
            return False, ie
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return False, ex

    def __get_index_by_table_title_and_class(self, title):
        try:
            classes = self.data_without_filter.find_all("td", class_="celdaEncabezado")
            titles = [str(x.text).lower() for x in classes]
            return True, titles.index(title)
        except ValueError as ve:
            # Add exception if it doesn't exist
            logger.error(ve)
            logger.error(str(traceback.format_exc()))
            return False, ve
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return False, ex

    def get_basic_data(self, url):
        try:
            title = "datos básicos"
            err, index = self.__get_index_by_table_title_and_class(title)
            err, df = self.__get_data_page_by_table(url, index)
            data_dict = df.to_dict(orient='split')['data']
            if isinstance(data_dict[0], (list, tuple)):
                result = {key: value for (key, value) in data_dict}
            else:
                result = {key: value for (key, value) in enumerate(data_dict)}
            return result
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return {}
