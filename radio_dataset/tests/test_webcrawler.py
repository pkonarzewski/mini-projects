import unittest
from web_crawler import StationPlaylistArchiveCreator, SqlLiteWraper
from datetime import date
from bs4 import BeautifulSoup


class TestStationPlaylistArchiveCreator(unittest.TestCase):
    def setUp(self):
        self.archiver = StationPlaylistArchiveCreator(station="rmf", page="radioarchiwum")

        self.src_testdata = r"tests\data\test_offline_radioarchiwum_20160101.html"
        self.test_soup = StationPlaylistArchiveCreator.file_to_soup(self.src_testdata)
        self.last_url = "https://radioarchiwum.net/radio/13/rmf-fm/date/01-01-2016/page/340"

    def test_initiation_archive_creator(self):
        exp_station = "rmf"
        exp_page = "radioarchiwum"
        exp_base_url = r"https://radioarchiwum.net/radio/{station_id}/{station_name}/date/{archive_date}"
        exp_sub_url = r"/page/{start_row}"
        exp_rstation_dict = {'station_id': 13, 'station_name': 'rmf-fm'}
        arch = StationPlaylistArchiveCreator(station=exp_station, page=exp_page)

        self.assertEqual(arch.station, exp_station)
        self.assertEqual(arch.page, exp_page)
        self.assertEqual(arch.page_metadata["base_url"], exp_base_url)
        self.assertEqual(arch.page_metadata["subpage_url"], exp_sub_url)
        self.assertEqual(arch.rstation_adrs, exp_rstation_dict)

    @unittest.skip("skip")
    def test_archive_data(self):
        self.archiver.archive_data(date(2016, 1, 1), date(2016, 1, 1))
        raise

    def test_gen_date_range(self):
        date_range = self.archiver.generate_date_range(date(2015, 1, 30), date(2015, 2, 1))
        exp_date_range = [date(2015, 1, 30), date(2015, 1, 31), date(2015, 2, 1)]
        self.assertEqual(date_range, exp_date_range)

    @unittest.skip("skip")
    def test_get_all_urls(self):
        url_list = self.archiver.get_all_urls_from_date(date(2016, 1, 1))
        exp_url_list = None
        self.assertEqual(url_list, exp_url_list)

    def test_get_base_url(self):
        url = self.archiver.get_base_url_for_date(date(2016, 1, 1))
        exp_url = r"https://radioarchiwum.net/radio/13/rmf-fm/date/01-01-2016"
        self.assertEqual(url, exp_url)

    def test_to_file_to_soup(self):
        file_path = self.src_testdata
        soup = self.archiver.file_to_soup(file_path)
        self.assertEqual(type(soup), BeautifulSoup)

    @unittest.skip("skip")
    def test_get_subpages_urls(self):
        sub_urls = self.archiver.get_subpages_urls(self.test_soup)
        exp_sub_urls = [""]
        self.assertEqual(sub_urls, exp_sub_urls)

    def test_get_subpages_urls(self):
        soup = self.archiver.file_to_soup(r"tests/data/test_offline_radioarchiwum_20160101_6subpages.html")
        sub_urls = self.archiver.get_subpages_urls(soup)
        exp_sub_urls = ["https://radioarchiwum.net/radio/13/rmf-fm/date/01-01-2016/page/20",
                        "https://radioarchiwum.net/radio/13/rmf-fm/date/01-01-2016/page/40",
                        "https://radioarchiwum.net/radio/13/rmf-fm/date/01-01-2016/page/60",
                        "https://radioarchiwum.net/radio/13/rmf-fm/date/01-01-2016/page/80",
                        "https://radioarchiwum.net/radio/13/rmf-fm/date/01-01-2016/page/100",
                        "https://radioarchiwum.net/radio/13/rmf-fm/date/01-01-2016/page/120"]

        self.assertEqual(sub_urls, exp_sub_urls)

    def test_extract_last_url(self):
        last_url = self.archiver.extract_last_url(self.test_soup)
        exp_last_url = self.last_url
        self.assertEqual(last_url, exp_last_url)

    def test_get_last_row(self):
        last_raw = self.archiver.get_last_row(self.last_url)
        exp_last_raw = 340
        self.assertEqual(last_raw, exp_last_raw)

    @unittest.skip("skip")
    def test_to_sqlite(self):
        self.archiver.to_sqllite()

    @unittest.skip("skip")
    def test_to_hdf5(self):
        self.test_to_hdf5()


class TestSqlLiteWraper(unittest.TestCase):
    def setUp(self):
        self.sql_wraper = SqlLiteWraper(r"tests\test_web_crawler.db3")

    def test_init_(self):
        self.sql_wraper.db_src = r"tests\web_crawler.db3"

    def test_read_db(self):
        custom_query = self.sql_wraper._from_db(query="SELECT id FROM songs_data")
        exp_custom_query = {1, 2, 3}
        self.assertEqual(custom_query, exp_custom_query)

        two_cols_query = self.sql_wraper._from_db(query="SELECT artist, new_song_flag FROM songs_data")
        exp_two_col_query = [('Darude', 0), ('Enia', 0), ('Michael Jackson', 1)]
        self.assertEqual(two_cols_query, exp_two_col_query)

    def test_get_urls_list(self):
        pend_urls = self.sql_wraper.get_urls_list(url_type="pending")
        exp_pend_urls = {"http://songs.arch/2", "http://songs.arch/3"}
        self.assertEqual(pend_urls, exp_pend_urls)

    def test_append_new_urls(self):
        # kasowanie jezeli cos jest
        self.sql_wraper._execute_stmt(query="DELETE FROM url_history_empty")

        new_urls = {"http://songs.arch/12", "http://songs.arch/13"}
        self.sql_wraper.append_new_urls(new_urls)

        sql_new_urls = self.sql_wraper._from_db("SELECT url FROM url_history_empty")
        self.assertEqual(new_urls, sql_new_urls)

