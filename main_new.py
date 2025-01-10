import random
import tkinter as tk
from tkinter import messagebox
import time

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

def calculate_hand(hand: list[str], player_bool: bool = True) -> int:
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
    print(f"calculate_hand -> hand: {hand}, total: {total}")
    if total == 21 and len(hand) == 2 and player_bool:
        print('BLACKJACK!')
        win_bet(bj=True)
    return total

def update_display():
    print(f"update_display -> player_hand: {player_hand}, house_hand: {house_hand}, bankroll: {bankroll}, current_bet: {current_bet}")

    if show_player_hand:
        player_label.config(text=f"Player: {player_hand if player_hand else '[]'} | Total: {calculate_hand(player_hand) if player_hand else 0}")
        house_label.config(text=f"House: [{house_hand[0]}, ?]" if house_hand else "House: []")
    bankroll_label.config(text=f"Bankroll: ${bankroll}")
    bet_label.config(text=f"Current Bet: ${current_bet}")

def hit():
    global player_hand, doubled_bet
    doubled_bet = False
    new_card = DECK_COPY.pop(0)
    player_hand.append(new_card)
    print(f"hit -> player_hand: {player_hand}")
    diable_double()
    update_display()

    if calculate_hand(player_hand) > 21:
        print("hit -> BUST")
        messagebox.showinfo("Game Over", "BUST! You lose.")
        lose_bet()
        reset_game()

def reveal_house_hand():
    print(f"reveal_house_hand -> house_hand: {house_hand}")
    house_label.config(text=f"House: {house_hand} | Total: {calculate_hand(house_hand, player_bool = False)}")
    root.update()

def stand(double: bool = False):
    global house_hand, bankroll
    print("stand -> Revealing house hand")
    reveal_house_hand()

    while calculate_hand(house_hand, player_bool = False) < 17:
        time.sleep(1)
        new_card = DECK_COPY.pop(0)
        house_hand.append(new_card)
        print(f"stand -> house_hand after hit: {house_hand}")
        reveal_house_hand()

    player_total = calculate_hand(player_hand)
    house_total = calculate_hand(house_hand, player_bool = False)

    print(f"stand -> player_total: {player_total}, house_total: {house_total}")
    if house_total > 21:
        print("stand -> House busts, player wins")
        messagebox.showinfo("Result", "House busts! You win!")
        win_bet()
    elif house_total > player_total:
        print("stand -> House wins")
        messagebox.showinfo("Result", "House wins!")
        lose_bet(double)
    elif house_total < player_total:
        print("stand -> Player wins")
        messagebox.showinfo("Result", "You win!")
        win_bet()
    else:
        print("stand -> It's a tie")
        messagebox.showinfo("Result", "It's a tie!")
        bankroll += current_bet
    reset_game()

def double():
    global bankroll, doubled_bet, player_hand, current_bet
    if bankroll < current_bet:
        print("double -> Not enough funds to double")
        messagebox.showinfo("Error", "Not enough funds to double the bet.")
        return
    doubled_bet = True
    bankroll -= current_bet
    current_bet *= 2
    new_card = DECK_COPY.pop(0)
    player_hand.append(new_card)
    print(f"double -> player_hand: {player_hand}, current_bet: {current_bet}")
    messagebox.showinfo("Double", f"You doubled the bet and drew: {new_card}")
    update_display()

    if calculate_hand(player_hand) > 21:
        print("double -> BUST")
        messagebox.showinfo("Game Over", "BUST! You lose.")
        lose_bet(double=True)
        reset_game()
    else:
        stand(double=True)

def win_bet(bj: bool = False):
    global bankroll
    payout = current_bet
    if bj:
        payout = current_bet * 1.5
    bankroll += current_bet + payout

    print(f"win_bet -> bankroll: {bankroll}")
    update_display()
    if bj:
        reset_game()

def lose_bet(double: bool = False):
    global bankroll 
    print(f"lose_bet -> bankroll: {bankroll}")
    update_display()

def reset_game():
    global player_hand, house_hand, DECK_COPY, bankroll, doubled_bet, current_bet
    doubled_bet = False
    current_bet = initial_bet
    enable_bet_buttons()
    diable_double()
    diable_actions()
    player_label.config(text="")
    house_label.config(text="")
    bet_label.config(text=f"Current Bet: ${current_bet}")
    bankroll_label.config(text=f"Bankroll: ${bankroll}")
    print("reset_game -> Game reset")

def play_game():
    global player_hand, house_hand, DECK_COPY, bankroll, current_bet
    if bankroll < current_bet:
        print("play_game -> Not enough bankroll to play")
        messagebox.showinfo("Game Over", "You are out of money! Game Over.")
        root.destroy()
        return

    bankroll -= current_bet
    DECK_COPY = DECK.copy()
    random.shuffle(DECK_COPY)
    player_hand = [DECK_COPY.pop(0), DECK_COPY.pop(0)]
    house_hand = [DECK_COPY.pop(0), DECK_COPY.pop(0)]
    print(f"play_game -> player_hand: {player_hand}, house_hand: {house_hand}")
    disable_bet_buttons()
    enable_actions()
    update_display()

def set_bet(amount):
    global current_bet, bankroll
    if current_bet + amount > bankroll:
        print("set_bet -> Not enough funds for this bet")
        messagebox.showinfo("Error", "Not enough funds for this bet.")
        return
    current_bet += amount
    print(f"set_bet -> current_bet: {current_bet}")
    update_display()

def disable_bet_buttons():
    global show_player_hand
    bet_10_button.config(state=tk.DISABLED)
    bet_20_button.config(state=tk.DISABLED)
    bet_50_button.config(state=tk.DISABLED)
    play_button.config(state=tk.DISABLED)
    print("disable_bet_buttons -> Bet buttons disabled")
    show_player_hand = True

def diable_double():
    double_button.config(state=tk.DISABLED)

def diable_actions():
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)

def enable_actions():
    hit_button.config(state=tk.ACTIVE)
    stand_button.config(state=tk.ACTIVE)
    double_button.config(state=tk.ACTIVE)


def enable_bet_buttons():
    global show_player_hand
    bet_10_button.config(state=tk.NORMAL)
    bet_20_button.config(state=tk.NORMAL)
    bet_50_button.config(state=tk.NORMAL)
    play_button.config(state=tk.NORMAL)
    print("enable_bet_buttons -> Bet buttons enabled")
    show_player_hand = False

DECK = [str(value)+suit for value in Values for suit in Suits]
DECK_COPY = DECK.copy()
random.shuffle(DECK_COPY)

player_hand = []
house_hand = []

bankroll = 100
doubled_bet = False
initial_bet = 10
current_bet = initial_bet

root = tk.Tk()
root.title("Blackjack Game")

bet_label = tk.Label(root, text=f"Current Bet: ${current_bet}")
bet_label.pack()

player_label = tk.Label(root, text="")
player_label.pack()

house_label = tk.Label(root, text="")
house_label.pack()

bankroll_label = tk.Label(root, text=f"Bankroll: ${bankroll}")
bankroll_label.pack()

bet_10_button = tk.Button(root, text="Bet $10", command=lambda: set_bet(10))
bet_10_button.pack()

bet_20_button = tk.Button(root, text="Bet $20", command=lambda: set_bet(20))
bet_20_button.pack()

bet_50_button = tk.Button(root, text="Bet $50", command=lambda: set_bet(50))
bet_50_button.pack()

play_button = tk.Button(root, text="Play", command=play_game)

play_button.pack()

hit_button = tk.Button(root, text="Hit", command=hit)
hit_button.pack()

stand_button = tk.Button(root, text="Stand", command=stand)
stand_button.pack()

double_button = tk.Button(root, text="Double", command=double)
double_button.pack()

reset_game()
root.mainloop()
