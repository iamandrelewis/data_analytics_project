import random

dice_art = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘")
}

def roll_dice(num_of_dice):
    dice = [random.randint(1, 6) for _ in range(num_of_dice)]
    total = sum(dice)
    for line in range(5):
        for die in dice:
            print(dice_art[die][line], end=" ")
        print()
    print(f"Total: {total}\n")
    return total

def main():
    print("🎲 Welcome to the Multiplayer Dice Game! 🎲")
    print("First to win the most rounds out of 6 is the champion. Type 'exit' anytime to quit.\n")

    # Get player names
    players = []
    while True:
        name = input("Enter player name (or type 'done' when finished): ")
        if name.lower() == 'done':
            if len(players) < 2:
                print("You need at least 2 players.")
                continue
            break
        elif name.strip() == "":
            print("Please enter a valid name.")
        else:
            players.append(name.strip())

    scores = {player: 0 for player in players}
    round_number = 1

    while round_number <= 6:
        print(f"\n🌀 Round {round_number}")
        try:
            user_input = input("How many dice should each player roll? (or type 'exit'): ")
            if user_input.lower() == 'exit':
                break
            num_of_dice = int(user_input)
        except ValueError:
            print("Please enter a valid number or 'exit'.")
            continue

        round_totals = {}
        for player in players:
            print(f"\n🎯 {player}'s turn:")
            total = roll_dice(num_of_dice)
            round_totals[player] = total

        max_score = max(round_totals.values())
        winners = [p for p, score in round_totals.items() if score == max_score]

        if len(winners) == 1:
            print(f"🏆 {winners[0]} wins this round!\n")
            scores[winners[0]] += 1
        else:
            print(f"🤝 It's a tie between {', '.join(winners)}!\n")
            for w in winners:
                scores[w] += 1

        print("📊 Scoreboard:")
        for player, score in scores.items():
            print(f"{player}: {score} round wins")
        
        round_number += 1

    print("\n🏁 Final Results:")
    for player, score in scores.items():
        print(f"{player}: {score} round wins")

    max_final_score = max(scores.values())
    final_winners = [p for p, score in scores.items() if score == max_final_score]

    if len(final_winners) == 1:
        print(f"\n🎉 {final_winners[0]} is the ultimate champion!")
    else:
        print(f"\n🔥 It's a draw between: {', '.join(final_winners)}!")

if __name__ == "__main__":
    main()