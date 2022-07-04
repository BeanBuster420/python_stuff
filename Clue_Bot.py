from pprint import pprint
from copy import copy

culprit_cards = ('White', 'Green', 'Mustard', 'Plum', 'Scarlet', 'Peacock')
weapon_cards = ('Candlestick', 'Knife', 'Rope', 
                'Lead Pipe', 'Revolver', 'Wrench')
room_cards = ('Ballroom', 'Billiard Room', 'Conservatory', 'Dining Room', 
              'Kitchen', 'Hall', 'Library', 'Lounge', 'Study')

guess_list = []

card_statuses = dict()

def card_statuses_setup(players):
    for card in (*culprit_cards, *weapon_cards, *room_cards):
        card_statuses[card] = [*(p.player_name for p in players), 'File']


def update():
    for player in players:
        for card in player.cards:
            card_statuses[card] = [player.player_name]
    print('Update')
    for guess in guess_list:
        if guess.card_shown == 'Unknown':
            possible_cards_shown = [guess.culprit, guess.weapon, guess.room]
            to_be_removed = []
            guess_supplier = guess.supplier.player_name
            for possibility in possible_cards_shown:
                if guess_supplier not in card_statuses[possibility]:
                    to_be_removed.append(possibility)
            for possibility in to_be_removed:
                possible_cards_shown.remove(possibility)
            if len(possible_cards_shown) == 1:
                card_owner = guess.supplier.player_name
                card_statuses[possible_cards_shown[0]] = [card_owner]
            if len(possible_cards_shown) == 0:
                guess_list.remove(guess)
                return 'Invalid guess.'


    Case_File.update()


class Player:
    def __init__(self, name):
        self.player_name = name
        self.guesses = []
        self.cards = []

    def guess(self, guess):
        self.guesses.append(guess)

        supplier_index = players.index(guess.supplier)
        guesser_index = players.index(self)

        if supplier_index != (guesser_index+1 % len(players)):
            skipped_players = players[slice((guesser_index + 1), 
                                            supplier_index or len(players))]
            for skipped_player in skipped_players:
                for card in (guess.culprit, guess.weapon, guess.room):
                    if skipped_player.player_name in card_statuses[card]:
                        card_statuses[card].remove(skipped_player.player_name)

        guess_list.append(guess)
        if update() == 'Invalid guess.':
            return 'Invalid guess.'


class Guess:
    def __init__(self, culprit, weapon, room, supplier, card_shown='Unknown'):
        self.culprit = culprit
        self.weapon = weapon
        self.room = room
        self.supplier = supplier
        self.card_shown = card_shown or 'Unknown'

        if self.card_shown != 'Unknown':
            card_statuses[card_shown] = list()
            card_statuses[card_shown].append(self.supplier.player_name)


class File:
    def __init__(self):
        self.possible_culprits = list(culprit_cards)
        self.possible_weapons = list(weapon_cards)
        self.possible_rooms = list(room_cards)
        self.contents = {
            'culprit': copy(culprit_cards),
            'weapon': copy(weapon_cards),
            'room': copy(room_cards)
        }

    def update(self):
        for (card, status) in card_statuses.items():
            if status != 'Unknown':
                if card in culprit_cards and card in self.possible_culprits:
                    self.possible_culprits.remove(card)

                elif card in weapon_cards and card in self.possible_weapons:
                    self.possible_weapons.remove(card)

                elif card in self.possible_rooms:
                    self.possible_rooms.remove(card)

        if len(self.possible_culprits) == 1:
            self.contents['culprit'] = self.possible_culprits[0]
            card_statuses[self.possible_culprits[0]] = ['File']

        if len(self.possible_weapons) == 1:
            self.contents['weapon'] = self.possible_weapons[0]
            card_statuses[self.possible_weapons[0]] = ['File']

        if len(self.possible_rooms) == 1:
            self.contents['room'] = self.possible_rooms[0]
            card_statuses[self.possible_rooms[0]] = ['File']

        return self.contents


def is_card(card):
    if card in (*culprit_cards, *weapon_cards, *room_cards):
        return True
    return False

def is_player(p):
    if p in (p.player_name for p in players):
        return True
    return False


def setup():
    Case_File = File()
    players = []

    for p in range(int(input('Number of Players: '))):
        p = input('Add Player: ')
        player_obj = Player(p)
        if p not in globals().keys():
            globals()[p] = player_obj
        else:
            raise Exception(f'Player name cannot be the same'
                            f' as a global variable. ({p})')
        players.append(player_obj)

    card_statuses_setup(players)

    c = input('Your First Card: ')
    while c:
        if is_card(c):
            players[0].cards.append(c)
        else:
            print(f'{c} is not a recognized card. Ensure correct spelling.')
        c = input('Your Next Card: ')

    return Case_File, players


def get_guess():
    guesser = input('Guesser: ')
    if not is_player(guesser):
        return 'Not a valid player.'
    guesser = globals()[guesser]

    g_cards = [c for c in input('Culprit, Weapon, Room: ').split(', ')]
    if len(g_cards) != 3:
        return 'Must provide three cards.'

    c, w, r = g_cards
    if c not in culprit_cards:
        return f'"{c}" is not a recognized culprit.'
    if w not in weapon_cards:
        return f'"{w}" is not a recognized weapon.'
    if r not in room_cards:
        return f'"{r}" is not a recognized room.'
    
    supp = input('Supplier: ')
    if not is_player(supp):
        return 'Not a valid player.'
    supp = globals()[supp]

    card_shown = input('Card Shown: ') or None
    if card_shown is not None and not is_card(card_shown):
        return f'{card_shown} is not a recognized card.'

    new_guess = Guess(*g_cards, 
                      supp, 
                      card_shown)

    guesser.guess(new_guess)
    return card_statuses


def main():
    run = True
    global Case_File, players
    Case_File, players = setup()
    print('\n')
    while run:
        g = get_guess()
        if type(g) == dict:
            pprint(g)
        else:
            print(g)
        print('')


if __name__ == '__main__':
    main()