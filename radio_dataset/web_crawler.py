# TODO: soup albo url zapisany w atrybucie albo soap jako atrybut

import requests
from bs4 import BeautifulSoup
from pakobox import gen_date_range
import codecs
import sqlite3
from itertools import chain
from os import path


class SqlLiteWraper(object):

    SQLITE_DATA_ADRS = {
        "pending_urls": "SELECT url FROM url_history WHERE visited = 0",
        "visited_urls": "SELECT url FROM url_history WHERE visited = 1"
    }

    TABLES_INSERT_DEF = {
        "url_history": '''INSERT INTO url_history VALUES(?,?,?)''',
        "songs_data": '''INSERT INTO songs_data VALUES(?,?,?,?,?,?)'''
    }

    def __init__(self, db_src):
        self.db_src = db_src
        self._test_db_exists()

    def _test_db_exists(self):
        if path.exists(self.db_src) is False:
            raise FileNotFoundError("Nie odnaleziono pliku bazy danych '{}'".format(self.db_src))

    def get_urls_list(self, url_type):
        try:
            q = self.SQLITE_DATA_ADRS[url_type+"_urls"]
        except KeyError:
            raise KeyError("Nieoczekiwany typ url '{}': oczekiwane 'pending', 'visited'".format(url_type))
        return self._from_db(q)

    def _from_db(self, query):
        conn = sqlite3.connect(self.db_src)
        c = conn.cursor()

        result = c.execute(query).fetchall()

        if len(result[0]) == 1:
            result = set(chain.from_iterable(result))

        conn.commit()
        conn.close()

        return result

    def append_new_urls(self, urls):
        self._data_to_db(table, urls)

    def _data_to_db(self, table, data):
        conn = sqlite3.connect(self.db_src)
        c = conn.cursor()

        data = self.format_data_to_db()
        c.executemany('''INSERT INTO url_history VALUES(?,?,?)''', data)

    def _execute_stmt(self, query):
        conn = sqlite3.connect(self.db_src)
        c = conn.cursor()

        c.execute(query)

        conn.commit()
        conn.close()

class StationPlaylistArchiveCreator(object):

    DB_NAME = "web_crawler.db3"

    PAGE_URL_DATA = {
        "radioarchiwum": {
            "base_url": r"https://radioarchiwum.net/radio/{station_id}/{station_name}/date/{archive_date}",
            "subpage_url": r"/page/{start_row}",
            'date_format': "%d-%m-%Y",
            "station_data": {
                "rmf": {
                    'station_id': 13,
                    'station_name': 'rmf-fm',
                }
            }
        }
    }

    def __init__(self, station, page="radioarchiwum"):
        self.station = station
        self.page = page
        self.sqlitedb = SqlLiteWraper(self.DB_NAME)

        # METADANE DLA STRONY DO WYCIAGANIA
        self.page_metadata = self.PAGE_URL_DATA[page]
        self.rstation_adrs = self.PAGE_URL_DATA[page]["station_data"][station]

    def archive_data(self, start_date, end_date):
        date_range = self.generate_date_range(start_date, end_date)
        for date in date_range:
            try:
                # bierz url
                pass
            except ValueError:
                print("ValueError")

    @staticmethod
    def generate_date_range(s_date, e_date):
        n_periods = (e_date - s_date).days + 1
        return gen_date_range(s_date, n_periods, 'd')

    def get_all_urls_from_date(self, date):
        base_url = self.get_base_url_for_date(date)
        sub_urls = self.get_subpages_urls(base_url)
        return [base_url] + sub_urls

    def get_base_url_for_date(self, input_date):
        base_url = self.page_metadata['base_url'].format(
                station_id=self.rstation_adrs["station_id"],
                station_name=self.rstation_adrs["station_name"],
                archive_date=input_date.strftime(self.page_metadata["date_format"])
        )
        return base_url

    def get_subpages_urls(self, base_soup):
        subpages_url_pattern = base_url + self.SUB_PAGE_SUFFIX
        last_subpage_url = self.extract_last_url(soup)
        last_row = self.get_last_row(last_subpage_url)

        subpages_url = [subpages_url_pattern(start_row=x) for x in range(20, last_row+1, 20)]

        assert last_subpage_url == subpages_url[-1], "Ostatni element nie zgadza sie"

        return subpages_url

    @staticmethod
    def extract_last_url(soup):
        last_url = None
        for page_links in soup.findAll('p', {'class': 'pagination'}, limit=1):
            for link in page_links.findAll('span', {'class': 'pagination_last'}, limit=1):
                last_url = link.findParent()['href']
        return last_url

    @staticmethod
    def get_last_row(url):
        return int(str(url).split("/")[-1])

    @staticmethod
    def url_to_soup(url):
        page_source = requests.get(url)
        html_text = page_source.text
        return BeautifulSoup(html_text, "lxml")

    @staticmethod
    def file_to_soup(src):
        html_text = codecs.open(src, encoding="utf8")
        return BeautifulSoup(html_text, "lxml")

    @staticmethod
    def to_sqllite(data, out_path, table):
        raise

    @staticmethod
    def to_hdf5(data, out_path):
        raise
