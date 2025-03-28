import os


class player:
    """
    This class is the player instance, 
    it contains the player attributes and the methods
    for updating the player position
    """
    def __init__(self,name, score,position):
        self.name = name
        self.score = score
        self.position = position

    def climb(self,x:int):
        """
        This method accepts the dice roll value and an instance of the player class, 
        and updates the position of the player on the board based on it's previous position
        """
        if(x == 3 and self.position < 24):
            self.position = 24
        elif (x == 14 and self.position < 42):
            self.position = 42
        elif (x == 30 and self.position < 86):
           self.position = 86
        elif (x == 37 and self.position < 57):
            self.position = 57
        elif (x == 60 and self.position < 96):
           self.position = 96
        elif (x == 66 and self.position < 74):
            self.position = 74
        else:
            self.position += x
    def fall(self,y:int) -> int:
        """
        This method accepts the dice roll value and an instance of the player class, 
        and updates the position of the player on the board based on it's previous position
        """
        if(y == 27):
            self.position = 7
        elif (y == 20):
            self.position = 1
        elif (y == 89):
           self.position = 5
        elif (y == 57):
           self.position = 29
        elif (y == 76):
           self.position = 44
        elif (y == 97):
           self.position = 2
        else:
            self.position += 0

class game:
    l = []
    """
    This class is the game instance, 
    it contains the methods for the board, and game conditions
    """
    def __init__(self):
        pass
    def board(l:list):
        print("SNAKES & LADDERS\t\t\t\tCreated by Andre Lewis (2108069)\n\n")
        turn = 2    
        for i in range(0,100):
            l.insert(i,i+1)
        for j in range(99,-1,-10):
            if(turn % 2 == 0):
                print(l[j],"|",l[j-1],"|",l[j-2],"|",l[j-3],"|",l[j-4],"|",l[j-5],"|",l[j-6],"|",l[j-7],"|",l[j-8],"|",l[j-9])
                print("-------------------------------------------------------------------------")
                turn -= 1
            else:
                print(l[j-9],"|",l[j-8],"|",l[j-7],"|",l[j-6],"|",l[j-5],"|",l[j-4],"|",l[j-3],"|",l[j-2],"|",l[j-1],"|",l[j])
                print("-------------------------------------------------------------------------")
                turn +=1
    def ladders():
        """
        """
        print("Ladders\n 3 -> 24 \n 14 -> 42\n 30 -> 86\n 37 -> 57\n 50 -> 96\n 66 -> 74\n")
    def snakes():
        """
        """
        print("Snakes\n 27 -> 7 \n 20 -> 1\n 89 -> 5\n 57 -> 29\n 76 -> 44\n 97 -> 2\n")
    def dice_roll() -> int:
        """
        """
        import random
        dice =[1,2,3,4,5,6]
        return random.choice(dice)
    def start(self) -> int:
        """
        """
        os.system('cls')
        try:
            playersList = {}
            numPlayers = int(input("Enter the number of players: "))
            if (numPlayers <= 4 and numPlayers > 1):
                for x in range(numPlayers):
                    playerName = input(f'Enter the name of Player #{x+1}: ')
                    playersList.update({
                        f'player{x}': player(playerName,0,0),
                    })
                while(True):
                    for p in playersList:
                        os.system('cls')
                        self.board(self.l)
                        self.snakes()
                        self.ladders()
                        try:
                            choice = int(input(f'{playersList[p].name}: Enter "1" to roll the dice ->  '))
                            if(choice == 1):
                                dice = self.dice_roll()
                                print("Dice: ",dice)
                                playersList[p].climb(x=dice)
                                playersList[p].fall(y=dice)
                                print(f'{playersList[p].name} is at position {playersList[p].position}')
                                os.system('pause')
                            else:
                                print('Enter "1" to proceed!....')
                                os.system('pause')
                                continue
                        except:
                            reversed(p)
                    if(playersList[p].position >= 100):
                        playersList[p].score += 1
                        print("Player ",playersList[p].name, " wins!")
                        break              
            else:
                print('Enter a valid number!')
                os.system('pause')
                self.start(self=game)
        except:
                    os.system('pause')
                    self.start(self=game)
        


if __name__ == "__main__":
    Game = game.start(self=game)
