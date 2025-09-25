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
        self.hp=self.rank*2
        self.atk=self.rank
    def __repr__(self):
        if self.rank==10:
            return "J"+self.suit
        if self.rank==15:
            return "Q"+self.suit        
        if self.rank==20:
            return "K"+self.suit        


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
    if len(played) == 1:
        if played[0].rank == 1:
            return True, hand.copy()
        combocards = [
            card_in_hand if (card_in_hand.rank == played[0].rank and card_in_hand.rank < 6) or card_in_hand.rank == 1 else "X"
            for card_in_hand in hand
        ]
        combo_flag = any(card != "X" for card in combocards)
        return combo_flag, combocards

    if len(played) == 2:
        if played[0].rank == 1:
            return False, []
        combocards = [
            card_in_hand if card_in_hand.rank == played[0].rank and base_atk + card_in_hand.rank <= 10 else "X"
            for card_in_hand in hand
        ]
        combo_flag = any(card != "X" for card in combocards)
        return combo_flag, combocards

    if len(played) == 3:
        if played[0].rank != 2:
            return False, []
        combocards = [
            card_in_hand if card_in_hand.rank == played[0].rank and base_atk + card_in_hand.rank <= 10 else "X"
            for card_in_hand in hand
        ]
        combo_flag = any(card != "X" for card in combocards)
        return combo_flag, combocards

    return False, []

def play_jester(hand, deck, discard, jesters):
    if jesters > 0:
        discard += hand
        hand.clear()
        for _ in range(8):
            if deck:
                hand.append(deck.pop())
        jesters -= 1
        print("Jester Played!")
    else:
        print("No more jesters left!")
    return hand, deck, discard, jesters

deck=[]

for suit in SUITS:
    for r in range(1,11):
        deck.append(card(suit, r))
    
castle=[]

for s in range(20,5,-5):
    for suit in SUITS:
        castle.append(enemy(suit,s))
random.shuffle(deck)

hand=[]
for _  in range (8):
    hand.append(deck.pop())

hand=sortHand(hand)

random.shuffle(castle[:4])
random.shuffle(castle[4:8])
random.shuffle(castle[8:11])

current_enemy=castle.pop()


played=[]
discard=[]
base_atk=0
game_lost=False
jesters=2
# Main Gameplay loop
while game_lost==False:
    enemy_isAlive=True

    print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
          "Hand: "+str(hand)+str(len(hand))+"\n"+
          "Jesters: "+str(jesters)+"\n"+
          "Deck: "+str(len(deck))+"/51"+"\n"+
          "Discard: "+str(len(discard))+" cards"+"\n"+
          "Played Cards: "+str(played)+"\n"+
          "Base Attack: "+str(base_atk)+"\n"+"\n")
    
    # STEP 1: play card from hand *Jesters can be played*

    card_input=input("What would you like to play? Please enter the card number: ")# Error wrap this

    while card_input == "J":
        hand, deck, discard, jesters = play_jester(hand, deck, discard, jesters)
        print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
            "Hand: "+str(hand)+str(len(hand))+"\n"+
            "Jesters: "+str(jesters)+"\n"+
            "Deck: "+str(len(deck))+"/51"+"\n"+
            "Discard: "+str(len(discard))+" cards"+"\n"+
            "Played Cards: "+str(played)+"\n"+
            "Base Attack: "+str(base_atk)+"\n"+"\n")
        card_input=input("What would you like to play? Please enter the card number: ")
    played.append(hand.pop(int(card_input)-1))

    base_atk=played[0].rank

    print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
          "Hand: "+str(hand)+str(len(hand))+"\n"+
          "Jesters: "+str(jesters)+"\n"+
          "Deck: "+str(len(deck))+"/51"+"\n"+
          "Discard: "+str(len(discard))+" cards"+"\n"+
          "Played Cards: "+str(played)+"\n"+
          "Base Attack: "+str(base_atk)+"\n"+"\n")
    
    #If a combo is available
    while True:  
        combo_flag=checkCombo(played, hand, base_atk)[0]
        if not combo_flag:
            print("No more combos available")
            break
            
        if input("Would you like to combo? Y/N: ") == "Y":
                print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
                "Hand: "+str(checkCombo(played, hand, base_atk)[1])+str(len(hand))+"\n"+
                "Jesters: "+str(jesters)+"\n"+
                "Deck: "+str(len(deck))+"/51"+"\n"+
                "Discard: "+str(len(discard))+" cards"+"\n"+
                "Played Cards: "+str(played)+"\n"+
                "Base Attack: "+str(base_atk)+"\n"+"\n")
                played.append(hand.pop(int(input("What would you like to combo with? Please enter the card number: "))-1))# Error wrap this
                base_atk=base_atk+played[len(played)-1].rank
        else:
            break
    
    # STEP 2 APPLY SUIT EFFECTS
    heart_flag=False
    diamond_flag=False
    club_flag=False
    spade_flag=False
    for c in played:
        # Flags so suits dont get triggered multiple times. Enemy suit accounted for in boolean. Hearts always before diamonds
        if c.suit==H and heart_flag==False and current_enemy.suit!=H:  # Shuffle discard and pop cards from discard onto bottom of deck
            random.shuffle(discard)
            for _ in range(0, base_atk):
                if len(discard)==0: # Check if theres anything left in discard
                    break
                deck.append(discard.pop())
            heart_flag=True
        if c.suit==D and diamond_flag==False and current_enemy.suit!=D : # Draws cards from top of deck into hand until hand is 8 cards full. sorts hand.
            for _ in range(0, base_atk):
                if len(hand)==8:
                    break 
                hand.append(deck.pop())
            hand=sortHand(hand)
            diamond_flag=True
        if c.suit==S and spade_flag==False and current_enemy.suit!=S : # Reduces enemy attack
            current_enemy.atk=0 if current_enemy.atk-base_atk<0 else current_enemy.atk-base_atk
            spade_flag=True
        if c.suit==C and club_flag==False and current_enemy.suit!=C: # Double damage
            base_atk=base_atk*2
            club_flag=True

    # STEP 3 Attack enemy and check if theyre dead
    
    current_enemy.hp=current_enemy.hp-base_atk   # DEALING DAMAGE

    # (i)
    if current_enemy.hp==0: # perfect kill?
        deck.append(current_enemy)
        current_enemy=castle.pop() #(iii)
        enemy_isAlive=False
    elif current_enemy.hp<0: # overkill?
        discard.append(current_enemy)
        current_enemy=castle.pop() #(iii)
        enemy_isAlive=False
    
    # (ii)
    discard=discard+played
    played.clear()
    base_atk=0

    if enemy_isAlive:# STEP 4 suffer damage. Skipped if we just killed the enemy. *Jesters can be played*
        
        incoming_damage=current_enemy.atk

        print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
                        "Hand: "+str(hand)+str(len(hand))+"\n"+
                        "Jesters: "+str(jesters)+"\n"+
                        "Deck: "+str(len(deck))+"/51"+"\n"+
                        "Discard: "+str(len(discard))+" cards"+"\n"+
                        "Played Cards: "+str(played)+"\n"+
                        "Base Attack: "+str(base_atk)+"\n"+"\n")
        
        while incoming_damage>0:
            if len(hand)==0:
                game_lost=True
                break
            print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
                        "Hand: "+str(hand)+str(len(hand))+"\n"+
                        "Jesters: "+str(jesters)+"\n"+
                        "Deck: "+str(len(deck))+"/51"+"\n"+
                        "Discard: "+str(len(discard))+" cards"+"\n"+
                        "Played Cards: "+str(played)+"\n"+
                        "Base Attack: "+str(base_atk)+"\n"+"\n")
            card_input=input("Discard a card to defend! Defense remaining: "+str(incoming_damage)+"   ")# Error wrap this

            while card_input == "J":
                hand, deck, discard, jesters = play_jester(hand, deck, discard, jesters)
                print("Current enemy: "+ str(current_enemy)+"    "+str(current_enemy.hp)+"HP"+"||"+str(current_enemy.atk)+"ATK"+"\n"+
                    "Hand: "+str(hand)+str(len(hand))+"\n"+
                    "Jesters: "+str(jesters)+"\n"+
                    "Deck: "+str(len(deck))+"/51"+"\n"+
                    "Discard: "+str(len(discard))+" cards"+"\n"+
                    "Played Cards: "+str(played)+"\n"+
                    "Base Attack: "+str(base_atk)+"\n"+"\n")
                if len(hand)==0:
                    game_lost=True
                    break
                card_input=input("Discard a card to defend! Defense remaining: "+str(incoming_damage)+"   ")
            if game_lost:
                break
            played.append(hand.pop(int(card_input)-1))
            incoming_damage=incoming_damage-played[len(played)-1].rank
    discard=discard+played
    played.clear()

#TODO:
# Test enemy behaviour in hand
# Handle game losses/defeats













