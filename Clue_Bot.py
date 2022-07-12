from copy import copy
from collections import OrderedDict
from typing import Union

culprit_cards = tuple(name.title() for name in ('White', 'Green', 'Mustard', 
                                           'Plum', 'Scarlet', 'Peacock'))
weapon_cards = tuple(name.title() for name in ('Candlestick', 'Knife', 'Rope', 
                                          'Lead Pipe', 'Revolver', 'Wrench'))
room_cards = tuple(name.title() for name in ('Ballroom', 'Billiard Room', 
                                        'Conservatory', 'Dining Room', 
                                        'Kitchen', 'Hall', 'Library', 
                                        'Lounge', 'Study'))
              
all_cards = (*culprit_cards, *weapon_cards, *room_cards)

commands = ('help', 'show')

help_command = '''
List of valid commands:

"help" - Provides uses and syntax for all valid commands.

"show" - Used to show guesses, players, or cards.
Syntax: "show players|guesses|cards"
'''

true_culprit = 'Unknown'
true_weapon = 'Unknown'
true_room = 'Unknown'

guess_list = []

card_statuses = OrderedDict()

def execute_command(command: str) -> None:
    base_command, *args = command.split(' ')
    if base_command == 'help':
        print(help_command)

    if base_command == 'show':
        if args[0] == 'guesses':
            for index, guess in enumerate(guess_list, 1):
                print(index, guess)
            print('')
        elif args[0] == 'players':
            print(f'Players: {", ".join(players)}')
        elif args[0] == 'cards':
            print_statuses()

    main_loop()


def get_input(__prompt: object) -> str:
    input_value = input(__prompt)
    if input_value.split(' ')[0] not in commands:
        return input_value
    else:
        execute_command(input_value)



def card_statuses_setup(players: list) -> None:
    for card in all_cards:
        card_statuses[card] = [*(p.player_name for p in players), 'File']


def update() -> None:
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
    def __init__(self, name: str) -> None:
        self.player_name = name
        self.guesses = []
        self.cards = set()

    def __str__(self) -> str:
        return self.player_name

    def guess(self, guess: 'Guess') -> bool | None:
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

        if supplier_index != (guesser_index + 1) % len(players):
            skipped_players = []
            next_player_index = guesser_index + 1
            while next_player_index != supplier_index:
                skipped_players.append(players[next_player_index])
                next_player_index = (next_player_index + 1) % len(players)

            for skipped_player in skipped_players:
                for card in (guess.culprit, guess.weapon, guess.room):
                    if skipped_player.player_name in card_statuses[card]:
                        card_statuses[card].remove(skipped_player.player_name)

        guess_list.append(guess)
        update()


class Guess:
    def __init__(self, 
                 guesser: 'Player', culprit: str, weapon: str, room: str, 
                 supplier: 'Player', card_shown: str = 'Unknown') -> None:
        self.guesser = guesser
        self.culprit = culprit
        self.weapon = weapon
        self.room = room
        self.supplier = supplier
        self.card_shown = card_shown or 'Unknown'

        if self.card_shown != 'Unknown':
            card_statuses[card_shown] = list()
            card_statuses[card_shown].append(self.supplier.player_name)
    
    def __str__(self) -> str:
        c, w, r, g, cs, s = (self.culprit, self.weapon, self.room, 
                             self.guesser, self.card_shown, self.supplier)
        return f'{c}, {w}, {r}, guessed by {g}, card {cs} supplied by {s}'


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
    def update(cls) -> dict:
        for (card, status) in card_statuses.items():
            if len(status) == 1 and status[0] != 'File':
                if card in culprit_cards and card in cls.possible_culprits:
                    cls.possible_culprits.remove(card)

                elif card in weapon_cards and card in cls.possible_weapons:
                    cls.possible_weapons.remove(card)

                elif card in cls.possible_rooms:
                    cls.possible_rooms.remove(card)

            if len(status) == 1 and status[0] == 'File':
                global true_culprit, true_weapon, true_room
                if card in culprit_cards:
                    true_culprit = card
                if card in weapon_cards:
                    true_weapon = card
                if card in room_cards:
                    true_room = card

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


def is_card(card: str) -> bool:
    if card in all_cards:
        return True
    return False


def is_player(p: Union[str, Player]) -> bool:
    if p in (*(p.player_name for p in players), *(p for p in players)):
        return True
    return False


def setup() -> list:
    players = []
    global card_statuses

    for p in range(int(get_input('Number of Players: '))):
        p = get_input('Add Player: ')
        player_obj = Player(p)
        if p not in globals().keys():
            globals()[p] = player_obj
        else:
            raise Exception('Player name cannot be the same '
                           f'as a global variable. ({p}, {globals()[p]})')
        players.append(player_obj)

    card_statuses_setup(players)

    c = get_input('Your First Card: ').title()
    while c:
        if is_card(c):
            players[0].cards.add(c)
        else:
            print(f'{c} is not a recognized card. Ensure correct spelling.')
        c = get_input('Your Next Card: ').title()

    for c in all_cards:
        if c not in players[0].cards:
            card_statuses[c].remove(players[0].player_name)

    return players


def get_guess() -> OrderedDict | str:
    guesser = get_input('Guesser: ')
    if not is_player(guesser):
        return 'Not a valid player.'
    guesser = globals()[guesser] # guesser is now a Player object

    g_cards = [c.title() for c in get_input('Culprit, Weapon, Room: ').split(', ')]
    if len(g_cards) != 3:
        return 'Must provide three cards.'

    c, w, r = g_cards
    if c not in culprit_cards:
        return f'"{c}" is not a recognized culprit.'
    if w not in weapon_cards:
        return f'"{w}" is not a recognized weapon.'
    if r not in room_cards:
        return f'"{r}" is not a recognized room.'
    
    supp = get_input('Supplier or "None": ')
    if not is_player(supp) and supp != 'None':
        return 'Not a valid player.'
    elif supp != 'None':
        supp = globals()[supp]
    else:
        supp = None

    card_shown = get_input('Card Shown: ').title() or None
    if card_shown is not None and not is_card(card_shown):
        return f'{card_shown} is not a recognized card.'

    new_guess = Guess(guesser, *g_cards, supp, card_shown)

    guesser.guess(new_guess)
    return card_statuses


def print_statuses() -> None:
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


def main() -> None:
    global players
    players = setup()
    print('\n')
    main_loop()


def main_loop():
    run = True
    while run:
        guess_return_value = get_guess()
        if type(guess_return_value) == OrderedDict:
            print_statuses()
            print('File Contents:\n'
                 f'Culprit: {true_culprit}\n'
                 f'Weapon: {true_weapon}\n'
                 f'Room: {true_room}')
        else:
            print(guess_return_value)
        print('')


if __name__ == '__main__':
    main()
