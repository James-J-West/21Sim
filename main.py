import random

Values = [i for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
Suits = ['H', 'D', 'C', 'S']

def get_value(card: str) -> int:
    value = card[:-1]
    if value in ['J', 'Q', 'K']:
        return 10
    elif value == 'A':
        return 11 
    else:
        return int(value)

def calculate_hand(hand: list[str]) -> int:
    total = 0
    ace_count = 0
    
    for card in hand:
        value = get_value(card)
        total += value
        if card[:-1] == 'A':
            ace_count += 1
    
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    
    return total

def print_hand(name: str, hand: list[str], reveal_all: bool = False):
    if reveal_all:
        print(f"{name} Hand: {hand} | Total: {calculate_hand(hand)}")
    else:
        print(f"{name} Hand: [{hand[0]}, ?]")

DECK = [str(value)+suit for value in Values for suit in Suits]

play_input = input("Do you want to play? (yes/no): ")
acceptable_answers = ['yes', 'no']
while play_input.lower() not in acceptable_answers:
    play_input = input("Please enter yes or no: ")

if play_input.lower() == 'yes':
    while True:
        DECK_COPY = DECK.copy()
        random.shuffle(DECK_COPY)
        hand = []
        house = []
        hand.append(DECK_COPY.pop(0))
        house.append(DECK_COPY.pop(0))
        hand.append(DECK_COPY.pop(0))
        house.append(DECK_COPY.pop(0))

        print_hand("Player", hand, reveal_all=True)
        print_hand("House", house, reveal_all=False)

        print('----------------------')

        try:
            while True:
                print(f'Your current total: {calculate_hand(hand)}')
                player_input = int(input("""\nChoose an action:
1: Hit
2: Stand
3: Split
Your choice: """))

                if player_input == 1:  # Hit
                    new_card = DECK_COPY.pop(0)
                    hand.append(new_card)
                    print(f'You drew: {new_card}')

                    hand_val = calculate_hand(hand)
                    print(f'Your hand: {hand} | Total: {hand_val}')
                    print_hand("House", house, reveal_all=False)

                    if hand_val > 21:
                        print('BUST! You lose.')
                        break  # End turn

                elif player_input == 2:  # Stand
                    print(f'You stand with a total of {calculate_hand(hand)}.')
                    print_hand("House", house, reveal_all=True)
                    while calculate_hand(house) < 17:
                        new_card = DECK_COPY.pop(0)
                        house.append(new_card)
                        print(f'House draws: {new_card}')

                    house_total = calculate_hand(house)
                    print(f'Final House Hand: {house} | Total: {house_total}')

                    if house_total > 21:
                        print('House busts! You win!')
                    elif house_total > calculate_hand(hand):
                        print('House wins!')
                    elif house_total < calculate_hand(hand):
                        print('You win!')
                    else:
                        print('It\'s a tie!')
                    break  # End turn

                elif player_input == 3:  # Split (if applicable)
                    if len(hand) == 2 and hand[0][:-1] == hand[1][:-1]:  # Check for a valid split
                        print('You chose to split. Implement split logic here.')
                        # Handle split logic
                        break  # End turn after handling split
                    else:
                        print('Invalid split option. You must have two cards of the same value to split.')

                else:
                    print('Invalid input. Please choose 1, 2, or 3.')

        except ValueError:
            print('Invalid input. Please enter a number (1, 2, or 3).')

        replay = input("Do you want to play again? (yes/no): ")
        if replay.lower() != 'yes':
            print("Thanks for playing! Goodbye!")
            break
