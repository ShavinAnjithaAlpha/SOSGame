from tkinter import *


class SOSGame(Tk):
    def __init__(self):
        super(SOSGame, self).__init__()
        self.title("SOS Game")
        self.geometry("500x600+250+100")
        self.config(bg="black")

        # create menu
        self.main_menu = Menu(self)
        self.config(menu = self.main_menu)

        self.file_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="New game", command=self.create_newgame)
        self.file_menu.add_command(label="Exit", command=lambda :self.destroy())

        self.w = 500
        self.h = 500
        self.n = 3
        # create the frame
        self.frame1 = Frame(self, bg="black")
        self.frame1.grid(row=1, column=0, padx=80, pady=10)

        # create the canvas
        self.canvas_display = Canvas(self, width=self.w, height="130", bd=0, highlightthickness=0, bg="black")
        self.canvas_display.grid(row=0, column=0)

        self.canvas_score = Canvas(self, width=self.w, height="130", bd=0, highlightthickness=0, bg="black")
        self.canvas_score.grid(row=2, column=0)

        # create partner boxes
        self.create_partner_boxes()

        # create the new game
        self.create_newgame()

    def create_partner_boxes(self):

        # box for X
        self.canvas_display.create_rectangle(100, 20, 200, 120, fill="#173ebd", outline="#173ebd", tag="X", width="5")
        self.canvas_display.create_text(150, 70, text="X", font=("Helvetica", 30), fill="white")

        # box for O
        self.canvas_display.create_rectangle(300, 20, 400, 120, fill="#173ebd", outline="#173ebd", tag="O", width="5")
        self.canvas_display.create_text(350, 70, text="O", font=("Helvetica", 30), fill="white")

    def create_newgame(self):
        self.canvas_score.delete("score")

        self.buttons = {}
        self.t = 100
        r = (self.w - 2 * self.t) / self.n
        q = (self.h - 2 * self.t) / self.n
        # create the buttons dictionary
        for i in range(0, self.n):
            for j in range(0, self.n):
                self.buttons[f"{i}{j}"] = Button(self.frame1, text="", bd=1, width=3, height=1, bg="#15e56d",
                                                 activebackground="#0abf57",
                                                 font=('Helvetica', 45),
                                                 command=lambda e=[i, j]: self.clicked_on_button(e[0], e[1]))
                self.buttons[f"{i}{j}"].grid(row=j, column=i)

        # defined the partner
        self.partner = "X"

        self.XO_matrix = []

        for i in range(0, self.n):
            sub_list = []
            for j in range(0, self.n):
                sub_list.append("_")
            self.XO_matrix.append(sub_list)

        # highlight the partner_1
        self.canvas_display.itemconfigure("X", outline="green2")

    def clicked_on_button(self, i ,j):
        # if partner is X button text create as the X
        if self.buttons[f"{i}{j}"]["text"] == "":
            if self.partner == "X":
                self.buttons[f"{i}{j}"]["text"] = "X"
                self.partner = "O"
                self.update_boxes("O")
            elif self.partner == "O":
                self.buttons[f"{i}{j}"]["text"] = "O"
                self.partner = "X"
                self.update_boxes("X")

        # get this info to list
        self.getinfo(i, j)
        # check for the win
        self.check_win()

    def update_boxes(self, s):

        if s == "X":
            self.canvas_display.itemconfigure("X", outline="green2")
            self.canvas_display.itemconfigure("O", outline="#173ebd")
        elif s == "O":
            self.canvas_display.itemconfigure("O", outline="green2")
            self.canvas_display.itemconfigure("X", outline="#173ebd")

    def getinfo(self, i, j):
        # update the matrix for i and j point
        self.XO_matrix[j][i] = self.buttons[f"{i}{j}"]["text"]

    def check_win(self):
        # first check by row
        for j in range(0, self.n):
            if self.XO_matrix[j][0] == self.XO_matrix[j][1] == self.XO_matrix[j][2] != "_":
                # display the winner
                self.display_winner(self.XO_matrix[j][0])
                # highlight the thoose buttons
                for i in range(0, self.n):
                    self.buttons[f"{i}{j}"]["bg"] = "red"
                self.after(2000, self.create_newgame)


        for i in range(0, self.n):
            if self.XO_matrix[0][i] == self.XO_matrix[1][i] == self.XO_matrix[2][i] != "_":
                # display the winner
                self.display_winner(self.XO_matrix[0][i])
                # highlight the thoose buttons
                for j in range(0, self.n):
                    self.buttons[f"{i}{j}"]["bg"] = "red"
                self.after(2000, self.create_newgame)


        # check for win for across by angled
        if self.XO_matrix[0][0] == self.XO_matrix[1][1] == self.XO_matrix[2][2] != "_":
            # display the winner
            self.display_winner(self.XO_matrix[0][0])
            l = [[0,0], [1,1], [2,2]]
            for i in l:
                self.buttons[f"{i[1]}{i[0]}"]["bg"] = "red"
            self.after(2000, self.create_newgame)

        if self.XO_matrix[0][2] == self.XO_matrix[1][1] == self.XO_matrix[2][0] != "_":
            # display the winner
            self.display_winner(self.XO_matrix[0][2])
            l = [[0, 2], [1, 1], [2, 0]]
            for i in l:
                self.buttons[f"{i[1]}{i[0]}"]["bg"] = "red"
            self.after(2000, self.create_newgame)

        # display the winner
        self.display_winner("_")

    def display_winner(self, s):

        if s == "X" or s == "O":
            self.canvas_score.create_text(self.w/2, 65, text=f"win {s}", font=('Helvetica', 40), fill="white", tag="score")
        else:
            s = 0
            for i in self.XO_matrix:
                for j in i:
                    if j != "_":
                        s += 1
            if s == self.n**2:
                self.canvas_score.create_text(self.w/2, 65, text="match draw", tag="score", font=('Helvetica', 40), fill="white")

if __name__ == "__main__":
    SOSGame().mainloop()