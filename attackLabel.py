
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

attack1=AttackLabel(game_canvas, 650, 375, 100, 30)