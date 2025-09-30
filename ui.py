import tkinter as tk
from PIL import Image, ImageTk
import random
S='spades'
C='clubs'
D='diamonds'
H='hearts'
SUITS=[S,C,D,H]
base_atk=0

# creating the initial window
root = tk.Tk()
root.geometry("1400x1000")
root.title("regicide")
root.config(bg="grey")

FRAME_WIDTH = 1400
FRAME_HEIGHT = 1000

class AttackLabel():
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height
        self.canvas = canvas
        self.x = x
        self.y = y

        self.label_id = canvas.create_text(
            self.x + self.width // 2,
            self.y + self.height + 20,
            text="faswghshsw",
            font=("Arial", 16, "bold"),
            fill="white"
        )

    def update_label(self, number):
        self.canvas.itemconfig(self.label_id, text=number)

def sortHand(hand):
    sorting_dict={S:[],
                  C:[],
                  D:[],
                  H:[]
    }

    for card in hand:
        sorting_dict[card.suit].append(card)
    for suit in sorting_dict:
        sorting_dict[suit]=sorted(sorting_dict[suit], key= lambda c: c.rank)
    
    return sorting_dict[S]+sorting_dict[C]+sorting_dict[D]+sorting_dict[H]
def checkCombo(played, hand, base_atk):
    if len(played) == 1:
        if played[0].rank == 1:
            return True, hand
        combocards = [
            card_in_hand if (card_in_hand.rank == played[0].rank and card_in_hand.rank < 6) or card_in_hand.rank == 1 else "X"
            for card_in_hand in hand
        ]
        combo_flag = any(card != "X" for card in combocards)
        return combo_flag, combocards

    if len(played) == 2:
        if played[0].rank == 1 or played[1].rank==1:
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

def reveal_next_enemy(canvas, castle, current_enemy):
    if current_enemy:
        canvas.delete(current_enemy.health_bar_bg)
        canvas.delete(current_enemy.health_bar)
        canvas.delete(current_enemy.hp_label.label_id)
    
        
    next_enemy = castle.pop()
    canvas.coords(next_enemy.character_id, 598, 90)

    # Correct health bar creation
    next_enemy.health_bar_bg = canvas.create_rectangle(
        450, 50, 950, 70, fill="black"
    )
    next_enemy.health_bar = canvas.create_rectangle(
        450, 50, 450 + 500 * (next_enemy.hp / next_enemy.max_hp), 70, fill="green"
    )

    next_enemy.hp_label=AttackLabel(canvas, 650, 0, 100, 30)
    
    return next_enemy

def attack():

    global discard
    global current_enemy
    global base_atk
    global tavern1
    global hand1
    global played_hand1
    global game_canvas
    global castle
    global enemy_attack
    enemy_isAlive=True
    heart_flag=False
    diamond_flag=False
    club_flag=False
    spade_flag=False
    print(f"pre: tavern: {len(tavern1.cards)}, hand: {len(hand1.cards)}, discard: {len(discard.cards)}, hp: {current_enemy.hp}, atk: {current_enemy.atk} ")
    for c in played_hand1.cards:
        # Flags so suits dont get triggered multiple times. Enemy suit accounted for in boolean. Hearts always before diamonds
        if c.suit==H and heart_flag==False and current_enemy.suit!=H:  # Shuffle discard and pop cards from discard onto bottom of deck
            tavern1.heal(discard)
            heart_flag=True
        if c.suit==D and diamond_flag==False and current_enemy.suit!=D : # Draws cards from top of tavern1.cards into hand until hand is 8 cards full. sorts hand.
            hand1.fill_hand(tavern1, base_atk)
            diamond_flag=True
        if c.suit==S and spade_flag==False and current_enemy.suit!=S : # Reduces enemy attack
            current_enemy.atk=0 if current_enemy.atk-base_atk<0 else current_enemy.atk-base_atk
            enemy_attack.update_label(current_enemy.atk)
            spade_flag=True
        if c.suit==C and club_flag==False and current_enemy.suit!=C: # Double damage
            base_atk=base_atk*2
            club_flag=True

    # STEP 3 Attack enemy and check if theyre dead
    current_enemy.hp=current_enemy.hp-base_atk   # DEALING DAMAGE
    current_enemy.update_health_bar()
    # (i)
    if current_enemy.hp==0: # perfect kill?
        tavern1.cards.append(current_enemy)
        game_canvas.coords(current_enemy.character_id, -200, -200)
        current_enemy=reveal_next_enemy(game_canvas, castle, current_enemy) #(iii, current_enemy
        current_enemy.update_health_bar()

        enemy_isAlive=False
    elif current_enemy.hp<0: # overkill?
        discard.add_card(current_enemy)
        current_enemy=reveal_next_enemy(game_canvas, castle, current_enemy) #(iii)
        current_enemy.update_health_bar()
        enemy_isAlive=False
    
    # (ii)
    while len(played_hand1.cards)>0:

        discard.add_card(played_hand1.cards.pop())
   
    base_atk=0
    print(f"post: tavern: {len(tavern1.cards)}, hand: {len(hand1.cards)}, discard: {len(discard.cards)}, hp: {current_enemy.hp}, atk: {current_enemy.atk} ")
    if enemy_isAlive and current_enemy.atk>0:
        play_btn.configure(text = "Defend", command=lambda: defend())
    player_attack.update_label(0)
    



cumulative_blocked=0
def defend():      
    print('defending')  
    global discard
    global current_enemy
    global base_atk
    global tavern1
    global hand1
    global played_hand1
    global game_canvas
    global castle
    global enemy_attack
    global cumulative_blocked

    incoming_damage=current_enemy.atk
    for _ in range(len(played_hand1.cards)):
        c=played_hand1.cards.pop()
        cumulative_blocked=cumulative_blocked+c.rank
        discard.add_card(c)
    
    if cumulative_blocked>=incoming_damage:
        play_btn.configure(text = "Attack", command=lambda: attack())
        player_attack.update_label(0)
        base_atk=0
        return
    elif cumulative_blocked<incoming_damage and len(hand1.cards)==0:
        show_frame(lose_menu)
        return

def image_resize(file, width, height):
    '''
    resizes an image to fit the frame

    parameter is the file to be resized
    '''
    og_image = Image.open(file)
    new_image = og_image.resize((width, height), Image.NEAREST)
    return ImageTk.PhotoImage(new_image)




class enemy():
    def __init__(self, canvas, rank, x, y, suit, width, height):
        self.width = width
        self.height = height
        self.suit = suit
        self.rank = rank
        self.max_hp = self.rank*2
        self.hp = self.max_hp
        self.atk = rank
        self.canvas = canvas
        self.x = x
        self.y = y


        
        self.filepath = f"enemies/{self.suit}/{self.rank} {self.suit}.png"

        
        self.image = image_resize(self.filepath, self.width, self.height)

        # draw sprite
        self.character_id = canvas.create_image(
                                                    self.x,
                                                    self.y,
                                                    image=self.image,
                                                    anchor="nw"
                                                )
        self.health_bar_bg = None
        self.health_bar = None
        self.hp_label=None
        
    def update_health_bar(self):
        '''changes the length and colour of health bar'''
        width = 500 * (self.hp / self.max_hp)
        self.canvas.itemconfig(self.health_bar, fill="yellow")
        self.canvas.coords(self.health_bar, 450, 50, 450+width, 70)
        if self.hp > self.max_hp / 2:
            self.canvas.itemconfig(self.health_bar, fill="green")
        elif self.hp > self.max_hp / 4:
            self.canvas.itemconfig(self.health_bar, fill="yellow")
        else:
            self.canvas.itemconfig(self.health_bar, fill="red")
        self.hp_label.update_label(f"{self.hp} / {self.max_hp}")



class tavern():
    def __init__(self, canvas, cards, x, y, width, height):
        self.width = width
        self.height = height
        self.cards = cards        
        self.max_cards = len(cards)
        self.canvas = canvas
        self.x = x
        self.y = y

        file_path = "back/Card back.png"
        self.image = image_resize(file_path, self.width, self.height)

        # draw tavern deck
        self.character_id = canvas.create_image(
            self.x,
            self.y,
            image=self.image,
            anchor="nw"
        )

        self.label_id = canvas.create_text(
            self.x + self.width // 2,
            self.y + self.height + 20,
            text=f"{len(self.cards)}/{self.max_cards}",
            font=("Arial", 16, "bold"),
            fill="white"
        )

    def update_label(self):
        self.canvas.itemconfig(self.label_id, text=f"{len(self.cards)}/{self.max_cards}")

    def draw_card(self):
        """Return the top card from the tavern if available"""
        if self.cards:
            card_obj = self.cards.pop()
            self.update_label()
            return card_obj
        return None
    
    def heal(self, discard):
        try:
            temp = list(zip(discard.cards, discard.references))  # Pair the elements
            random.shuffle(temp)  # Shuffle the pairs

            res1, res2 =zip(*temp)  # Unzip into separate lists

            discard.cards, discard.references = list(res1), list(res2)
        except(Exception):
            return
        for _ in range(0, base_atk):
            if len(discard.cards)==0: # Check if theres anything left in discard
                break
            next_card=discard.cards.pop()
            to_del=discard.references.pop()
            del to_del
            tavern1.cards.append(next_card)



class card():
    def __init__(self, canvas, rank, suit, width, height, x, y):
        self.width = width
        self.height = height
        self.suit = suit
        self.rank = rank
        self.canvas = canvas
        self.x = x
        self.y = y
        self.border_id = None
        self.raised = False 


        # store filepath so other systems (discard, save, etc.) can reopen it
        self.filepath = f"{self.suit}/{self.rank} {self.suit}.png"

        # load & store PhotoImage (keeps reference on self)
        self.image = image_resize(self.filepath, self.width, self.height)

        # draw sprite
        self.character_id = canvas.create_image(
            self.x,
            self.y,
            image=self.image,
            anchor="nw"
        )
        canvas.tag_bind(self.character_id, "<Button-1>", self.on_click)

    def on_click(self, event):
        global base_atk
        global played_hand1
        global hand1
        global player_attack
        hand1.cards.remove(self)
        played_hand1.add_card(self)

        combo_flag, combo_cards= checkCombo(played_hand1.cards, hand1.cards, base_atk)

        for c in hand1.cards:
            if isinstance(c, card) and c.raised:
                c.canvas.move(c.character_id, 0, +20)
                if c.border_id:
                    c.canvas.move(c.border_id, 0, +20)
                c.raised = False

        
        if combo_flag:
            for c in combo_cards:
                if isinstance(c, card) and not c.raised:
                    c.canvas.move(c.character_id, 0, -20)
                    if c.border_id:
                        c.canvas.move(c.border_id, 0, -20)
                    c.raised = True
        base_atk=base_atk+self.rank

        displayed_attack=base_atk
        for c in played_hand1.cards:
            if c.suit==C:
                displayed_attack=base_atk*2
                break
        player_attack.update_label(displayed_attack)
        print(f"Base Attack: {base_atk}")

    def set_x(self, new_x):
        self.x = new_x

    def get_x(self):
        return self.x

    def set_y(self, new_y):
        self.y = new_y

    def get_y(self):
        return self.y

    def __repr__(self):
        return str(self.rank)+self.suit


        


class played_hand():
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height
        self.cards = []
        self.canvas = canvas
        self.x = x
        self.y = y
        
        self.hand_bg = canvas.create_rectangle(x,
                                                y,
                                                x+width,
                                                y+height,
                                                fill="yellow",
                                                stipple="gray50"
                                                )
        self.card_positions=[470,590,710,830]

    def add_card(self, card_obj):
        """Add a card to the played hand"""
        if len(self.cards) < len(self.card_positions):
            pos_x = self.card_positions[len(self.cards)]
            pos_y = self.y + 20  # small offset inside the zone

            # update the card’s logical position
            card_obj.set_x(pos_x)
            card_obj.set_y(pos_y)

            # move the image into place
            self.canvas.coords(card_obj.character_id, pos_x, pos_y)

            self.canvas.tag_unbind(card_obj.character_id, "<Button-1>")

            # bring card above background
            self.canvas.tag_raise(card_obj.character_id)

            # store in played hand
            self.cards.append(card_obj)
        else:
            print("Played hand is full!")
        
    def clear(self):
        self.cards=[]
        




class hand():
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height
        
        self.canvas = canvas
        self.x = x
        self.y = y
        self.slotwidth=115
        self.slotheight=154
        self.card_positions=[230,350,470,590,710,830,950,1070]
        self.cards=[]
        self.highlights = {}
        self.hand_bg = self.canvas.create_rectangle(self.x,
                                                    self.y,
                                                    self.x+self.width,
                                                    self.y+self.height,
                                                    fill="brown",
                                                    stipple="gray50"
                                                    )
    

    
        
    
    def fill_hand(self, tavern, num_cards=8):
        """Draw cards from the tavern to fill up the hand slots"""
        for _ in range(num_cards):
            card_obj = tavern.draw_card()

            if not card_obj or len(self.cards)==8:
                break  # tavern empty
            self.cards.append(card_obj)
        self.cards=sortHand(self.cards)

        for (card, pos) in zip(self.cards, self.card_positions):
            card.set_x(pos)
            card.set_y(self.y + 15)
            self.canvas.coords(card.character_id, card.get_x(), card.get_y())
            self.canvas.tag_raise(card.character_id)

            
        

class JokerWidget():
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height
        
        self.canvas = canvas
        self.x = x
        self.y = y

        self.hand_bg = canvas.create_rectangle(x,
                                                y,
                                                x+width,
                                                y+height,
                                                fill="red",
                                                stipple="gray50"
                                                )
        self.joker_widg_slots=[1165, 1275]
    def fill_jokers(self):
        for slot in self.joker_widg_slots:
            joker1=Joker(game_canvas, 100, 144, slot, 25)


        
class Joker():
    def __init__(self, canvas, width, height, x, y):
        self.width = width
        self.height = height
        self.canvas = canvas
        self.x = x
        self.y = y

        self.image = image_resize('joker (larry).png', self.width, self.height)

        # draw sprite
        self.character_id = canvas.create_image(
            self.x,
            self.y,
            image=self.image,
            anchor="nw"
        )
        canvas.tag_bind(self.character_id, "<Button-1>", self.on_click)

    def on_click(self, event):
        print(f"You clicked {self.rank} of {self.suit}")

class discard_pile():
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height
        self.cards = []   
        self.canvas = canvas
        self.x = x
        self.y = y
        self.references=[] # list of PhotoImage references for the pile

        # Label under pile
        self.label = tk.Label(canvas, text="Discarded: 0", bg="grey", fg="white", font=("Arial", 14, "bold"))
        self.label.place(x=self.x, y=self.y + self.height//2 + 10, anchor="n")

    def add_card(self, card_obj):
        """Move a card object into the discard pile."""
        try:
            self.canvas.tag_unbind(card_obj.character_id, "<Button-1>")
        except Exception:
            pass

        # Remove the card's existing image on the canvas (optional, since we redraw rotated)
        try:
            self.canvas.delete(card_obj.character_id)
        except Exception:
            pass
        # Resize card image to discard pile size and rotate
        img = Image.open(card_obj.filepath).resize((self.width, self.height), Image.NEAREST)
        angle = random.randint(-20, 20)
        img = img.rotate(angle, expand=True)

        # Convert to Tk image and keep reference
        tk_img = ImageTk.PhotoImage(img)
        self.references.append(tk_img)
        self.cards.append(card_obj)

        # Draw centered on pile
        self.canvas.create_image(self.x, self.y, image=tk_img, anchor="center")

        # Update counter
        self.label.config(text=f"Discarded: {len(self.cards)}")



def show_frame(frame):
    '''
    raises the desired frame to the front

    the parameter is the desired frame
    '''
    frame.tkraise()

main_menu = tk.Frame(root, width=FRAME_WIDTH, height=FRAME_HEIGHT)
pause_menu = tk.Frame(root, width=FRAME_WIDTH, height=FRAME_HEIGHT)
win_menu = tk.Frame(root, width=FRAME_WIDTH, height=FRAME_HEIGHT)
lose_menu = tk.Frame(root, width=FRAME_WIDTH, height=FRAME_HEIGHT)

game_screen = tk.Frame(root, width=FRAME_WIDTH, height=FRAME_HEIGHT)

for frame in (main_menu, game_screen, lose_menu, win_menu, pause_menu,):
    frame.place(x=0, y=0, relwidth=1, relheight=1)



menu_canvas = tk.Canvas(main_menu,
                        width=FRAME_WIDTH,
                        height=FRAME_HEIGHT,
                        bg="grey")
menu_canvas.pack()
bg_image = image_resize("board.png", FRAME_WIDTH, FRAME_HEIGHT)
menu_canvas.create_image(0, 0, anchor="nw", image=bg_image)

start_btn = tk.Button(main_menu,
                      text="Start Game",
                      font=("Arial", 14, "bold"),
                      command=lambda: show_frame(game_screen))
start_btn.place(x=600, y=300, height=75, width=200)

exit_btn = tk.Button(main_menu,
                     text="Exit",
                     font=("Arial", 14, "bold"),
                     command=root.quit)
exit_btn.place(x=600, y=500, height=75, width=200)

title_img = image_resize('Regicide.png', 400, 200)
title=menu_canvas.create_image(500, 50, anchor="nw", image=title_img)



pause_canvas = tk.Canvas(pause_menu,
                       width=FRAME_WIDTH,
                       height=FRAME_HEIGHT,
                       bg="grey")
pause_canvas.pack()

pause_canvas.create_image(0, 0, anchor="nw", image=bg_image)
pause_img = image_resize('Pause.png', 400, 200)
pause_title=pause_canvas.create_image(500, 50, anchor="nw", image=pause_img)

back_to_menu_btn = tk.Button(pause_menu,
                             text="Back to Main Menu",
                             font=("Arial", 14),
                             command=lambda: show_frame(main_menu))
back_to_menu_btn.place(x=600, y=200, height=50, width=200)

start_btn = tk.Button(pause_menu,
                      text="play Game",
                      font=("Arial", 14, "bold"),
                      command=lambda: show_frame(game_screen))
start_btn.place(x=600, y=300, height=75, width=200)



win_canvas = tk.Canvas(win_menu,
                       width=FRAME_WIDTH,
                       height=FRAME_HEIGHT,
                       bg="grey")
win_canvas.pack()

win_canvas.create_image(0, 0, anchor="nw", image=bg_image)
win_img = image_resize('win.png', 400, 200)
win_title=win_canvas.create_image(500, 50, anchor="nw", image=win_img)

back_to_menu_btn = tk.Button(win_menu,
                             text="Back to Main Menu",
                             font=("Arial", 14),
                             command=lambda: show_frame(main_menu))
back_to_menu_btn.place(x=600, y=200, height=50, width=200)



lose_canvas = tk.Canvas(lose_menu,
                       width=FRAME_WIDTH,
                       height=FRAME_HEIGHT,
                       bg="grey")
lose_canvas.pack()

lose_canvas.create_image(0, 0, anchor="nw", image=bg_image)
lose_img = image_resize('LOSE.png', 400, 200)
lose_title=lose_canvas.create_image(500, 50, anchor="nw", image=lose_img)

back_to_menu_btn = tk.Button(lose_menu,
                             text="Back to Main Menu",
                             font=("Arial", 14),
                             command=lambda: show_frame(main_menu))
back_to_menu_btn.place(x=600, y=200, height=50, width=200)



game_canvas = tk.Canvas(game_screen, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg="grey")
game_canvas.pack()
game_canvas.create_image(0, 0, anchor="nw", image=bg_image)

# Initialising deck
deck=[]

for suit in SUITS:
    for r in range(1,11):
        deck.append(card(game_canvas, r, suit, 105, 144, -200, -200))

random.shuffle(deck)
tavern1=tavern(game_canvas, deck, 69, 695, 102, 144)

 # Initialising Hand  
hand1=hand(game_canvas, 220, 680, 965, 178)
hand1.fill_hand(tavern1)

# Initialising Castle and current_enemy
castle=[]

for rank in range(20,5,-5):
    for suit in SUITS:
        castle.append(enemy(game_canvas, rank, -400,-400, suit, 204, 288))


kings=castle[:4]
queens=castle[4:8]
jacks=castle[8:12]

random.shuffle(kings)
random.shuffle(queens)
random.shuffle(jacks)

castle.clear()
castle=kings+queens+jacks

current_enemy=reveal_next_enemy(game_canvas, castle, None)
current_enemy.update_health_bar()

# Initialising Misc
played_hand1 = played_hand(game_canvas, 452, 475, 500, 184)

discard = discard_pile(game_canvas, 1300, 800, 105, 154)  # x,y is center

jokerwid=JokerWidget(game_canvas, 1160, 20, 220, 154)
jokerwid.fill_jokers()


enemy_attack=AttackLabel(game_canvas, 650, 340, 100, 30)
enemy_attack.update_label(current_enemy.atk)


player_attack=AttackLabel(game_canvas, 650, 405, 100, 30)
player_attack.update_label(0)


base_atk=0
game_lost=False






def discard_random(event=None):
    while played_hand1.cards:
        card_obj = played_hand1.cards.pop(0)   
        discard.add_card(card_obj)


clear_btn = tk.Button(game_screen, text="clear", command=discard_random)
clear_btn.place(x=960, y=615)  

discard_btn = tk.Button(game_screen, text="discard", command=discard_random)
discard_btn.place(x=960, y=615)  

lose_btn = tk.Button(game_screen, text="lose", command=lambda: show_frame(lose_menu))
lose_btn.place(x=960, y=575)  

pause_btn = tk.Button(game_screen, text="pause", command=lambda: show_frame(pause_menu))
pause_btn.place(x=960, y=535)  

play_btn = tk.Button(game_screen, text="Attack", command=lambda: attack())
play_btn.place(x=960, y=495)  


root.bind("<KeyRelease-1>", lambda e: hand1.unhighlight_card(1))

root.bind("<KeyPress-2>", lambda e: hand1.highlight_card(2))
root.bind("<KeyRelease-2>", lambda e: hand1.unhighlight_card(2))

root.bind("<KeyPress-3>", lambda e: hand1.highlight_card(3))
root.bind("<KeyRelease-3>", lambda e: hand1.unhighlight_card(3))

root.bind("<KeyPress-4>", lambda e: hand1.highlight_card(4))
root.bind("<KeyRelease-4>", lambda e: hand1.unhighlight_card(4))

root.bind("<KeyPress-5>", lambda e: hand1.highlight_card(5))
root.bind("<KeyRelease-5>", lambda e: hand1.unhighlight_card(5))

root.bind("<KeyPress-6>", lambda e: hand1.highlight_card(6))
root.bind("<KeyRelease-6>", lambda e: hand1.unhighlight_card(6))

root.bind("<KeyPress-7>", lambda e: hand1.highlight_card(7))
root.bind("<KeyRelease-7>", lambda e: hand1.unhighlight_card(7))

root.bind("<KeyPress-8>", lambda e: hand1.highlight_card(8))
root.bind("<KeyRelease-8>", lambda e: hand1.unhighlight_card(8))




show_frame(main_menu)
# Run the Tkinter event loop
root.mainloop()
