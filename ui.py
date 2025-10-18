import tkinter as tk
from PIL import Image, ImageTk
import random

S = 'spades'
C = 'clubs'
D = 'diamonds'
H = 'hearts'
SUITS = [S, C, D, H]
base_atk = 0

# creating the initial window
root = tk.Tk()
root.geometry("1400x1000")
root.title("regicide")
root.config(bg="grey")

FRAME_WIDTH = 1400
FRAME_HEIGHT = 1000

def safe_bind(canvas, item_id, sequence, func):
    try:
        canvas.tag_bind(item_id, sequence, func)
    except Exception:
        pass

def safe_unbind(canvas, item_id, sequence):
    try:
        canvas.tag_unbind(item_id, sequence)
    except Exception:
        pass

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
            text="",
            font=("Arial", 16, "bold"),
            fill="white"
        )

    def update_label(self, number):
        self.canvas.itemconfig(self.label_id, text=str(number))

def sortHand(hand):
    sorting_dict = {S: [], C: [], D: [], H: []}
    for card in hand:
        sorting_dict[card.suit].append(card)
    for suit in sorting_dict:
        sorting_dict[suit] = sorted(sorting_dict[suit], key=lambda c: c.rank)
    return sorting_dict[S] + sorting_dict[C] + sorting_dict[D] + sorting_dict[H]

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
        if played[0].rank == 1 or played[1].rank == 1:
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
    next_enemy = castle.pop()

    if current_enemy:
        canvas.delete(current_enemy.health_bar_bg)
        canvas.delete(current_enemy.health_bar)
        canvas.delete(current_enemy.hp_label.label_id)
        enemy_attack.update_label(next_enemy.atk)

    canvas.coords(next_enemy.character_id, 598, 90)

    next_enemy.health_bar_bg = canvas.create_rectangle(
        450, 50, 950, 70, fill="black"
    )
    next_enemy.health_bar = canvas.create_rectangle(
        450, 50, 450 + 500 * (next_enemy.hp / next_enemy.max_hp), 70, fill="green"
    )

    next_enemy.hp_label = AttackLabel(canvas, 650, 0, 100, 30)

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

    enemy_isAlive = True
    heart_flag = False
    diamond_flag = False
    club_flag = False
    spade_flag = False

    print(f"pre: tavern: {len(tavern1.cards)}, hand: {len(hand1.cards)}, discard: {len(discard.cards)}, hp: {current_enemy.hp}, atk: {current_enemy.atk}")
    print(f"Hand {hand1.cards}, played {played_hand1.cards}")

    original_base_atk = base_atk
    club_flag = False

    # First pass: check for club
    for c in played_hand1.cards:
        if c.suit == C and not club_flag and current_enemy.suit != C:
            club_flag = True

    # Second pass: apply effects using original_base_atk
    for c in played_hand1.cards:
        if c.suit == H and not heart_flag and current_enemy.suit != H:
            tavern1.heal(discard, original_base_atk)
            heart_flag = True
        if c.suit == D and not diamond_flag and current_enemy.suit != D:
            hand1.fill_hand(tavern1, original_base_atk)
            diamond_flag = True
        if c.suit == S and not spade_flag and current_enemy.suit != S:
            reduction = original_base_atk
            current_enemy.atk = 0 if current_enemy.atk - reduction < 0 else current_enemy.atk - reduction
            enemy_attack.update_label(current_enemy.atk)
            spade_flag = True

    # Calculate damage
    damage = original_base_atk * 2 if club_flag else original_base_atk

    # Attack enemy
    current_enemy.hp = current_enemy.hp - damage
    current_enemy.update_health_bar()

    if current_enemy.hp == 0:
        tavern1.cards.append(current_enemy)
        game_canvas.coords(current_enemy.character_id, -200, -200)
        current_enemy = reveal_next_enemy(game_canvas, castle, current_enemy)
        current_enemy.update_health_bar()
        enemy_isAlive = False
    elif current_enemy.hp < 0:
        discard.add_card(current_enemy)
        current_enemy = reveal_next_enemy(game_canvas, castle, current_enemy)
        current_enemy.update_health_bar()
        enemy_isAlive = False

    # Move played cards to discard
    while len(played_hand1.cards) > 0:
        discard.add_card(played_hand1.cards.pop())

    base_atk = 0
    print(f"post: tavern: {len(tavern1.cards)}, hand: {len(hand1.cards)}, discard: {len(discard.cards)}, hp: {current_enemy.hp}, atk: {current_enemy.atk} ")
    print(f"Hand {hand1.cards}, played {played_hand1.cards}")

    if enemy_isAlive and current_enemy.atk > 0:
        play_btn.configure(text="Defend", command=lambda: defend())
    player_attack.update_label(0)

    # Lower any raised cards unless diamonds just drew
    for c in hand1.cards:
        if ((isinstance(c, card) or isinstance(c, enemy))) and c.raised and not diamond_flag:
            c.set_y(c.get_y() + 20)
            game_canvas.move(c.character_id, 0, +20)
            if getattr(c, 'border_id', None):
                game_canvas.move(c.border_id, 0, +20)
        c.raised = False
    hand1.update_positions()
cumulative_blocked = 0

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
    global jesters

    incoming_damage = current_enemy.atk
    for _ in range(len(played_hand1.cards)):
        c = played_hand1.cards.pop()
        cumulative_blocked = cumulative_blocked + c.rank
        discard.add_card(c)

    if cumulative_blocked >= incoming_damage:
        play_btn.configure(text="Attack", command=lambda: attack())
        player_attack.update_label(0)
        base_atk = 0
        cumulative_blocked = 0
        hand1.update_positions()
        return
    elif cumulative_blocked < incoming_damage and len(hand1.cards) == 0 and jesters == 0:
        show_frame(lose_menu)
        hand1.update_positions()
        return
    hand1.update_positions()

def image_resize(file, width, height):
    og_image = Image.open(file)
    new_image = og_image.resize((width, height), Image.NEAREST)
    return ImageTk.PhotoImage(new_image)

class enemy():
    def __init__(self, canvas, rank, x, y, suit, width, height):
        self.width = width
        self.height = height
        self.suit = suit
        self.rank = rank
        self.max_hp = self.rank * 2
        self.hp = self.max_hp
        self.atk = rank
        self.canvas = canvas
        self.x = x
        self.y = y
        self.raised = False
        self.border_id = None

        self.filepath = f"enemies/{self.suit}/{self.rank} {self.suit}.png"
        self.image = image_resize(self.filepath, self.width, self.height)

        self.character_id = canvas.create_image(
            self.x,
            self.y,
            image=self.image,
            anchor="nw"
        )
        self.health_bar_bg = None
        self.health_bar = None
        self.hp_label = None
    
    def update_health_bar(self):
        width = 500 * (self.hp / self.max_hp)
        self.canvas.itemconfig(self.health_bar, fill="yellow")
        self.canvas.coords(self.health_bar, 450, 50, 450 + width, 70)
        if self.hp > self.max_hp / 2:
            self.canvas.itemconfig(self.health_bar, fill="green")
        elif self.hp > self.max_hp / 4:
            self.canvas.itemconfig(self.health_bar, fill="yellow")
        else:
            self.canvas.itemconfig(self.health_bar, fill="red")
        self.hp_label.update_label(f"{self.hp} / {self.max_hp}")

    def on_click(self, event):
        global base_atk
        global played_hand1
        global hand1
        global player_attack
        global current_enemy

        if self not in hand1.cards:
            return

        hand1.cards.remove(self)
        played_hand1.add_card(self)
        self.raised = False

        if play_btn.cget("text") == "Attack":
            combo_flag, combo_cards = checkCombo(played_hand1.cards, hand1.cards, base_atk)

            for c in hand1.cards:
                if ((isinstance(c, card) or isinstance(c, enemy))) and c.raised:
                    c.set_y(c.get_y() + 20)
                    c.canvas.move(c.character_id, 0, +20)
                    if getattr(c, 'border_id', None):
                        c.canvas.move(c.border_id, 0, +20)
                    c.raised = False

            if combo_flag:
                for c in combo_cards:
                    if (isinstance(c, card) or isinstance(c, enemy)) and not c.raised:
                        c.set_y(c.get_y() - 20)
                        c.canvas.move(c.character_id, 0, -20)
                        if getattr(c, 'border_id', None):
                            c.canvas.move(c.border_id, 0, -20)
                        c.raised = True

        base_atk = base_atk + self.rank

        displayed_attack = base_atk
        for c in played_hand1.cards:
            if c.suit == C and not current_enemy.suit == C:
                displayed_attack = base_atk * 2
                break
        player_attack.update_label(displayed_attack)
        print(f"Base Attack: {base_atk}")

        safe_bind(self.canvas, self.character_id, "<Button-1>", self.return_to_hand)
        hand1.update_positions()

    def set_x(self, new_x):
        self.x = new_x

    def get_x(self):
        return self.x

    def set_y(self, new_y):
        self.y = new_y

    def get_y(self):
        return self.y

    def return_to_hand(self, event):
        global base_atk
        global current_enemy
        self.raised = False
        if self in played_hand1.cards:
            played_hand1.cards.remove(self)
        base_atk = max(0, base_atk - self.rank)

        displayed_attack = base_atk
        for c in played_hand1.cards:
            if c.suit == C and not current_enemy.suit == C:
                displayed_attack = base_atk * 2
                break
        player_attack.update_label(displayed_attack)

        # Move back to tavern top, then refill 1 card to hand
        tavern1.cards.append(self)
        game_canvas.coords(self.character_id, -200, -200)
        hand1.fill_hand(tavern1, 1)

        safe_bind(self.canvas, self.character_id, "<Button-1>", self.on_click)

        combo_flag, combo_cards = checkCombo(played_hand1.cards, hand1.cards, base_atk)
        for c in hand1.cards:
            if (isinstance(c, card) or isinstance(c, enemy)) and c.raised:
                c.raised = False

        if combo_flag:
            for c in combo_cards:
                if (isinstance(c, card) or isinstance(c, enemy)) and not c.raised:
                    c.set_y(c.get_y() - 20)
                    c.canvas.move(c.character_id, 0, -20)
                    if getattr(c, 'border_id', None):
                        c.canvas.move(c.border_id, 0, -20)
                    c.raised = True

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
        if self.cards:
            card_obj = self.cards.pop()
            self.update_label()
            return card_obj
        return None

    def heal(self, discard, base_atk):
        # Shuffle discard pile (cards + references aligned)
        try:
            if not discard.cards or not discard.references:
                return
            temp = list(zip(discard.cards, discard.references))
            random.shuffle(temp)
            res1, res2 = zip(*temp) if temp else ([], [])
            discard.cards, discard.references = list(res1), list(res2)
        except ValueError:
            return

        for _ in range(base_atk):
            if not discard.cards:
                break
            next_card = discard.cards.pop()
            if discard.references:
                discard.references.pop()
            # Hide discard image (keep the original card’s canvas image intact)
            # Put card back to tavern
            self.cards.append(next_card)
            # Rebind click for hand usage later
            safe_bind(next_card.canvas, next_card.character_id, "<Button-1>", next_card.on_click)
        self.update_label()

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

        self.filepath = f"{self.suit}/{self.rank} {self.suit}.png"
        self.image = image_resize(self.filepath, self.width, self.height)

        self.character_id = canvas.create_image(
            self.x,
            self.y,
            image=self.image,
            anchor="nw"
        )
        safe_bind(self.canvas, self.character_id, "<Button-1>", self.on_click)

    def return_to_hand(self, event):
        global current_enemy
        global base_atk
        self.raised = False

        if self in played_hand1.cards:
            played_hand1.cards.remove(self)
        base_atk = max(0, base_atk - self.rank)

        displayed_attack = base_atk
        for c in played_hand1.cards:
            if c.suit == C and not current_enemy.suit == C:
                displayed_attack = base_atk * 2
                break
        player_attack.update_label(displayed_attack)

        tavern1.cards.append(self)
        game_canvas.coords(self.character_id, -200, -200)
        hand1.fill_hand(tavern1, 1)
        safe_bind(self.canvas, self.character_id, "<Button-1>", self.on_click)

        combo_flag, combo_cards = checkCombo(played_hand1.cards, hand1.cards, base_atk)

        for c in hand1.cards:
            if (isinstance(c, card) or isinstance(c, enemy)) and c.raised:
                c.raised = False

        if combo_flag:
            for c in combo_cards:
                if (isinstance(c, card) or isinstance(c, enemy)) and not c.raised:
                    c.set_y(c.get_y() - 20)
                    c.canvas.move(c.character_id, 0, -20)
                    if getattr(c, 'border_id', None):
                        c.canvas.move(c.border_id, 0, -20)
                    c.raised = True

    def on_click(self, event):
        global base_atk
        global played_hand1
        global hand1
        global player_attack
        global current_enemy
        self.raised = False

        if self not in hand1.cards:
            return

        hand1.cards.remove(self)
        played_hand1.add_card(self)
        hand1.update_positions()

        if play_btn.cget("text") == "Attack":
            combo_flag, combo_cards = checkCombo(played_hand1.cards, hand1.cards, base_atk)

            for c in hand1.cards:
                if (isinstance(c, card) or isinstance(c, enemy)) and c.raised:
                    c.set_y(c.get_y() + 20)
                    c.canvas.move(c.character_id, 0, +20)
                    if getattr(c, 'border_id', None):
                        c.canvas.move(c.border_id, 0, +20)
                    c.raised = False

            if combo_flag:
                for c in combo_cards:
                    if (isinstance(c, card) or isinstance(c, enemy)) and not c.raised:
                        c.set_y(c.get_y() - 20)
                        c.canvas.move(c.character_id, 0, -20)
                        if getattr(c, 'border_id', None):
                            c.canvas.move(c.border_id, 0, -20)
                        c.raised = True

        base_atk = base_atk + self.rank

        displayed_attack = base_atk
        if play_btn.cget("text") == "Attack":
            for c in played_hand1.cards:
                if c.suit == C and not current_enemy.suit == C:
                    displayed_attack = base_atk * 2
                    break
        player_attack.update_label(displayed_attack)
        print(f"Base Attack: {base_atk}")

        safe_bind(self.canvas, self.character_id, "<Button-1>", self.return_to_hand)

    def set_x(self, new_x): 
        self.x = new_x

    def get_x(self):
        return self.x

    def set_y(self, new_y):
        self.y = new_y

    def get_y(self):
        return self.y

    def __repr__(self):
        return str(self.rank) + self.suit

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
                                               x + width,
                                               y + height,
                                               fill="yellow",
                                               stipple="gray50"
                                               )
        self.card_positions = [470, 590, 710, 830]

    def add_card(self, card_obj):
        if len(self.cards) < len(self.card_positions):
            pos_x = self.card_positions[len(self.cards)]
            pos_y = self.y + 20

            card_obj.set_x(pos_x)
            card_obj.set_y(pos_y)

            self.canvas.coords(card_obj.character_id, pos_x, pos_y)

            safe_unbind(self.canvas, card_obj.character_id, "<Button-1>")

            self.canvas.tag_raise(card_obj.character_id)

            self.cards.append(card_obj)
        else:
            print("Played hand is full!")

    def clear(self):
        self.cards = []

class hand():
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height

        self.canvas = canvas
        self.x = x
        self.y = y
        self.slotwidth = 115
        self.slotheight = 154
        self.card_positions = [230, 350, 470, 590, 710, 830, 950, 1070]
        self.cards = []
        self.highlights = {}
        self.hand_bg = self.canvas.create_rectangle(self.x,
                                                    self.y,
                                                    self.x + self.width,
                                                    self.y + self.height,
                                                    fill="brown",
                                                    stipple="gray50"
                                                    )

    def update_positions(self):
        for idx, c in enumerate(self.cards):
            pos = self.card_positions[idx]
            c.set_x(pos)
            c.set_y(self.y + 15)
            self.canvas.coords(c.character_id, c.get_x(), c.get_y())
            self.canvas.tag_raise(c.character_id)
            c.raised = False
            if hasattr(c, 'border_id') and c.border_id:
                self.canvas.coords(c.border_id, c.get_x() - 2, c.get_y() - 2, c.get_x() + c.width + 2, c.get_y() + c.height + 2)

    def _prepare_card_for_hand(self, card_obj):
        # Ensure card has the correct size/image and click binding when entering hand
        target_w, target_h = 105, 144
        if getattr(card_obj, 'width', None) != target_w or getattr(card_obj, 'height', None) != target_h:
            card_obj.width = target_w
            card_obj.height = target_h
        # Refresh image to correct size, always safe
        card_obj.image = image_resize(card_obj.filepath, card_obj.width, card_obj.height)
        try:
            self.canvas.itemconfig(card_obj.character_id, image=card_obj.image)
        except Exception:
            # Card may have been removed; recreate if needed
            card_obj.character_id = self.canvas.create_image(-200, -200, image=card_obj.image, anchor="nw")
        safe_bind(card_obj.canvas, card_obj.character_id, "<Button-1>", card_obj.on_click)

    def fill_hand(self, tavern, num_cards=8):
        for _ in range(num_cards):
            if len(self.cards) >= 8:
                break
            card_obj = tavern.draw_card()
            if not card_obj:
                break
            # Prepare incoming card/enemy for hand zone
            if isinstance(card_obj, (card, enemy)):
                self._prepare_card_for_hand(card_obj)
            self.cards.append(card_obj)
        self.cards = sortHand(self.cards)
        self.update_positions()

    # Minimal highlight handlers to avoid attribute errors from key bindings
    def highlight_card(self, idx):
        idx = idx - 1
        if 0 <= idx < len(self.cards):
            c = self.cards[idx]
            if not getattr(c, 'border_id', None):
                c.border_id = self.canvas.create_rectangle(
                    c.get_x() - 2, c.get_y() - 2, c.get_x() + c.width + 2, c.get_y() + c.height + 2,
                    outline="gold", width=3
                )
            else:
                self.canvas.itemconfig(c.border_id, state="normal")

    def unhighlight_card(self, idx):
        idx = idx - 1
        if 0 <= idx < len(self.cards):
            c = self.cards[idx]
            if getattr(c, 'border_id', None):
                self.canvas.itemconfig(c.border_id, state="hidden")

class JokerWidget():
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height

        self.canvas = canvas
        self.x = x
        self.y = y

        self.hand_bg = canvas.create_rectangle(x,
                                               y,
                                               x + width,
                                               y + height,
                                               fill="red",
                                               stipple="gray50"
                                               )
        self.joker_widg_slots = [1165, 1275]
    def fill_jokers(self):
        for slot in self.joker_widg_slots:
            Joker(game_canvas, 100, 144, slot, 25)

# Add a global variable to track jokers
jesters = 2

def play_jester(joker_instance=None):
    global jesters
    global hand1
    global tavern1
    global discard
    global current_enemy

    if jesters > 0:
        # Move all hand cards to discard
        while hand1.cards:
            discard.add_card(hand1.cards.pop())
        # Refill hand to 8 cards
        hand1.fill_hand(tavern1, 8)
        jesters -= 1
        print("Jester Played! Jokers left:", jesters)
        print(f"post: tavern: {len(tavern1.cards)}, hand: {len(hand1.cards)}, discard: {len(discard.cards)}, hp: {current_enemy.hp}, atk: {current_enemy.atk} ")
        print(f"Hand {hand1.cards}, played {played_hand1.cards}")

        # Change the clicked joker's image to card back
        if joker_instance:
            card_back_img = image_resize("back/Card back.png", joker_instance.width, joker_instance.height)
            joker_instance.canvas.itemconfig(joker_instance.character_id, image=card_back_img)
            joker_instance.image = card_back_img
    else:
        print("No more jesters left!")

class Joker():
    def __init__(self, canvas, width, height, x, y):
        self.width = width
        self.height = height
        self.canvas = canvas
        self.x = x
        self.y = y

        self.image = image_resize('joker (larry).png', self.width, self.height)

        self.character_id = canvas.create_image(
            self.x,
            self.y,
            image=self.image,
            anchor="nw"
        )
        safe_bind(canvas, self.character_id, "<Button-1>", self.on_click)

    def on_click(self, event):
        play_jester(self)

class discard_pile():
    def __init__(self, canvas, x, y, width, height):
        self.width = width
        self.height = height
        self.cards = []
        self.canvas = canvas
        self.x = x
        self.y = y
        self.references = []  # list of PhotoImage references for the pile

        self.label = tk.Label(canvas, text="Discarded: 0", bg="grey", fg="white", font=("Arial", 14, "bold"))
        self.label.place(x=self.x, y=self.y + self.height // 2 + 10, anchor="n")

    def add_card(self, card_obj):
        # Unbind click from existing card
        safe_unbind(self.canvas, card_obj.character_id, "<Button-1>")

        # Create a rotated resized image for discard pile visualization
        try:
            img = Image.open(card_obj.filepath).resize((self.width, self.height), Image.NEAREST)
        except Exception:
            # Fallback to card back if missing asset
            img = Image.open("back/Card back.png").resize((self.width, self.height), Image.NEAREST)

        angle = random.randint(-20, 20)
        img = img.rotate(angle, expand=True)
        tk_img = ImageTk.PhotoImage(img)
        self.references.append(tk_img)

        # Draw discard sprite (separate from the card_obj's own image)
        self.canvas.create_image(self.x, self.y, image=tk_img, anchor="center")

        # Hide/move the original card image so it can be reused later without losing its PhotoImage reference
        try:
            self.canvas.coords(card_obj.character_id, -200, -200)
        except Exception:
            pass

        self.cards.append(card_obj)
        self.label.config(text=f"Discarded: {len(self.cards)}")

def show_frame(frame):
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
title = menu_canvas.create_image(500, 50, anchor="nw", image=title_img)

pause_canvas = tk.Canvas(pause_menu,
                         width=FRAME_WIDTH,
                         height=FRAME_HEIGHT,
                         bg="grey")
pause_canvas.pack()

pause_canvas.create_image(0, 0, anchor="nw", image=bg_image)
pause_img = image_resize('Pause.png', 400, 200)
pause_title = pause_canvas.create_image(500, 50, anchor="nw", image=pause_img)

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
win_title = win_canvas.create_image(500, 50, anchor="nw", image=win_img)

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
lose_title = lose_canvas.create_image(500, 50, anchor="nw", image=lose_img)

back_to_menu_btn = tk.Button(lose_menu,
                             text="Back to Main Menu",
                             font=("Arial", 14),
                             command=lambda: show_frame(main_menu))
back_to_menu_btn.place(x=600, y=200, height=50, width=200)

game_canvas = tk.Canvas(game_screen, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg="grey")
game_canvas.pack()
game_canvas.create_image(0, 0, anchor="nw", image=bg_image)

# Initialising deck
deck = []
for suit in SUITS:
    for r in range(1, 11):
        deck.append(card(game_canvas, r, suit, 105, 144, -200, -200))

random.shuffle(deck)
tavern1 = tavern(game_canvas, deck, 69, 695, 102, 144)

# Initialising Hand
hand1 = hand(game_canvas, 220, 680, 965, 178)
hand1.fill_hand(tavern1)

# Initialising Castle and current_enemy
castle = []
for rank in range(20, 5, -5):
    for suit in SUITS:
        castle.append(enemy(game_canvas, rank, -400, -400, suit, 204, 288))

kings = castle[:4]
queens = castle[4:8]
jacks = castle[8:12]

random.shuffle(kings)
random.shuffle(queens)
random.shuffle(jacks)

castle.clear()
castle = kings + queens + jacks

current_enemy = reveal_next_enemy(game_canvas, castle, None)
current_enemy.update_health_bar()

# Initialising Misc
played_hand1 = played_hand(game_canvas, 452, 475, 500, 184)
discard = discard_pile(game_canvas, 1300, 800, 105, 154)  # x,y is center

jokerwid = JokerWidget(game_canvas, 1160, 20, 220, 154)
jokerwid.fill_jokers()

enemy_attack = AttackLabel(game_canvas, 650, 340, 100, 30)
enemy_attack.update_label(current_enemy.atk)

player_attack = AttackLabel(game_canvas, 650, 405, 100, 30)
player_attack.update_label(0)

base_atk = 0
game_lost = False

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

# Key bindings for highlight/unhighlight (1..8)
root.bind("<KeyPress-1>", lambda e: hand1.highlight_card(1))
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
root.mainloop()