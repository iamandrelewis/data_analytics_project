import random

def card_deck():
    card_value = ['Ace','2','3','4','5','6','7','8','9','10','J','Q','K']
    card_type = ['Hearts','Spades','Clubs','Diamonds']
    deck = []
    for i in card_type:
        for j in card_value:
            deck.append(j + ' of ' + i)
    return deck

def card_value(card):
    if card.startswith('10'):
        return 10
    first_char = card[0]
    if first_char in ('J','Q','K'):
        return 10
    elif first_char in ('2','3','4','5','6','7','8','9'):
        return int(first_char)
    elif first_char == 'A':
        print("\n" + card)
        num = input("Do you want this to be 1 or 11?\n> ")
        while num not in ('1', '11'):
            num = input("Do you want this to be 1 or 11?\n> ")
        return int(num)

def new_card(deck):
    return deck[random.randint(0, len(deck)-1)]

def remove_card(deck, card):
    deck.remove(card)

play_again = ''
while play_again.upper() != 'EXIT':
    new_deck = card_deck()
    card1 = new_card(new_deck)
    remove_card(new_deck, card1)
    card2 = new_card(new_deck)
    remove_card(new_deck, card2)
    print("\n\n\n\n" + card1 + " and " + card2)
    valu1 = card_value(card1)
    valu2 = card_value(card2)
    total = valu1 + valu2
    print("With a total of " + str(total))

    dealer_card1 = new_card(new_deck)
    remove_card(new_deck, dealer_card1)
    dealer_card2 = new_card(new_deck)
    remove_card(new_deck, dealer_card2)
    dealer_value1 = card_value(dealer_card1)
    dealer_value2 = card_value(dealer_card2)
    dealer_total = dealer_value1 + dealer_value2
    print('\nThe Dealer smiles as he looks at you and\n deals one card up and one card face down')
    print("First a " + dealer_card1 + " and face down card.")

    if total == 21:
        print("Blackjack!")
    else:
        while total < 21:
            answer = input("Would you like to hit or stand?\n> ")
            if answer.lower() == 'hit':
                more_card = new_card(new_deck)
                remove_card(new_deck, more_card)
                more_value = card_value(more_card)
                total += more_value
                print(more_card + " for a new total of " + str(total))
                if total > 21:
                    print("You LOSE!")
                    play_again = input("Would you like to continue? EXIT to leave\n")
                    break
            elif answer.lower() == 'stand':
                break

    if total > 21:
        continue

    print("\nDealer reveals the face-down card: " + dealer_card2)
    print("Dealer's total is " + str(dealer_total))
    while dealer_total < 17 and dealer_total <= 21:
        dealer_more = new_card(new_deck)
        remove_card(new_deck, dealer_more)
        more_dealer_value = card_value(dealer_more)
        dealer_total += more_dealer_value
        print("Dealer draws " + dealer_more + ". Total: " + str(dealer_total))
        if dealer_total > 21:
            print("Dealer Bust! You win!")
            break

    if dealer_total > 21:
        pass
    elif dealer_total > total:
        print("Dealer wins with " + str(dealer_total) + "!")
    elif dealer_total < total:
        print("You win with " + str(total) + "!")
    else:
        print("It's a tie!")

    play_again = input("\nWould you like to continue? EXIT to leave\n")
