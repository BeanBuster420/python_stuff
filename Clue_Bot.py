from copy import copy
from collections import OrderedDict

culprit_cards = ('White', 'Green', 'Mustard', 'Plum', 'Scarlet', 'Peacock')
weapon_cards = ('Candlestick', 'Knife', 'Rope', 
                'Lead Pipe', 'Revolver', 'Wrench')
room_cards = ('Ballroom', 'Billiard Room', 'Conservatory', 'Dining Room', 
              'Kitchen', 'Hall', 'Library', 'Lounge', 'Study')

true_culprit = 'Unknown'
true_weapon = 'Unknown'
true_room = 'Unknown'

guess_list = []

card_statuses = OrderedDict()

def card_statuses_setup(players):
    for card in (*culprit_cards, *weapon_cards, *room_cards):
        card_statuses[card] = [*(p.player_name for p in players), 'File']


def update():
    for player in players:
        for card in player.cards:
            card_statuses[card] = [player.player_name]

    for guess in guess_list:
        if guess.card_shown == 'Unknown' and guess.supplier is not None:
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
                raise Exception('Invalid guess.')


    File.update()


class Player:
    def __init__(self, name):
        self.player_name = name
        self.guesses = []
        self.cards = set()

    def guess(self, guess):
        self.guesses.append(guess)

        if guess.supplier == None:
            c, w, r = guess.culprit, guess.weapon, guess.room
            for card in (c, w, r):
                if self.player_name not in card_statuses[card]:
                    card_statuses[card] = ['File']
                    if card is c:
                        global true_culprit
                        true_culprit = card
                        File.update()
                    if card is w:
                        global true_weapon
                        true_weapon = card
                        File.update()
                    if card is r:
                        global true_room
                        true_room = card
                        File.update()
            guess_list.append(guess)
            update()
            return True

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
        update()


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
    possible_culprits = list(culprit_cards)
    possible_weapons = list(weapon_cards)
    possible_rooms = list(room_cards)
    contents = {
        'culprit': copy(culprit_cards),
        'weapon': copy(weapon_cards),
        'room': copy(room_cards)
    }

    @classmethod
    def update(cls):
        for (card, status) in card_statuses.items():
            if status != 'Unknown':
                if card in culprit_cards and card in cls.possible_culprits:
                    cls.possible_culprits.remove(card)

                elif card in weapon_cards and card in cls.possible_weapons:
                    cls.possible_weapons.remove(card)

                elif card in cls.possible_rooms:
                    cls.possible_rooms.remove(card)

        if len(cls.possible_culprits) == 1:
            true_culprit = cls.possible_culprits[0]
            cls.contents['culprit'] = true_culprit
            card_statuses[cls.possible_culprits[0]] = ['File']
            

        if len(cls.possible_weapons) == 1:
            true_weapon = cls.possible_weapons[0]
            cls.contents['weapon'] = true_weapon
            card_statuses[cls.possible_weapons[0]] = ['File']

        if len(cls.possible_rooms) == 1:
            true_room = cls.possible_rooms[0]
            cls.contents['room'] = true_room
            card_statuses[cls.possible_rooms[0]] = ['File']

        return cls.contents


def is_card(card):
    if card in (*culprit_cards, *weapon_cards, *room_cards):
        return True
    return False


def is_player(p):
    if p in (*(p.player_name for p in players), *(p for p in players)):
        return True
    return False


def setup():
    players = []

    for p in range(int(input('Number of Players: '))):
        p = input('Add Player: ')
        player_obj = Player(p)
        if p not in globals().keys():
            globals()[p] = player_obj
        else:
            raise Exception(f'Player name cannot be the same '
                            f'as a global variable. ({p}, {globals()[p]})')
        players.append(player_obj)

    card_statuses_setup(players)

    c = input('Your First Card: ')
    while c:
        if is_card(c):
            players[0].cards.add(c)
        else:
            print(f'{c} is not a recognized card. Ensure correct spelling.')
        c = input('Your Next Card: ')

    return players


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
    
    supp = input('Supplier or "None": ')
    if not is_player(supp) and supp != 'None':
        return 'Not a valid player.'
    elif supp != 'None':
        supp = globals()[supp]
    else:
        supp = None

    card_shown = input('Card Shown: ') or None
    if card_shown is not None and not is_card(card_shown):
        return f'{card_shown} is not a recognized card.'

    new_guess = Guess(*g_cards, supp, card_shown)

    guesser.guess(new_guess)
    return card_statuses


def print_statuses():
    print('\nCulprits:')
    for card in (culprit_cards):
        print(f'{card}: {card_statuses[card]}')

    print('\nWeapons:')
    for card in (weapon_cards):
        print(f'{card}: {card_statuses[card]}')

    print('\nRooms:')
    for card in (room_cards):
        print(f'{card}: {card_statuses[card]}')

    print('')


def main():
    run = True
    global players
    players = setup()
    print('\n')
    while run:
        guess_return_value = get_guess()
        if type(guess_return_value) == OrderedDict:
            print_statuses()
            print(f'File Contents:\n'
                  f'Culprit: {true_culprit}\n'
                  f'Weapon: {true_weapon}\n'
                  f'Room: {true_room}')
        else:
            print(guess_return_value)
        print('')


if __name__ == '__main__':
    main()
