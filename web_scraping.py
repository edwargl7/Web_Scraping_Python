import logging
import re
import ssl
import traceback
import urllib.request as urllib_request

import pandas as pd
from bs4 import BeautifulSoup

logname = "log/web_scraping.log"
logging.basicConfig(
    filename=logname,
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger('web_scraping')

# Regular Expressions - RegEx
REGEX_NUMBER = re.compile('^\\d*.- ')  # e.g. '1.- '
REGEX_STATE = re.compile(' ?- ?\\(([aA|nN].*)\\)')  # e.g. ' - (Avalado)'
REGEX_PLAN = re.compile('Plan de trabajo:(.*?)Estado del arte:')
REGEX_STATE_ART = re.compile('Estado del arte:(.*?)Objetivos:')
REGEX_OBJECTIVE = re.compile('Objetivos:(.*?)Retos:')
REGEX_CHALLENGE = re.compile('Retos:(.*?)Visión:')
REGEX_VISION = re.compile('Visión:(.*)?')


class WebScraping:
    def __init__(self):
        self.context = ssl.SSLContext()
        self.data_without_filter = None

    def _data_validation(self, field_title, method_message, url):
        try:
            field_exists, idx, msg = self._get_index_by_table_title_and_class(
                field_title)
            if field_exists:
                data_exists, df, msg = self._get_data_page_by_table(url, idx)
                if data_exists:
                    data_dict = df.to_dict(orient='split')['data']
                    data_dict = data_dict[1:]
                    return data_dict, 'data processed successfully'
                else:
                    return {}, msg
            else:
                return {}, msg
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            msg = 'error validating ' + method_message
            return {}, msg

    def _get_data_page_by_table(self, url, index):
        try:
            if not self.data_without_filter:
                self.get_data_without_filter(url)
            tables = self.data_without_filter.find_all('table')
            df = pd.read_html(str(tables))
            return True, df[index], 'table obtained successfully'
        except IndexError as ie:
            logger.error(ie)
            logger.error(str(traceback.format_exc()))
            return False, None, 'error getting data from table, index error'
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return False, None, 'error getting data from table'

    def _get_index_by_table_title_and_class(self, title):
        try:
            classes = self.data_without_filter.find_all(
                "td", class_="celdaEncabezado")
            titles = [str(x.text).lower() for x in classes]
            return True, titles.index(title), 'table found successfully'
        except ValueError as ve:
            # Add exception if it doesn't exist
            logger.error(ve)
            logger.error(str(traceback.format_exc()))
            return False, None, 'table \'{table}\' not found'.format(table=title)
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return False, None, 'error getting table index'

    def get_data_without_filter(self, url):
        try:
            response = urllib_request.urlopen(url,
                                              context=self.context).read()
            soup = BeautifulSoup(response, 'lxml')
            self.data_without_filter = soup
            return True, 'data obtained successfully'
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            self.data_without_filter = None
            return False, 'it is not possible to obtain data from this url'

    def get_basic_data(self, url):
        try:
            field_title = "datos básicos"
            m_msg = 'basic data'
            data, msg = self._data_validation(field_title,
                                              m_msg, url)
            if isinstance(data, (list, tuple)):
                if len(data) > 0:
                    result = {key: value for (key, value) in data}
                else:
                    result = {}
                    msg = 'table without records'
                return result, msg
            else:
                return data, msg
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return {}, 'error processing basic data'

    def get_list_of_institutions(self, url):
        try:
            field_title = "instituciones"
            m_msg = 'the list of institutions'
            institutions, msg = self._data_validation(field_title,
                                                      m_msg, url)
            if isinstance(institutions, (list, tuple)):
                if len(institutions) > 0:
                    result = {}
                    for idx, inst in enumerate(institutions):
                        inst = REGEX_NUMBER.sub('', inst[0])
                        data = REGEX_STATE.split(inst)
                        name, state = data[0], data[1]
                        result[idx] = {
                            'Institución': name,
                            'Estado': state
                        }
                else:
                    result = {}
                    msg = 'table without records'
                return result, msg
            else:
                return institutions, msg
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return {}, 'error processing list of institutions'

    def get_strategic_plan(self, url):
        try:
            field_title = "plan estratégico"
            m_msg = 'the strategic plan'
            data, msg = self._data_validation(field_title,
                                              m_msg, url)
            if isinstance(data, (list, tuple)):
                if len(data) > 0:
                    data = data[0][0]
                    result = {'Plan estratégico dividido': {}}
                    regex_list = [REGEX_PLAN, REGEX_STATE_ART,
                                  REGEX_OBJECTIVE, REGEX_CHALLENGE,
                                  REGEX_VISION]
                    title_list = ['Plan de trabajo', 'Estado del arte',
                                  'Objetivos', 'Retos', 'Visión']
                    for idx, regex in enumerate(regex_list):
                        text = regex.search(data)
                        if text:
                            text = text.group(1)
                            title = title_list[idx]
                            result['Plan estratégico dividido'][title] = text.strip()

                    result['Plan estratégico sin dividir'] = data
                else:
                    result = {}
                    msg = 'table without records'
                return result, msg
            else:
                return data, msg
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return {}, 'error processing the strategic plan'

    def get_members(self, url):
        # P, Q, R, W del drive
        # Nombre, Inicio-fin vinculación
        try:
            title = "integrantes del grupo"
            err, index = self.__get_index_by_table_title_and_class(title)
            err, df = self.__get_data_page_by_table(url, index)
            data_dict = df.to_dict(orient='split')['data']
            print(data_dict)
            if isinstance(data_dict[0], (list, tuple)):
                result = {key: value for (key, value) in data_dict}
            else:
                result = {key: value for (key, value) in enumerate(data_dict)}
            return result
        except Exception as ex:
            logger.error(ex)
            logger.error(str(traceback.format_exc()))
            return {}
