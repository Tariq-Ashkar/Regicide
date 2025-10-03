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

root.title("regicide")
root.config(bg="grey")


screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
print (screen_h)

FRAME_WIDTH = int(screen_w * 0.9)
FRAME_HEIGHT = int(screen_h * 0.9)
root.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}")
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
        print("here")
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
def reveal_enemy(canvas, castle):
    next_enemy=castle.pop()
    canvas.move(next_enemy.character_id, FRAME_WIDTH*0.5+400, FRAME_WIDTH*0.15+400)
    return next_enemy
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
        self.max_hp = 200
        self.hp = self.max_hp
        self.atk = 5
        self.canvas = canvas
        self.x = x
        self.y = y


        
        file_path = f"enemies/{self.suit}/{self.rank} {self.suit}.png"

        
        self.image = image_resize(file_path, self.width, self.height)

        # draw sprite
        self.character_id = canvas.create_image(
                                                    self.x,
                                                    self.y,
                                                    image=self.image,
                                                    anchor="center"
                                                )
        self.health_bar_bg = canvas.create_rectangle(450,
                                                     50,
                                                     950 *
                                                     (self.hp / self.max_hp),
                                                     70,
                                                     fill="black")
        self.health_bar = canvas.create_rectangle(450,
                                                  50,
                                                  950 *
                                                  (self.hp / self.max_hp),
                                                  70,
                                                  fill="green")

    def update_health_bar(self):
        '''changes the length and colour of health bar'''
        width = 950 * (self.hp / self.max_hp)
        self.canvas.coords(self.health_bar, 450, 50, width, 70)
        if self.hp > self.max_hp / 2:
            self.canvas.itemconfig(self.health_bar, fill="green")
        elif self.hp > self.max_hp / 4:
            self.canvas.itemconfig(self.health_bar, fill="yellow")
        else:
            self.canvas.itemconfig(self.health_bar, fill="red")



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
        hand1.cards.remove(self)
        played_hand1.add_card(self)
        print(hand1.cards)
        print(played_hand1.cards)
        combo_flag, combo_cards= checkCombo(played_hand1.cards, hand1.cards, base_atk)
        print(combo_cards)
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
        num_cards=4
        card_width=105
        total_cards_width = num_cards * card_width
        spacing = (self.width - total_cards_width) // (num_cards - 1)

        self.card_positions = [
             1+ self.x + i * (card_width + spacing) for i in range(num_cards)
        ]

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
        num_cards=8
        card_width=105
        total_cards_width = num_cards * card_width
        spacing = (self.width - total_cards_width) // (num_cards - 1)

        self.card_positions = [
            3 + self.x + i * (card_width + spacing) for i in range(num_cards)
        ]
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
        self.cards.clear()
        for _ in range(num_cards):
            card_obj = tavern.draw_card()
            if not card_obj:
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
        num_cards=2
        card_width=105
        total_cards_width = num_cards * card_width
        spacing = (self.width - total_cards_width) // (num_cards - 1)

        self.joker_widg_slots = [
            3 + self.x + i * (card_width + spacing) for i in range(num_cards)
        ]
    def fill_jokers(self):
        for slot in self.joker_widg_slots:
            joker1=Joker(game_canvas, 100, 144, slot, self.y+4)


        
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

class discard_pile:
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height
        self.cards = []   # list of PhotoImage references for the pile
        self.canvas = canvas
        self.x = x
        self.y = y

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
        self.cards.append(tk_img)

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
bg_image = image_resize("board.png",  width=FRAME_WIDTH+200, height=FRAME_HEIGHT+200,)
menu_canvas.create_image(FRAME_WIDTH//2, FRAME_HEIGHT//2, anchor="c", image=bg_image)

start_btn = tk.Button(main_menu,
                      text="Start Game",
                      font=("Arial", 14, "bold"),
                      command=lambda: show_frame(game_screen))
start_btn.place(relx=0.43, rely=0.3, relwidth=0.14, relheight=0.075)

exit_btn = tk.Button(main_menu,
                     text="Exit",
                     font=("Arial", 14, "bold"),
                     command=root.quit)
exit_btn.place(relx=0.43, rely=0.4, relwidth=0.14, relheight=0.075)

title_img = image_resize('Regicide.png', 400, 200)
title=menu_canvas.create_image(FRAME_WIDTH*0.5, FRAME_HEIGHT*0.2, anchor="center", image=title_img)



pause_canvas = tk.Canvas(pause_menu,
                       width=FRAME_WIDTH,
                       height=FRAME_HEIGHT,
                       bg="grey")
pause_canvas.pack()

pause_canvas.create_image(FRAME_WIDTH//2, FRAME_HEIGHT//2, anchor="c", image=bg_image)
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

win_canvas.create_image(FRAME_WIDTH//2, FRAME_HEIGHT//2, anchor="c", image=bg_image)
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
game_canvas.create_image(FRAME_WIDTH//2, FRAME_HEIGHT//2, anchor="c", image=bg_image)

# Initialising deck
deck=[]

for suit in SUITS:
    for r in range(1,11):
        deck.append(card(game_canvas, r, suit, 105, 144, -200, -200))

random.shuffle(deck)
tavern1=tavern(game_canvas, deck,FRAME_WIDTH*0.07,FRAME_HEIGHT*0.72, 102, 144)

played_width = 500
played_height = 184
played_x = (FRAME_WIDTH - played_width) // 2
played_y = int(FRAME_HEIGHT * 0.5)
played_hand1 = played_hand(game_canvas, played_x, played_y, played_width, played_height)

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

current_enemy=reveal_enemy(game_canvas, castle)
current_enemy.update_health_bar()

# Initialising Misc
hand_width = 965
hand_height = 178
hand_x = (FRAME_WIDTH - hand_width) // 2
hand_y = int(FRAME_HEIGHT * 0.77)
hand1 = hand(game_canvas, hand_x, hand_y, hand_width, hand_height)
hand1.fill_hand(tavern1)

discard = discard_pile(game_canvas, FRAME_WIDTH*0.9,FRAME_HEIGHT*0.8, 105, 154)  # x,y is center

jokerwid=JokerWidget(game_canvas, FRAME_WIDTH*0.8,FRAME_HEIGHT*0.1, 220, 154)
jokerwid.fill_jokers()

base_atk=0
game_lost=False






def discard_random(event=None):
    while played_hand1.cards:
        card_obj = played_hand1.cards.pop(0)   
        discard.add_card(card_obj)


clear_btn = tk.Button(game_screen, text="clear", command=discard_random)
clear_btn.place(relx=0.66, rely=0.5, anchor="center")

discard_btn = tk.Button(game_screen, text="discard", command=discard_random)
discard_btn.place(relx=0.66, rely=0.55, anchor="center")

lose_btn = tk.Button(game_screen, text="lose", command=lambda: show_frame(lose_menu))
lose_btn.place(relx=0.66, rely=0.6, anchor="center")

pause_btn = tk.Button(game_screen, text="pause", command=lambda: show_frame(pause_menu))
pause_btn.place(relx=0.66, rely=0.65, anchor="center")

win_btn = tk.Button(game_screen, text="win", command=lambda: show_frame(win_menu))
win_btn.place(relx=0.66, rely=0.7, anchor="center")


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
