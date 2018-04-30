import unittest
from casino_simulator.roulette import Outcome, Bin, Wheel, BinBuilder, Bet, NonRandom, Table, Game
from casino_simulator.roulette import Player, Passenger57, Martingale
from casino_simulator.exceptions import InvalidBet


# OUTCOME ============================================================
class TestOutcome(unittest.TestCase):

    def test_init(self):
        o1 = Outcome('x', 2)
        self.assertEqual(type(o1), Outcome)

    def test_win_amount(self):
        outcome1_2 = Outcome('col1', 2)
        self.assertEqual(outcome1_2.win_amount(2), 4)
        self.assertEqual(outcome1_2.win_amount(7), 14)

    def test_eq(self):
        o1 = Outcome('Red', 1)
        o2 = Outcome('Red', 1)

        self.assertEqual(o1, o2)

    def test_neq(self):
        o1 = Outcome('Street123', 11)
        o2 = Outcome('1', 35)

        self.assertNotEqual(o1, o2)

    def test_hash(self):
        o1 = Outcome('Red', 1)
        o2 = Outcome('Red', 1)

        self.assertEqual(o1.__hash__(), o2.__hash__())

    def test_str(self):
        o = Outcome('Street456', 11)

        self.assertEqual(str(o), 'Street456 (11:1)')

    def test_repr(self):
        o = Outcome('Street456', 11)

        self.assertEqual(repr(o), "Outcome('Street456', 11)")


# BIN =================================================================
class TestBin(unittest.TestCase):

    def setUp(self):
        self.o1 = Outcome('00-0-1-2-3', 6)
        self.o2 = Outcome('00', 36)
        self.o3 = Outcome('0', 0)

    def test_assign(self):
        zero = Bin({self.o1, self.o3})
        zerozero = Bin({self.o1, self.o2})

        self.assertEqual(len(zero), 2)
        self.assertEqual(len(zerozero), 2)

    def test_add_outcome(self):
        o1 = Outcome('0', 0)
        o2 = Outcome('00', 36)
        bin0 = Bin()

        bin0.add(o1)
        self.assertEqual(bin0.outcomes, frozenset({o1}))

        bin0.add(o2)
        self.assertEqual(bin0.outcomes, frozenset({o1, o2}))

        bin0_m = Bin([o1, o2])
        self.assertEqual(bin0_m.outcomes, frozenset({o1, o2}))


# WHEEL ===============================================================
# NON-RANODM
class TestNonRandom(unittest.TestCase):
    def test_nonrandom(self):
        choices = ['a', 'b', 'c']

        nrnd = NonRandom()

        nrnd.set_seed(0)
        assert nrnd.choice(choices) == 'a'
        assert nrnd.choice(choices) == 'a'

        nrnd.set_seed(2)
        assert nrnd.choice(choices) == 'c'


class TestWheel(unittest.TestCase):

    def setUp(self):
        self.o1 = Outcome('00-0-1-2-3', 6)
        self.o2 = Outcome('00', 36)
        self.o3 = Outcome('0', 0)
        self.o4 = Outcome('bla', 12)
        self.o5 = Outcome('ccc', 15)

        self.bin0 = Bin([self.o1, self.o2, self.o3])
        self.bin1 = Bin([self.o4, self.o5])

        self.wheel = Wheel(rng=NonRandom())
        self.wheel.add_outcome(0, self.o1)
        self.wheel.add_outcome(0, self.o2)
        self.wheel.add_outcome(0, self.o3)

        self.wheel.add_outcome(1, self.o4)
        self.wheel.add_outcome(1, self.o5)

        self.wheel.add_outcome(21, self.o5)

    def test_adding_bins(self):
        self.wheel.add_outcome(12, self.o1)
        self.wheel.add_outcome(12, self.o2)
        self.assertEqual(self.wheel.get_bin(12), Bin([self.o1, self.o2]))

    def test_pseudo_random_select(self):
        self.wheel.rng.set_seed(0)
        self.assertEqual(self.wheel.next(), self.bin0)

        self.wheel.rng.set_seed(1)
        self.assertEqual(self.wheel.next(), self.bin1)

    def test_get_outcome(self):
        self.assertEqual(len(self.wheel.all_outcomes), 5)
        self.assertEqual(self.wheel.get_outcome('bla'), self.o4)

# BINBUILDER ========================================================
class TestBinBuilder(unittest.TestCase):

    def test_straight_bets(self):
        wheel = Wheel()
        BinBuilder().straight_bets(wheel)

        self.assertEqual(wheel.get_bin(0), Bin([Outcome('0', 35)]))
        self.assertEqual(wheel.get_bin(37), Bin([Outcome('00', 35)]))

    def test_split_bets(self):
        wheel = Wheel()
        BinBuilder().split_bets(wheel)

        self.assertEqual(wheel.get_bin(1), Bin([Outcome('Split 1-2', 17),
                                                Outcome('Split 1-4', 17)]))

        self.assertEqual(wheel.get_bin(5),
                         Bin([Outcome('Split 4-5', 17),
                              Outcome('Split 5-6', 17),
                              Outcome('Split 2-5', 17),
                              Outcome('Split 5-8', 17)]))

        self.assertEqual(wheel.get_bin(15), Bin([Outcome('Split 12-15', 17),
                                                 Outcome('Split 14-15', 17),
                                                 Outcome('Split 15-18', 17)]))

        self.assertEqual(wheel.get_bin(36), Bin([Outcome('Split 35-36', 17),
                                                 Outcome('Split 33-36', 17)]))

    def test_street_bets(self):
        wheel = Wheel()
        BinBuilder().street_bets(wheel)

        self.assertEqual(wheel.get_bin(1), Bin([Outcome('Street 1-2-3', 11)]))
        self.assertEqual(wheel.get_bin(36), Bin([Outcome('Street 34-35-36', 11)]))

    def test_corner_bets(self):
        wheel = Wheel()
        BinBuilder().corner_bets(wheel)

        self.assertEqual(wheel.get_bin(1), Bin([Outcome('Corner 1-2-4-5', 8)]))

        self.assertEqual(wheel.get_bin(8), Bin([Outcome('Corner 4-5-7-8', 8),
                                                Outcome('Corner 5-6-8-9', 8),
                                                Outcome('Corner 7-8-10-11', 8),
                                                Outcome('Corner 8-9-11-12', 8)]))

        self.assertEqual(wheel.get_bin(35), Bin([Outcome('Corner 31-32-34-35', 8),
                                                 Outcome('Corner 32-33-35-36', 8)]))

    def test_line_bets(self):
        wheel = Wheel()
        BinBuilder().line_bets(wheel)

        self.assertEqual(wheel.get_bin(1), Bin([Outcome('Line 1-2-3-4-5-6', 5)]))

        self.assertEqual(wheel.get_bin(10), Bin([Outcome('Line 7-8-9-10-11-12', 5),
                                                 Outcome('Line 10-11-12-13-14-15', 5)]))

        self.assertEqual(wheel.get_bin(36), Bin([Outcome('Line 31-32-33-34-35-36', 5)]))

    def test_dozen_bets(self):
        wheel = Wheel()
        BinBuilder().dozen_bets(wheel)

        self.assertEqual(wheel.get_bin(1), Bin([Outcome('Dozen 1-12', 2)]))
        self.assertEqual(wheel.get_bin(13), Bin([Outcome('Dozen 13-24', 2)]))
        self.assertEqual(wheel.get_bin(25), Bin([Outcome('Dozen 25-36', 2)]))
        self.assertEqual(wheel.get_bin(36), Bin([Outcome('Dozen 25-36', 2)]))

    def test_column_bets(self):
        wheel = Wheel()
        BinBuilder().column_bets(wheel)

        self.assertEqual(wheel.get_bin(1), Bin([Outcome('Column 1', 2)]))
        self.assertEqual(wheel.get_bin(23), Bin([Outcome('Column 2', 2)]))
        self.assertEqual(wheel.get_bin(36), Bin([Outcome('Column 3', 2)]))

    def test_even_money_bets(self):
        wheel = Wheel()
        BinBuilder().even_money_bets(wheel)

        self.assertEqual(wheel.get_bin(1), Bin([Outcome('Red', 1),
                                                Outcome('Low', 1),
                                                Outcome('Odd', 1)]))
        self.assertEqual(wheel.get_bin(18), Bin([Outcome('Red', 1),
                                                 Outcome('Low', 1),
                                                 Outcome('Even', 1)]))
        self.assertEqual(wheel.get_bin(28), Bin([Outcome('Black', 1),
                                                 Outcome('High', 1),
                                                 Outcome('Even', 1)]))

    def test_five_bet(self):
        wheel = Wheel()
        BinBuilder().five_bet(wheel)

        self.assertEqual(wheel.get_bin(0), Bin([Outcome('00-0-1-2-3', 6)]))
        self.assertEqual(wheel.get_bin(37), Bin([Outcome('00-0-1-2-3', 6)]))
        self.assertEqual(wheel.get_bin(3), Bin([Outcome('00-0-1-2-3', 6)]))
        self.assertEqual(wheel.get_bin(4), Bin([]))


# BET =================================================================
class TestBet(unittest.TestCase):
    def setUp(self):
        self.red_oc = Outcome('RED', 1)
        self.split_oc = Outcome('Split 1-2', 17)

        self.red_bet = Bet(5, self.red_oc)
        self.split_bet = Bet(30, self.split_oc)

    def test_win_amount(self):
        self.assertEqual(self.red_bet.win_amount(), 5+1*5)
        self.assertEqual(self.split_bet.win_amount(), 30+30*17)

    def test_lose_amount(self):
        self.assertEqual(self.red_bet.lose_amount(), 5)
        self.assertEqual(self.split_bet.lose_amount(), 30)


# TABLE ===============================================================
class TestTable(unittest.TestCase):
    def setUp(self):
        self.t = Table(limit=100)

        oc = Outcome('Red', 1)

        self.b1 = Bet(15, oc)
        self.b2 = Bet(30, oc)
        self.b3 = Bet(100, oc)
        self.b4 = Bet(55, oc)

    def test_table(self):
        self.assertTrue(self.t.is_valid(self.b1))
        self.t.place_bet(self.b1)

        self.assertTrue(self.t.is_valid(self.b2))
        self.t.place_bet(self.b2)

        self.assertFalse(self.t.is_valid(self.b3))
        with self.assertRaises(InvalidBet):
            self.t.place_bet(self.b3)

        self.assertTrue(self.t.is_valid(self.b4))
        self.t.place_bet(self.b4)

        self.assertEqual(len(self.t.bets), 3)
        self.assertEqual(sum([b.amount for b in self.t.bets]), 100)


# GAME ================================================================
class TestGame(unittest.TestCase):
    def setUp(self):
        self.wheel = Wheel()
        binb = BinBuilder()
        binb.build_bins(self.wheel)

        self.table = Table(limit=100)

        self.player = Passenger57(self.table)

    def test_game_init(self):
        game = Game(wheel=self.wheel, table=self.table)

    def test_game_cycle(self):
        game = Game(wheel=self.wheel, table=self.table)

        for _ in range(5):
            game.cycle(self.player)


# PLAYERS =============================================================
class TestPassenger57(unittest.TestCase):
    def setUp(self):
        self.wheel = Wheel()
        BinBuilder().build_bins(self.wheel)
        self.table = Table(limit=100)

        self.b_bet = Bet(1, self.wheel.get_outcome('Black'))

        self.player = Passenger57(table=self.table)

    def test_init_player(self):
        self.assertEqual(self.player.black, self.b_bet.outcome)

    def test_palce_bet(self):
        self.player.place_bets()

        assert len(self.table.bets) == 1
        assert self.table.bets[0].amount == 1
        self.assertEqual(self.table.bets[0].outcome, self.b_bet.outcome)

    def test_win(self):
        self.assertEqual(self.player.win(self.b_bet), 2)

    def test_lose(self):
        self.assertEqual(self.player.lose(self.b_bet), 1)


class TestMartingale(unittest.TestCase):
    def setUp(self):
        self.wheel = Wheel(rng=NonRandom())
        BinBuilder().build_bins(self.wheel)
        self.table = Table(limit=1000)

    def test_init_player(self):
        self.player = Martingale(table=self.table)

    def test_place_bet(self):
        pass
