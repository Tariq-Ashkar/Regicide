import tkinter as tk
from PIL import Image, ImageTk
import random

# creating the initial window
root = tk.Tk()
root.geometry("1400x1000")
root.title("regicide")
root.config(bg="grey")

FRAME_WIDTH = 1400
FRAME_HEIGHT = 1000



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


        
        file_path = f"{self.suit}/{self.rank} {self.suit}.png"

        
        self.image = image_resize(file_path, self.width, self.height)

        # draw sprite
        self.character_id = canvas.create_image(
                                                    self.x,
                                                    self.y,
                                                    image=self.image,
                                                    anchor="nw"
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
        print(f"You clicked {self.rank} of {self.suit}")
        played_hand1.add_card(self)

    def set_x(self, new_x):
        self.x = new_x

    def get_x(self):
        return self.x

    def set_y(self, new_y):
        self.y = new_y

    def get_y(self):
        return self.y

        
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
        slotwidth=115
        slotheight=154

        self.hand_bg = canvas.create_rectangle(x,
                                                y,
                                                x+width,
                                                y+height,
                                                fill="brown",
                                                stipple="gray50"
                                                )
        
        self.hand_slot1 = canvas.create_rectangle(225,
                                                690,
                                                225+slotwidth,
                                                690+slotheight,
                                                fill="blue",
                                                
                                                )
        self.hand_slot2 = canvas.create_rectangle(345,
                                                690,
                                                345+slotwidth,
                                                690+slotheight,
                                                fill="blue",
                                                )
        self.hand_slot3 = canvas.create_rectangle(465,
                                                690,
                                                465+slotwidth,
                                                690+slotheight,
                                                fill="blue",
                                                )
        self.hand_slot4 = canvas.create_rectangle(585,
                                                690,
                                                585+slotwidth,
                                                690+slotheight,
                                                fill="blue",
                                                )
        self.hand_slot5 = canvas.create_rectangle(705,
                                                690,
                                                705+slotwidth,
                                                690+slotheight,
                                                fill="blue",
                                                )
        self.hand_slot6 = canvas.create_rectangle(825,
                                                690,
                                                825+slotwidth,
                                                690+slotheight,
                                                fill="blue",
                                                )
        self.hand_slot7 = canvas.create_rectangle(945,
                                                690,
                                                945+slotwidth,
                                                690+slotheight,
                                                fill="blue",
                                                )
        self.hand_slot8 = canvas.create_rectangle(1065,
                                                690,
                                                1065+slotwidth,
                                                690+slotheight,
                                                fill="blue",
                                                )
        self.card_positions=[230,350,470,590,710,830,950,1070]
        self.cards=[]
    
    def fill_hand(self, tavern, num_cards=8):
        """Draw cards from the tavern to fill up the hand slots"""
        self.cards.clear()
        for pos in self.card_positions[:num_cards]:
            card_obj = tavern.draw_card()
            if not card_obj:
                break  # tavern empty
            card_obj.set_x(pos)
            card_obj.set_y(self.y + 15)

            self.canvas.coords(card_obj.character_id, card_obj.get_x(), card_obj.get_y())
            self.canvas.tag_raise(card_obj.character_id)

            self.cards.append(card_obj)


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


suits = ["diamonds", "hearts", "clubs", "spades"]
ranks = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "ace", "jack", "queen", "king"]

super_cards=[]
for suit in suits:
    for rank in ranks:
        temp_card = card(game_canvas, rank, suit, 105, 144, -200, -200)  
        super_cards.append(temp_card)

cards = []
played_cards = []
tavern1=tavern(game_canvas, super_cards, 69, 695, 102, 144)
enemy1=enemy(game_canvas, "king", 598, 90, "diamonds", 204, 288)
enemy1.update_health_bar()
hand1=hand(game_canvas, 220, 680, 965, 184)
hand1.fill_hand(tavern1)

played_hand1 = played_hand(game_canvas, 452, 475, 500, 184)

discard = discard_pile(game_canvas, 1300, 800, 105, 154)  # x,y is center
def discard_random(event=None):
    while played_hand1.cards:
        card_obj = played_hand1.cards.pop(0)   
        discard.add_card(card_obj)



discard_btn = tk.Button(game_screen, text="discard", command=discard_random)
discard_btn.place(x=960, y=615)  

lose_btn = tk.Button(game_screen, text="lose", command=lambda: show_frame(lose_menu))
lose_btn.place(x=960, y=575)  

pause_btn = tk.Button(game_screen, text="pause", command=lambda: show_frame(pause_menu))
pause_btn.place(x=960, y=535)  

win_btn = tk.Button(game_screen, text="win", command=lambda: show_frame(win_menu))
win_btn.place(x=960, y=495)  

show_frame(main_menu)
# Run the Tkinter event loop
root.mainloop()
