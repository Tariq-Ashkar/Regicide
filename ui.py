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

game_screen = tk.Frame(root, width=FRAME_WIDTH, height=FRAME_HEIGHT)
game_screen.pack(fill="both", expand=True)
canvas = tk.Canvas(game_screen, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg="grey")
canvas.pack()



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
    def __init__(self, canvas, max_cards, x, y, width, height):
            self.width = width
            self.height = height
            self.max_cards = max_cards
            self.cards = self.max_cards
            self.canvas = canvas
            self.x = x
            self.y = y
            file_path = "back/Card back.png"
            self.image = image_resize(file_path, self.width, self.height)

            self.character_id = canvas.create_image(
                                                        self.x,
                                                        self.y,
                                                        image=self.image,
                                                        anchor="nw"
                                                    )
class card():
    def __init__(self, canvas, rank, suit, width, height, x, y):
        self.width = width
        self.height = height
        self.suit = suit
        self.rank = rank
        self.canvas = canvas
        self.x=x
        self.y=y


        
        file_path = f"{self.suit}/{self.rank} {self.suit}.png"

        
        self.image = image_resize(file_path, self.width, self.height)

        # draw sprite
        self.character_id = canvas.create_image(
                                                    self.x,
                                                    self.y,
                                                    image=self.image,
                                                    anchor="nw"
                                                )
        


class hand():
    def __init__(self, canvas, cards, x, y, width, height):
        self.width = width
        self.height = height
        self.cards = cards
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


def show_frame(frame):
    '''
    raises the desired frame to the front

    the parameter is the desired frame
    '''
    frame.tkraise()

suits = ["diamonds", "hearts", "clubs", "spades"]
ranks = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "ace", "jack", "queen", "king"]
for suit in suits:
    for rank in ranks:
        pass
        



cards = []
tavern1=tavern(canvas, 52, 69, 695, 102, 144)
enemy1=enemy(canvas, "king", 598, 90, "diamonds", 204, 288)
enemy1.update_health_bar()
hand1=hand(canvas, cards, 220, 675, 965, 184)
temp_card=card(canvas, rank, suit, 105, 144, 230, 695)

# Run the Tkinter event loop
root.mainloop()
