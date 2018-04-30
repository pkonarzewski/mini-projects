"""Symulator gry w ruletke."""
import random
from collections.abc import Set, Sequence
from casino_simulator.exceptions import InvalidBet


class RouletteGame(object):
    """Definicja podstawowych zasad gry."""
    def __init__(self):
        # BETS OUTCOME
        self.straight_bet_odds = 35
        self.split_bet_odds = 17
        self.street_bet_odds = 11
        self.corner_bet_odds = 8
        self.five_bet_odds = 6  # 0 00 1 2 3
        self.line_bet_odds = 5
        self.dozen_bet_odds = 2
        self.column_bet_odds = 2
        self.even_money_bet_odds = 1

        self.table_layout = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
            [13, 14, 15],
            [16, 17, 18],
            [19, 20, 21],
            [22, 23, 24],
            [25, 26, 27],
            [28, 29, 30],
            [31, 32, 33],
            [34, 35, 36]
        ]


class Outcome(object):
    """
    Zawiera Wygrana, na ktora moze być postawiony zaklad.

    Jedna przegroda na Ruletce moze miec wiele mozliwych wygranych.
    Wygrana posiada wspolczynnik wygranej. Jezeli odds wynosi 2 i
    postawimy 1 to wyplacane jest 2 plus postawione 1.

    name: Nazwa wygranej
    odds: Wspolczynnik wyplaty dla tej wygranej
    """

    def __init__(self, name, odds):

        self.name = name
        self.odds = odds

    def win_amount(self, amount):
        """
        Mnozy wspolczynnik wygranej przez ilosc obstawiona.

        :param amount: kwota postawiona
        :return: Mnozenie wspolczynnika i kwoty
        """
        return amount * self.odds

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.name != other.name:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return '{name:s} ({odds:d}:1)'.format_map(vars(self))

    def __repr__(self):
        return '{class_:s}({name!r}, {odds!r})'.format(
            class_=type(self).__name__, **vars(self))


class Bin(Set):
    """
    Przegroda zawiera zbior Wygranych z nim powiazanych.

    Reprezentuje przegrody ruletki z powiazanymi wyplatami.
    """

    def __init__(self, outcomes=()):
        self.outcomes = frozenset(outcomes)

    def __contains__(self, item):
        return item in self.outcomes

    def __iter__(self):
        return iter(self.outcomes)

    def __len__(self):
        return len(self.outcomes)

    def __str__(self):
        return ', '.join(map(str, self.outcomes))

    def __repr__(self):
        return str(self.outcomes)

    def add(self, *outcomes):
        """Dodaje Wygrane do Przegrody.

        *outcome: Wygrane ktore maja byc przypisane do Przegrody
        """
        self.outcomes |= set([*outcomes])


class NonRandom(random.Random):
    """Nielosowy generator liczb losowych."""

    def __init__(self):
        self.value = None

    def set_seed(self, value):
        """Zapisuje kolejna wartosc ktora zostanie zwrocona."""
        self.value = value

    def choice(self, sequence):
        return sequence[self.value]


class Wheel(Sequence):
    """
    Ruletaka skladajaca się z 38 Przegrod i generatora liczb pseudolosowych.

    Portafi wybrac w sposob losowy jedena z przegrod, symulujac w ten
    sposob zakrecenie kołem.
    Klasa zawiera rowniez mapowanie wszystkich rodzajow Wygranych
    identyfikowalnych po nazwie.
    """

    def __init__(self, rng=None):
        self.bins = tuple(Bin() for _ in range(38))
        self.rng = rng if rng else random.Random()
        self.all_outcomes = set()

    def __getitem__(self, index):
        return self.bins[index]

    def __len__(self):
        return len(self.bins)

    def add_outcome(self, number, outcome):
        """
        Dodaje podane Wygrane do Przegrody oraz unikatowa liste Wygranych.

        number: numer przegrody <0:37>
        outcome: Wygrana do dodania dla danej przegrody
        """
        self.bins[number].add(outcome)
        self.all_outcomes.add(outcome)

    def next(self):
        """
        Wybiera losowo jednena z przegrod ruletki.

        return: Bin
        """
        return self.rng.choice(self.bins)

    def get_bin(self, number):
        """
        Zwraca przegrode o podanym numerze.

        number: numer przegrody
)        return: Bin
        """
        return self.__getitem__(number)

    def get_outcome(self, name):
        """Zwraca Wygrana o podanej nazwie."""
        return [oc for oc in self.all_outcomes if oc.name.lower() == name.lower()][0]


class BinBuilder(object):
    """
    BinBuilder buduje Ruletka z Bins ze wszystkimi Outcomes.

    wheel: Objekt Ruletka ktory ma byc zainicjowany
    """

    def __init__(self):
        self.game = RouletteGame()

    def build_bins(self, wheel):
        self.straight_bets(wheel=wheel)
        self.split_bets(wheel=wheel)
        self.street_bets(wheel=wheel)
        self.corner_bets(wheel=wheel)
        self.line_bets(wheel=wheel)
        self.dozen_bets(wheel=wheel)
        self.column_bets(wheel=wheel)
        self.even_money_bets(wheel=wheel)
        self.five_bet(wheel=wheel)

    def straight_bets(self, wheel):
        """Generate straight bets."""
        for n in range(0, 37):
            wheel.add_outcome(n, Outcome(str(n), self.game.straight_bet_odds))
        wheel.add_outcome(37, Outcome('00', self.game.straight_bet_odds))

    def split_bets(self, wheel):
        """Generate split bets"""
        bet_name = 'Split {}-{}'

        # Left-Right pairs
        for row in self.game.table_layout:
            for n in row[:2]:
                wheel.add_outcome(n, Outcome(bet_name.format(n, n + 1), self.game.split_bet_odds))
                wheel.add_outcome(n + 1, Outcome(bet_name.format(n, n + 1), self.game.split_bet_odds))

        # Up-Down pairs
        for row in self.game.table_layout[:-1]:
            for n in row:
                wheel.add_outcome(n, Outcome(bet_name.format(n, n + 3), self.game.split_bet_odds))
                wheel.add_outcome(n + 3, Outcome(bet_name.format(n, n + 3), self.game.split_bet_odds))

    def street_bets(self, wheel):
        """Generate street bets."""
        bet_name = 'Street {}-{}-{}'

        for row in self.game.table_layout:
            for n in row:
                wheel.add_outcome(n, Outcome(bet_name.format(*row), self.game.street_bet_odds))

    def corner_bets(self, wheel):
        """Generate corner bets"""
        bet_name = 'Corner {}-{}-{}-{}'

        for row in self.game.table_layout[:-1]:
            for n in row[:-1]:
                bname = bet_name.format(n, n + 1, n + 3, n + 4)
                wheel.add_outcome(n, Outcome(bname, self.game.corner_bet_odds))
                wheel.add_outcome(n + 1, Outcome(bname, self.game.corner_bet_odds))
                wheel.add_outcome(n + 3, Outcome(bname, self.game.corner_bet_odds))
                wheel.add_outcome(n + 4, Outcome(bname, self.game.corner_bet_odds))

    def line_bets(self, wheel):
        """Generate line bets."""
        bet_name = 'Line {}-{}-{}-{}-{}-{}'

        for row in self.game.table_layout[:-1]:
            line_nr = [x for x in range(row[0], row[0] + 6)]
            bname = bet_name.format(*line_nr)
            for n in line_nr:
                wheel.add_outcome(n, Outcome(bname, self.game.line_bet_odds))

    def dozen_bets(self, wheel):
        """Generate dozen bes"""
        bet_name = 'Dozen {}-{}'

        for n in range(1, 37):
            if n <= 12:
                bname = bet_name.format(1, 12)
            elif n <= 24:
                bname = bet_name.format(13, 24)
            else:
                bname = bet_name.format(25, 36)
            wheel.add_outcome(n, Outcome(bname, self.game.dozen_bet_odds))

    def column_bets(self, wheel):
        """Generate column bets"""
        bet_name = 'Column {}'

        for row in self.game.table_layout:
            wheel.add_outcome(row[0], Outcome(bet_name.format(1), self.game.column_bet_odds))
            wheel.add_outcome(row[1], Outcome(bet_name.format(2), self.game.column_bet_odds))
            wheel.add_outcome(row[2], Outcome(bet_name.format(3), self.game.column_bet_odds))

    def even_money_bets(self, wheel):
        """Generate even-money bets"""

        for n in range(1, 37):
            if n < 19:
                wheel.add_outcome(n, Outcome('Low', self.game.even_money_bet_odds))
            else:
                wheel.add_outcome(n, Outcome('High', self.game.even_money_bet_odds))

            if n % 2 == 0:
                wheel.add_outcome(n, Outcome('Even', self.game.even_money_bet_odds))
            else:
                wheel.add_outcome(n, Outcome('Odd', self.game.even_money_bet_odds))

            if n in (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 24, 36):
                wheel.add_outcome(n, Outcome('Red', self.game.even_money_bet_odds))
            else:
                wheel.add_outcome(n, Outcome('Black', self.game.even_money_bet_odds))

    def five_bet(self, wheel):
        """Generate five bet"""
        bet_name = '00-0-1-2-3'

        for n in range(0, 4):
            wheel.add_outcome(n, Outcome(bet_name, self.game.five_bet_odds))

        # 00
        wheel.add_outcome(37, Outcome(bet_name, self.game.five_bet_odds))


class Bet(object):
    """
    Zaklad powiazuje Wygrana z kwota obstawiana jak i rowniez Gracza.

    amount: Kwota jaka zostala postawiona
    outcome: Wynik jaki jest obstawiony
    """

    def __init__(self, amount, outcome):
        self.amount = amount
        self.outcome = outcome

    def win_amount(self):
        """Zwraca kwote w przypadku zwyciestwa."""
        return self.amount + self.amount * self.outcome.odds

    def lose_amount(self):
        """Zwraca kwote stracona przy przegranej"""
        return self.amount

    def __str__(self):
        return '{0} on {1}'.format(self.amount, self.outcome)


class Table(object):
    """Stol zawiera wszystkie Zaklady umieszczone przez Gracza.

    Stol dba o limity, zaklada tylko jednego gracza.
    limit: wysokosc limitu na stole
    """
    def __init__(self, limit):
        self.limit = limit
        self.bets = []

    def is_valid(self, bet):
        """Sprawdza czy dany Zaklad nie przekroczy limitu stolu."""
        if sum([b.amount for b in self.bets]) + bet.amount <= self.limit:
            return True
        else:
            return False

    def place_bet(self, bet):
        """Umieszcza dany zaklad na stole."""
        if self.is_valid(bet):
            self.bets += [bet]
        else:
            raise InvalidBet("Bet exceds table limit {}.".format(self.limit))

    def __iter__(self):
        return iter(self.bets[:])

    def __str__(self):
        return ', '.join(map(str, self.bets))


class Game(object):
    """Klasa reprezentuje gre w ruletke."""
    def __init__(self, wheel, table):
        self. wheel = wheel
        self.table = table

    def cycle(self, player):
        """Wykonie jednej kolejki gry.

        Kolejka składa się z umiszeczenia zakładów,
        zakrecenia kołaem i wylosowania przegordy i
        wpłaceniu wszystkich wygranych / zgarnieciu przegranych.
        """
        player.place_bets()

        selected_bin = self.wheel.next()

        for bet in self.table.bets:
            if bet.outcome in selected_bin:
                player.win(bet)
            else:
                player.lose(bet)


class Player(object):
    """Bazowa klasa gracza.

    stake: aktualny stos gracza z jakim zaczyna
    rounds_to_go: liczba rund pozostała do zakończenia
    table: stol z ktorym gracz jest powiazany
    """

    stake = None
    rounds_to_go = None

    def __init__(self, table):
        self.table = table

    def playing(self):
        raise NotImplementedError()

    def place_bets(self):
        raise NotImplementedError()

    def win(self, bet):
        return bet.win_amount()

    def lose(self, bet):
        return bet.lose_amount()


class Passenger57(Player):
    """Gracz obstawiajacy zawsze czarne."""

    black = Outcome('Black', 1)

    def __init__(self, table):
        self.table = table
        super(Passenger57).__init__(self)

    def playing(self):
        return True

    def place_bets(self):
        self.table.place_bet(Bet(1, self.black))


class Martingale(Player):

    black = Outcome('Black', 1)

    def __init__(self, table):
        self.table = table
        self.loss_count = 1
        self.bet_multiple = 2^self.loss_count

        super(Martingale).__init__(self)

    def playing(self):
        return True

    def place_bets(self):
        self.table.place_bet(Bet(self.bet_multiple, self.black))

    def win(self, bet):
        super.win(bet)
        self.loss_count = 1

    def lose(self, bet):
        super.lose(bet)
        self.loss_count += 1
