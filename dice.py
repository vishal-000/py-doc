import random
player_1 = input("Enter player_1 name here :")
player_2 = input("Enter player 2 name here :")
turn =1

score_1,score_2 = 0,0
print("this is trial one")
if turn == 1:
    score_1 += random.randint(1,6)
    turn = 2
if turn ==2:
    score_2 += random.randint(1,6)
    turn = 1 
print(f"The scores are score_1:{score_1} and score_2:{score_2}")
print("this is trial two")
def if(key):
        return(to roll again )
        if turn == 1:
            score_1 += random.randint(1,6)
            turn = 2
        if turn ==2:
            score_2 += random.randint(1,6)
            turn = 1 
        print(f"The scores are score_1:{score_1} and score_2:{score_2}")
        print("this is trial three")
        if turn == 1:
            score_1 += random.randint(1,6)
            turn = 2

        if turn ==2:
            score_2 += random.randint(1,6)
            turn = 1  
        print(f"The scores are score_1:{score_1} and score_2:{score_2}")
        print("this is trial four")
        if turn == 1:
            score_1 += random.randint(1,6)
            turn = 2
        if turn ==2:
            score_2 += random.randint(1,6)
            turn = 1   
        print(f"The scores are score_1:{score_1} and score_2:{score_2}")
        if score_1 > score_2:
            print(f"The Winner is {player_1} with score of {score_1}")
        else:
            print(f"The winner is {player_2} with score if {score_2}")