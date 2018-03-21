# TODO wymuszenie odswierzenia
from bs4 import BeautifulSoup
import urllib.request
import os
import inspect
import re
import codecs
import random
import argparse


class MeltSongs(object):

    artist_hrefs = {
        "kaczmarski": r"http://www.tekstowo.pl/piosenki_artysty,jacek_kaczmarski,alfabetycznie,strona,{}.html",
        "coma": r"http://www.tekstowo.pl/piosenki_artysty,coma,alfabetycznie,strona,{}.html",
        "budka_s": r"http://www.tekstowo.pl/piosenki_artysty,budka_suflera,alfabetycznie,strona,{}.html",
        "peja": r"http://www.tekstowo.pl/piosenki_artysty,peja,alfabetycznie,strona,{}.html",
        "grubson": r"http://www.tekstowo.pl/piosenki_artysty,grubson,alfabetycznie,strona,{}.html"
    }

    banned_english_songs = set(['afternoons_in_the_colour_of_lemo', 'always_summer', 'better_man', 'confusion', 'dance_with_a_queen',
                                'don_t_set_your_dogs_on_me', 'eckhart__eng_', 'excess__prelude_', 'f_t_m_o', 'f_t_p_', 'fuck_the_police',
                                'furious_fate', 'jesie_', '_just', '_keep_the_peace', '_late', '_lion', 'locomotive', '_moscow', 't_b_t_r',
                                'nothing_for_you', 'poisonous_plants', 'rainy_song', 'silence_and_fire', 'song_4_boys', 'struggle',
                                'summertime', 'tranfusion', 'turn_back_the_river', 'coma_way.', 'what_do_you_want_from_me_',
                                'when_the_music_is_a_flame', 'with_you', 'witnesses_of_the_decline_of_the_eternal_boys_land'])

    def __init__(self, artist, pages_count, refresh=False):
        self.initial_href = self.artist_hrefs[artist]
        self.pages_count = pages_count
        self.refresh = refresh

        # tworzenie folderow jezeli nie ma
        self.temp_dir = r'D:\tmp\markovch'
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        SCRIPT_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.out_dir = SCRIPT_PATH + r'\data'
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        self.page_link = re.search('^(.*)/+', self.initial_href).group(1)
        self.db_file_path = self.out_dir + '\\' + re.search('piosenki_artysty,(.*),alfabetycznie', self.initial_href).group(1) + '_songs_db.file'

        # gogo
        self.songs_paths = self.download_songs(self.initial_href, self.pages_count)

    def _download_file(self, link, refresh):
        '''Download file from link and return path to local file'''

        local_name = re.sub('\W', '_', re.search('.*/(.*).html$', link).group(1)) + '.html'
        local_file = self.temp_dir + '\\' + local_name

        if not os.path.isfile(local_file) or refresh is True:
            print("Pobieranie pliku: {} ...".format(local_name))
            urllib.request.urlretrieve(link, local_file)
        else:
            pass
            # print("Plik istnieje: {} .".format(local_name))
        return local_file

    def download_songs(self, initial_href, pages_count):
        '''Download table of content a then dowlnoad each of url, return list of local files. Filter unwanted.'''
        spaths = []

        # pobieranie spisu tresci a potem wyluskiwanie z kazdego listy linkow do poszczegolnych piosenek, które zostają również pobrane
        for n in range(1, self.pages_count + 1):
            link = initial_href.format(n)

            songs_list_file = self._download_file(link, refresh=False)

            page = codecs.open(songs_list_file, 'r', encoding='utf8').read()
            soup = BeautifulSoup(page)

            data = soup.findAll("div", {"class": "ranking-lista"})
            for div in data:
                links = div.findAll('a', class_='title')
                for a in links:
                    link = self.page_link + a['href']
                    spaths.append(self._download_file(link, self.refresh))

        # usuwanie zbannowanych linkow
        banned = set([song for song in spaths for bann in self.banned_english_songs if re.search(bann, song)])
        # print('Pozyskano {} piosenek, {} zostało usuniętych z listy'.format(len(spaths), len(banned)))

        [spaths.remove(x) for x in banned]

        return spaths  # zwraca liste scieżek piosenek

    def generate_db(self, refresh=False):
        '''Generate file for MarkovChain class. Saves on disc'''
        # TODO: jezeli potrzbne statystyki to print
        songs_paths = self.songs_paths
        words_list = ''

        if os.path.isfile(self.db_file_path) and refresh is False:
            # print("Plik istnieje.")
            pass
        else:
            print("Tworzenie pliku...")
            for spath in songs_paths:
                # sname = re.search(r'(piosenka.*)_?.html', spath).group(1) + ':'
                page = codecs.open(spath, "r", encoding='utf8').read()
                soup = BeautifulSoup(page)
                html_song_lyrics = soup.findAll("div", {"class": "song-text"})

                for song in html_song_lyrics:
                    if len(html_song_lyrics) > 1:
                        print("Blad, znaleziono wiecej tekstow")
                        break

                    words = song.text.replace('Tekst piosenki:', '').replace('Poznaj historię zmian tego tekstu', '')
                    words = re.sub('/|_|,|\.|\!|"|:|-|x[0-9]+', '', words)
                    # words += '.'
                    words = words.lower()
                    words = words.split()

                # Łączenie po spacjami
                words_list += ' '.join(words)

            # Zapisywanie do pliku
            with codecs.open(self.db_file_path, "w", encoding="utf8") as f:
                f.write(words_list)
                print("Plik stworzony.")
        return 1


class MarkovChain():

    def __init__(self, file):
        self.file = file
        self.cache = {}
        self.words = []
        self.generate_triples()

    def generate_triples(self):
        db_songs = codecs.open(self.file, "r", encoding="utf8").read()
        self.words = db_songs.split()
        for x in range(len(self.words) - 2):
            key = (self.words[x], self.words[x + 1])
            if key in self.cache:
                self.cache[key].append(self.words[x + 2])
            else:
                self.cache[key] = [self.words[x + 2]]
        return

    def generate_song(self, size=25):
        seed = random.randint(0, len(self.cache) - 3)
        w1, w2 = self.words[seed], self.words[seed + 1]
        gen_song = []
        for i in range(size):
            gen_song.append(w1)
            # print(self.cache[(w1, w2)])
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_song.append(w2)
        return (" ".join(gen_song))


# Main
parser = argparse.ArgumentParser(description='Generate songs using Markov Chains.')
parser.add_argument('artist_name', metavar='-a', type=str, nargs='?', default='coma', help='Name of artist to process: coma, kaczmarski, budka_s, peja, grubson')
args = parser.parse_args()

artist = args.artist_name

# Tworzenie bazy
songs_db = MeltSongs(artist, 4)
songs_db.generate_db(refresh=False)

# Generowanie tekstów piosenek
markov_songs = MarkovChain(songs_db.db_file_path)
lirycs = markov_songs.generate_song()
print("\nPiosnka od {0}: \n {1}".format(artist, lirycs))
