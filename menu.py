import os 
from games.snakes import *

def menu():
    os.system('cls')
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("\t\tWELCOME TO GROUP #3's ARCADE")
    print("---------------------------------------------------------\n")
    print(" [1]. Snakes and Ladders by Andre Lewis\t\t(2108069)")
    print(" [2]. Dice by Jerome McKenzie\t\t\t(#######)")
    print(" [3]. Tic Tac Toe by Chris-Anthony Williams\t(#######)")
    print(" [4]. Black Jack by Matthew Thomas\t\t(#######)\n")
    print("---------------------------------------------------------")
    print(" [0]. Exit")
    print("=========================================================")
    option = input("\nSelect an option: ")
    match option:
        case '1':
            Game = game.start(self=game)
            menu()
        case '2':
            pass
        case '3':
            tic_tac_toe()
        case '4':
            pass
        case '0':
            pass
        case _:
            menu()

if __name__ == "__main__":
    menu()