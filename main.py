import random
import collections
S='S'
C='C'
D='D'
H='H'
SUITS=[S,C,D,H]


class card():
    def __init__(self,suit='', rank=0):
        self.suit=suit
        self.rank=rank

    def __repr__(self):
        return str(self.rank)+self.suit

class enemy(card):
    def __init__(self, suit, rank):
        super().__init__(suit, rank)
        if self.rank == 11:
            power=10
        elif self.rank == 12:
            power=15
        elif self.rank == 13:
            power=20
        self.hp=power*2
        self.atk=power

def sortHand(hand):
    sorting_dict={"S":[],
                  "C":[],
                  "D":[],
                  "H":[]
    }

    for card in hand:
        sorting_dict[card.suit].append(card)
    for suit in sorting_dict:
        sorting_dict[suit]=sorted(sorting_dict[suit], key= lambda c: c.rank)
    
    return sorting_dict["S"]+sorting_dict["C"]+sorting_dict["D"]+sorting_dict["H"]

def checkCombo(played, hand, base_atk):
    combo_flag=False
    combocards=[]
    if len(played)==1:
        if played[0].rank == 1:
                combocards=hand
                combo_flag=True
        else: 
            for c in range(0,len(hand)):
                if hand[c].rank==played[0].rank or hand[c].rank==1:
                    combocards.append(hand[c])
                    combo_flag=True
                else:
                    combocards.append("X")
        return (combo_flag, combocards)
    if len(played)==2:
        if(played[0].rank==1 or played[0].rank==1):
            combo_flag=False 
            return (combo_flag, combocards)

        
        for c in range(0,len(hand)):
            if hand[c].rank==played[0].rank and base_atk+hand[c].rank<=10:
                combocards.append(hand[c])
                combo_flag=True

            else:
                combocards.append("X")
        return (combo_flag, combocards)   
    if len(played)==3:
        if(played[0].rank != 2):
            combo_flag=False 
            return (combo_flag, combocards)   
        for c in range(0,len(hand)):
            if hand[c].rank==played[0].rank and base_atk+hand[c].rank<=10:
                combocards.append(hand[c])
                combo_flag=True

            else:
                combocards.append("X")
        return (combo_flag, combocards)   

    return False
deck=[]


for suit in SUITS:
    for r in range(1,11):
        deck.append(card(suit, r))
    
castle=[[],[],[]]

for suit in SUITS:
    for s in range(0,3):
        castle[s].append(enemy(suit,11+s))

random.shuffle(deck)

hand=deck[:9]
hand=sortHand(hand)

for stage in castle:
    random.shuffle(stage)
stage=0
current_enemy=castle[stage].pop()
while True:

    print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
          "Hand: "+str(hand)+"\n"+
          "Deck: "+str(len(deck))+"/40")
    
    # STEP 1: play card from hand
    played=[]
    played.append(hand.pop(int(input("What would you like to play? Please enter the card number: "+"\n"+"\n"+"\n"))-1))# Error wrap this
    base_atk=played[0].rank

    print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
          "Hand: "+str(hand)+"\n"+
          "Deck: "+str(len(deck))+"/40"+"\n"+
          "Played Cards: "+str(played)+"\n"+"\n"+"\n")
    

    if played[0].rank in range(1,6):
        while True:
            flag=checkCombo(played, hand, base_atk)[0]
                                
            if not flag:
                print("No more combos available")
                break
        
            if input("Would you like to combo? Y/N: ") == "Y":
                    print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
                    "Hand: "+str(checkCombo(played, hand, base_atk)[1])+"\n"+
                    "Deck: "+str(len(deck))+"/40"+"\n"+
                    "Played Cards: "+str(played)) 
                    played.append(hand.pop(int(input("What would you like to combo with? Please enter the card number: "+"\n"+"\n"+"\n"))-1))# Error wrap this
                    base_atk=base_atk+played[len(played)-1].rank





            
    