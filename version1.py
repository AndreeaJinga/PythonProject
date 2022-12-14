from tkinter import *
from tkinter import ttk
from tkinter import messagebox

background_color = "thistle2"
button_color = "thistle"
active_button_color = "thistle3"
frame_background = "thistle4"


def one_player_game(main_window):
    one_player_frame = Frame(main_window, bg="blue", height=450, width=200, highlightthickness=40,
                             highlightbackground="blue")
    one_player_frame.tkraise()


def two_players_game(main_window):
    messagebox.showinfo("Hello", "It works too!!!!")


def init():
    main_window = Tk()
    main_window.title("Mancala")
    main_window.geometry("1000x500")

    start_frame = Frame(main_window, bg=background_color, height=450, width=950)
    start_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # blank_label1 = Label(start_frame, text="", width=100, fg=background_color)
    # blank_label2 = Label(start_frame, text="", width=100)
    # blank_label1.grid(row=0, column=0, ipadx=10, ipady=10)
    # blank_label2.grid(row=0, column=2)
    title_label = Label(start_frame, text="Welcome to Owale!")
    title_label.grid(row=1, column=1, ipadx=10, ipady=10)
    players_label = Label(start_frame, text="How many players will play?")
    players_label.grid(row=2, column=1, ipadx=10, ipady=10)

    one_player_button = Button(start_frame, text="One player!", fg="black")
    one_player_button.grid(row=3, column=1, ipadx=10, ipady=10)
    two_players_button = Button(start_frame, text="Two players!", fg="black")
    two_players_button.grid(row=4, column=1, ipadx=10, ipady=10)

    return main_window


def init2():
    main_window = Tk()
    main_window.title("Mancala")
    main_window.geometry("1000x500")
    main_window.config(bg=background_color)

    start_frame = Frame(main_window, bg=frame_background, height=450, width=200, highlightthickness=40,
                        highlightbackground=frame_background)
    start_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    title_label = Label(start_frame, text="Welcome to Owale!", bg=frame_background, padx=10, pady=2.5,
                        font=("Lucida Calligraphy", 20, "bold"))
    title_label.grid(row=1, ipadx=10, ipady=10, columnspan=2)
    players_label = Label(start_frame, text="How many players will play?", bg=frame_background, padx=10, pady=15,
                          font=("Arial", 14))
    players_label.grid(row=2, ipadx=10, ipady=10, columnspan=2)

    one_player_button = Button(start_frame, text="One player!", bg=button_color, activebackground=active_button_color,
                               font=("Arial", 12, "bold"), command=lambda: one_player_game(main_window))
    one_player_button.grid(row=3, column=0, ipadx=10, ipady=5, columnspan=1)
    two_players_button = Button(start_frame, text="Two players!", bg=button_color, activebackground=active_button_color,
                                font=("Arial", 12, "bold"), command=lambda: two_players_game(main_window))
    two_players_button.grid(row=3, column=1, ipadx=10, ipady=5, columnspan=1)

    return main_window


def main():
    main_window = init2()
    main_window.mainloop()


main()
