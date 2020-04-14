import ssl
import urllib.request as urllib_request
import pandas as pd
from bs4 import BeautifulSoup

URL = 'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000013887'


def run(url):
    context = ssl.SSLContext()
    response = urllib_request.urlopen(url, context=context).read()
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table')
    print(type(tables))

    df = pd.read_html(str(tables))
    df[4].to_csv('./test.csv')


run(URL)
