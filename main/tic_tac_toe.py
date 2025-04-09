def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(all(cell != " " for cell in row) for row in board)

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    turn = 0
    
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        player = players[turn % 2]
        print(f"Player {player}, enter your move (row and column: 1-3 each, separated by space): ")
        
        try:
            row, col = map(int, input().split())
            row, col = row - 1, col - 1  # Convert to 0-based index

            if board[row][col] != " ":
                print("Cell already occupied! Choose another.")
                continue

            board[row][col] = player
            print_board(board)

            if check_winner(board, player):
                print(f"Player {player} wins!")
                break

            if is_full(board):
                print("It's a draw!")
                break

            turn += 1

        except (ValueError, IndexError):
            print("Invalid input! Enter row and column numbers between 1 and 3.")

if __name__ == "_main_":
    tic_tac_toe()