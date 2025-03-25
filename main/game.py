import os


class player:
    """
    mkf
    """
    def __init__(self,name, score,position):
        self.name = name
        self.score = score
        self.position = position

    def climb(*args,x:int) -> int:
        """
        Nla
        """
        print(args)
        if(x == 3):
            x = 24
        elif (x == 14):
            x = 42
        elif (30):
            x = 86
        return x
    def fall(*args,y:int) -> int:
        print(args)
        return y


class game:
    l = []
    """
    """
    def __init__(self):
        pass
    def board(l:list):
        print("SNAKES & LADDERS")
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
        print("Ladders\n 3-24 \n 14-42\n 30-86\n 37-57\n 50-96\n 66-74\n")
    def snakes(): 
        print("Snakes\n 3-24 \n 14-42\n 30-86\n 37-57\n 50-96\n 66-74\n")
    def dice_roll() -> int:
        import random
        dice =[1,2,3,4,5,6]
        return random.choice(dice)
    def start(self) -> int:
        os.system('cls')
        """        try:"""
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
                    try:
                        choice = int(input(f'{playersList[p].name}: Enter "1" to roll the dice ->  '))
                        if(choice == 1):
                            dice = self.dice_roll()
                            playersList[p].position += dice   
                            print("Dice: ",dice, "Before climb")
                            playersList[p].position = playersList[p].climb(x=dice)
                            print(f'{playersList[p].name} is at position {playersList[p].position}')
                            print(dice, "After fall")
                            playersList[p].position = playersList[p].fall(y=dice)
                            print(f'{playersList[p].name} is at position {playersList[p].position}')
                            os.system('pause')
                        else:
                            print('Enter "1" to proceed!....')
                            os.system('pause')
                            continue
                    except:
                        reversed(p)
                if(playersList[p].position >= 100):
                    break              
        else:
            print('Enter a valid number!')
            os.system('pause')
            self.start(self=game)
        """        except:
                    os.system('cls')
                    self.start(self=game)
        """


if __name__ == "__main__":
    Game = game.start(self=game)
