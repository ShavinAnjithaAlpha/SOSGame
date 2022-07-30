from tkinter import *
from PIL import ImageTk, Image


class SOSGame(Tk):
    def __init__(self):
        super(SOSGame, self).__init__()
        self.title("SOS Game")
        self.geometry("1000x800+0+0")
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
        self.n = 15
        # create the frame
        self.frame1 = Frame(self, bg="black")
        self.frame1.grid(row=1, column=0, padx=80, pady=10)

        # create the canvas
        self.canvas_display = Canvas(self, width=self.w, height="130", bd=0, highlightthickness=0, bg="black")
        self.canvas_display.grid(row=0, column=0)

        self.canvas_score = Canvas(self, width=200, height=self.h+130, bd=0, highlightthickness=0, bg="black")
        self.canvas_score.grid(row=0, column=1, rowspan=2)

        # load the image for background of canvas_score
        global wallpaper
        wallpaper = ImageTk.PhotoImage(Image.open("background.jpg").resize((200, 630), Image.ANTIALIAS))
        # set the background the canvas_score
        self.canvas_score.create_image(0, 0, image=wallpaper, anchor="nw")

        # create partner boxes
        self.create_partner_boxes()

        # create the new game
        self.create_newgame()

    def create_partner_boxes(self):

        # box for X
        #for i in range(self.n)
        self.canvas_display.create_rectangle(100, 20, 200, 120, fill="#173ebd", outline="#173ebd", tag="X", width="5")
        self.canvas_display.create_text(150, 70, text="X", font=("Helvetica", 30), fill="white")

        # box for O
        self.canvas_display.create_rectangle(300, 20, 400, 120, fill="#173ebd", outline="#173ebd", tag="O", width="5")
        self.canvas_display.create_text(350, 70, text="O", font=("Helvetica", 30), fill="white")

    def create_newgame(self):
        self.canvas_score.delete("score")

        self.buttons = {}
        # create the buttons dictionary
        for i in range(0, self.n):
            for j in range(0, self.n):
                self.buttons[f"{i}|{j}"] = Button(self.frame1, text="", bd=1, width=3, bg="#15e56d",
                                                 activebackground="#0abf57",
                                                 font=('Helvetica', 14),
                                                 command=lambda e=[i, j]: self.clicked_on_button(e[0], e[1]))
                self.buttons[f"{i}|{j}"].grid(row=j, column=i)

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

        # create the new empyt list for save previous crosses
        self.pre_crosses = []
        # set the score to empty list
        self.scores = {"X" : 0,
                        "O" : 0}

        self.update_score("_")

    def clicked_on_button(self, i ,j):
        # if partner is X button text create as the X
        if self.buttons[f"{i}|{j}"]["text"] == "":
            if self.partner == "X":
                self.buttons[f"{i}|{j}"]["text"] = "X"
                self.partner = "O"
                # self.update_boxes("O")
            elif self.partner == "O":
                self.buttons[f"{i}|{j}"]["text"] = "O"
                self.partner = "X"
                # self.update_boxes("X")

        # get this info to list
        self.getinfo(i, j)
        # check for the win
        self.check_validpattern()
        self.update_boxes()

    def update_boxes(self): # previous get the s var

        if self.partner == "X":
            self.canvas_display.itemconfigure("X", outline="green2")
            self.canvas_display.itemconfigure("O", outline="#173ebd")
        elif self.partner == "O":
            self.canvas_display.itemconfigure("O", outline="green2")
            self.canvas_display.itemconfigure("X", outline="#173ebd")

    def getinfo(self, i, j):
        # update the matrix for i and j point
        self.XO_matrix[j][i] = self.buttons[f"{i}|{j}"]["text"]

    def check_validpattern(self):

        # instance variable for check the win scores
        win_var = 0

        # first check by row
        for j in range(0, self.n):
            for i in range(0, self.n-2):
                if (self.XO_matrix[j][i] == self.XO_matrix[j][i+1] == self.XO_matrix[j][i+2] != "_") and not([[j, i], [j, i+1], [j, i+2]] in self.pre_crosses):
                    self.update_score(self.XO_matrix[j][i])
                    # highlight the thoose buttons
                    l = [[j,i ], [j ,i+1], [j, i+2]]
                    for e in l:
                        self.buttons[f"{e[1]}|{e[0]}"]["bg"] = "red"
                    # append the this pattern to pre_crosses list
                    self.pre_crosses.append(l)
                    win_var += 1
                    # self.after(2000, self.create_newgame)


        for i in range(0, self.n):
            for j in range(0, self.n-2):
                if (self.XO_matrix[j][i] == self.XO_matrix[j+1][i] == self.XO_matrix[j+2][i] != "_") and not([[j, i], [j+1, i], [j+2, i]] in self.pre_crosses):
                    # display the winner
                    self.update_score(self.XO_matrix[j][i])
                    # highlight the thoose buttons
                    l = [[j, i],[j+1, i], [j+2, i]]
                    for e in l:
                        self.buttons[f"{e[1]}|{e[0]}"]["bg"] = "red"
                    self.pre_crosses.append(l)
                    win_var += 1


        # check for win for across by angled
        for k in range(0, self.n-2):
            i = k
            for j in range(0, self.n-2-k):
                if (self.XO_matrix[j][i] == self.XO_matrix[j+1][i+1] == self.XO_matrix[j+2][i+2] != "_") and not([[j, i], [j+1, i+1], [j+2, i+2]] in self.pre_crosses):
                    self.update_score(self.XO_matrix[j][i])
                    l = [[j, i], [j+1, i+1], [j+2, i+2]]
                    for e in l:
                        self.buttons[f"{e[1]}|{e[0]}"]["bg"] = "red" 
                    self.pre_crosses.append(l)
                    win_var += 1
                i += 1

        for h in range(1, self.n-2):
            j = h
            for i in range(0, self.n-2-h):
                if (self.XO_matrix[j][i] == self.XO_matrix[j+1][i+1] == self.XO_matrix[j+2][i+2] != "_") and not([[j, i], [j+1, i+1], [j+2, i+2]] in self.pre_crosses):
                    self.update_score(self.XO_matrix[j][i])
                    l = [[j, i], [j+1, i+1], [j+2, i+2]]
                    for e in l:
                        self.buttons[f"{e[1]}|{e[0]}"]["bg"] = "red"
                    self.pre_crosses.append(l)
                    win_var += 1
                j += 1

        for g in range(self.n-1, 1, -1):
            i = g
            for j in range(0, g-1):
                if (self.XO_matrix[j][i] == self.XO_matrix[j+1][i-1] == self.XO_matrix[j+2][i-2] != "_") and not([[j, i], [j+1, i-1], [j+2, i-2]] in self.pre_crosses):
                    self.update_score(self.XO_matrix[j][i])
                    l = [[j, i], [j+1, i-1], [j+2, i-2]]
                    for e in l:
                        self.buttons[f"{e[1]}|{e[0]}"]["bg"] = "red"
                    self.pre_crosses.append(l)
                    win_var += 1 
                i -= 1

        for v in range(1, self.n-2):
            j = v
            for i in range(self.n-1, 1+v, -1):
                if (self.XO_matrix[j][i] == self.XO_matrix[j+1][i-1] == self.XO_matrix[j+2][i-2] != "_") and not([[j, i], [j+1, i-1], [j+2, i-2]] in self.pre_crosses):
                    self.update_score(self.XO_matrix[j][i])
                    l = [[j, i], [j+1, i-1], [j+2, i-2]]
                    for e in l:
                        self.buttons[f"{e[1]}|{e[0]}"]["bg"] = "red"
                    self.pre_crosses.append(l)
                    win_var += 1
                j += 1

        if win_var > 0:
            # change the partner again
            if self.partner == "X":
                self.partner = "O"
            else:
                self.partner = "X"




        
    def update_score(self, s):

        # first update the score
        if s != "_":
            self.scores[s] += 5

        # thenn display the score in the canvas
        self.canvas_score.delete("scores")

        x_score = self.scores["X"]
        o_score = self.scores["O"]
        self.canvas_score.create_text(100, 150, text=f"X : {x_score}", font=('Helvetica', 35), fill="white", tag="scores")
        self.canvas_score.create_text(100, 450, text=f"O : {o_score}", font=('Helvetica', 35), fill="white", tag="scores")

        
if __name__ == "__main__":
    SOSGame().mainloop()