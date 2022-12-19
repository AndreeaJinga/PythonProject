import time
from tkinter import *
# from tkinter import ttk
# from tkinter import messagebox

# TODO PALETAR FRUMOS!!!!
# colors
main_window_background_color = "thistle2"
button_color = "thistle"
active_button_color = "thistle3"
frame_background = "thistle4"
boardgame_background_color = "misty rose"

# dimensions
main_window_width = 1000
main_window_height = 500

# global variables
turn = "player_one"
turn_label = Label(None)
holes = []
player_one_score = 0
player_one_score_label = Label(None)
player_two_score = 0
player_two_score_label = Label(None)
warning_unit = 0


# TODO FOR TODAY: set-up pentru logica <-> initializarea jocului <-> apel func dupa draw_board;
#  facut functia de move + de spefic ce validari ar fi de facut;
#  de stabilit cum va arata final
def valid_move(pressed_button):
    global turn
    if 0 <= pressed_button <= 5 and turn == "player_two":
        return True
    if 6 <= pressed_button <= 11 and turn == "player_one":
        return True
    return False


def get_next_position_in_weird_circle(current_position):
    position_to_change = 0
    if 6 <= current_position <= 10:
        position_to_change = current_position + 1
    elif 1 <= current_position <= 5:
        position_to_change = current_position - 1
    elif current_position == 0:
        position_to_change = 6
    elif current_position == 11:
        position_to_change = 5
    return position_to_change


def calculate_points(last_modified_hole_position):
    points = 0
    return points


def draw_holes(canvas, init_flag):
    global holes
    first_row_of_holes = []
    second_row_of_holes = []
    for i in range(0, 6):
        first_row_of_holes.append(canvas.create_oval(100 + i * 130, 100, 200 + i * 130, 200, fill="white"))
        second_row_of_holes.append(canvas.create_oval(100 + i * 130, 250, 200 + i * 130, 350, fill="white"))
    for i, hole in enumerate(holes):
        if 0 <= i <= 5:
            canvas.create_text(150 + i * 130, 150, text=str(hole), font=("Arial", 25, "bold"))
            # if not init_flag:  # it would be nice to do...
            #     time.sleep(0.5)
        else:
            canvas.create_text(150 + (i - 6) * 130, 300, text=str(hole), font=("Arial", 25, "bold"))
            # if not init_flag:
            #     time.sleep(0.5)


def move(starting_position, canvas):
    global holes
    position_to_change = starting_position
    for i in range(0, holes[starting_position]):
        position_to_change = get_next_position_in_weird_circle(position_to_change)
        if position_to_change == starting_position:
            continue
        holes[position_to_change] += 1
    holes[starting_position] = 0
    points = calculate_points(position_to_change)
    # TODO: caculate+points
    # TODO: draw_holes_number in functie
    draw_holes(canvas, False)
    return points


def choose_to_move2(position_button, canvas):  # player two move
    global player_two_score, player_two_score_label, turn, turn_label, warning_unit
    if not valid_move(position_button):
        turn_label.config(font=("Arial", 9+warning_unit, "bold"))
        warning_unit += 1
    else:
        warning_unit = 0
        turn_label.config(font=("Arial", 9))

        points = move(position_button, canvas)
        player_two_score += points
        player_two_score_label.config(text=f"Player Two Score: {str(player_two_score)}")

        turn = "player_one"
        turn_label.config(text="It is player one turn!")


def choose_to_move1(position_button, canvas):  # player one move
    global player_one_score, player_one_score_label, turn, turn_label, warning_unit
    if not valid_move(position_button):
        turn_label.config(font=("Arial", 9+warning_unit, "bold"))
        warning_unit += 1
    else:
        warning_unit = 0
        turn_label.config(font=("Arial", 9))

        points = move(position_button, canvas)
        player_one_score += points
        player_one_score_label.config(text=f"Player One Score: {str(player_one_score)}")

        turn = "player_two"
        turn_label.config(text="It is player two turn!")


def draw_board(main_window):
    global holes, player_two_score, player_one_score, turn_label, player_one_score_label, player_two_score_label
    one_player_frame = Frame(main_window, bg=boardgame_background_color, height=main_window_height,
                             width=main_window_width, highlightthickness=20,
                             highlightbackground=boardgame_background_color)
    one_player_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    one_player_frame.tkraise()

    canvas = Canvas(main_window, bg="white", height=main_window_height - 90, width=main_window_width - 100,
                    highlightthickness=20, highlightbackground="white")
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    # TODO: MAKE IT PRETTY - rectangles
    first_rectangle = canvas.create_rectangle(70, 80, 880, 220)
    second_rectangle = canvas.create_rectangle(70, 230, 880, 370)
    # first_row_of_holes = []
    # second_row_of_holes = []
    # for i in range(0, 6):
    #     first_row_of_holes.append(canvas.create_oval(100 + i * 130, 100, 200 + i * 130, 200))
    #     second_row_of_holes.append(canvas.create_oval(100 + i * 130, 250, 200 + i * 130, 350))
    # for i, hole in enumerate(holes):
    #     if 0 <= i <= 5:
    #         canvas.create_text(150 + i * 130, 150, text=str(hole), font=("Arial", 25, "bold"))
    #         if not init_flag:
    #             time.sleep(0.5)
    #     else:
    #         canvas.create_text(150 + (i-6) * 130, 300, text=str(hole), font=("Arial", 25, "bold"))
    #         if not init_flag:
    #             time.sleep(0.5)
    draw_holes(canvas, True)
    buttons = []
    for i in range(0, 6):
        buttons.append(Button(canvas, text="Choose hole", bg=button_color, activebackground=active_button_color,
                              font=("Arial", 12, "bold"),
                              command=lambda position=i: choose_to_move2(position, canvas)))
        buttons[i].place(x=95 + 130 * i, y=40)
    for i in range(6, 12):
        buttons.append(Button(canvas, text="Choose hole", bg=button_color, activebackground=active_button_color,
                              font=("Arial", 12, "bold"),
                              command=lambda position=i: choose_to_move1(position, canvas)))
        buttons[i].place(x=95 + 130 * (i - 6), y=380)
    turn_label = Label(canvas, text="It is player One turn!", bg=boardgame_background_color)
    turn_label.place(x=10, y=10)

    player_one_score_label = Label(canvas, text=f"Player One Score: {str(player_one_score)}",
                                   bg=boardgame_background_color, font=("Arial", 10, "bold"))
    player_one_score_label.place(x=400, y=420)

    player_two_score_label = Label(canvas, text=f"Player Two Score: {str(player_two_score)}",
                                   bg=boardgame_background_color, font=("Arial", 10, "bold"))
    player_two_score_label.place(x=400, y=10)
    return buttons, canvas


def init_game():
    global holes, player_one_score, player_two_score
    for i in range(0, 12):              # 4 4 4 4 4 4 <- player2
        holes.append(4)                 # 4 4 4 4 4 4 <- player1
    player_one_score = 0
    player_two_score = 0


# TODO
def a_player_cannot_move():
    global holes
    return False


# TODO: not used
def is_game_over():
    global player_one_score, player_two_score
    if player_one_score >= 24:
        return True
    if player_two_score >= 24:
        return True
    if a_player_cannot_move():
        return True
    return False


def one_player_game_init(main_window):
    global turn, holes
    init_game()
    buttons, canvas = draw_board(main_window)


# TODO
def two_players_game(main_window):
    global turn
    init_game()
    buttons, canvas = draw_board(main_window)


def init2():
    main_window = Tk()
    main_window.title("Mancala")
    main_window.geometry(f"{main_window_width}x{main_window_height}")
    main_window.config(bg=main_window_background_color)

    start_frame = Frame(main_window, bg=frame_background, height=main_window_height-50, width=main_window_width/5,
                        highlightthickness=40, highlightbackground=frame_background)
    start_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    title_label = Label(start_frame, text="Welcome to Owale!", bg=frame_background, padx=10, pady=2.5,
                        font=("Lucida Calligraphy", 20, "bold"))
    title_label.grid(row=1, ipadx=10, ipady=10, columnspan=2)
    players_label = Label(start_frame, text="How many players will play?", bg=frame_background, padx=10, pady=15,
                          font=("Arial", 14))
    players_label.grid(row=2, ipadx=10, ipady=10, columnspan=2)

    one_player_button = Button(start_frame, text="One player!", bg=button_color, activebackground=active_button_color,
                               font=("Arial", 12, "bold"), command=lambda: one_player_game_init(main_window))
    one_player_button.grid(row=3, column=0, ipadx=10, ipady=5, columnspan=1)
    two_players_button = Button(start_frame, text="Two players!", bg=button_color, activebackground=active_button_color,
                                font=("Arial", 12, "bold"), command=lambda: two_players_game(main_window))
    two_players_button.grid(row=3, column=1, ipadx=10, ipady=5, columnspan=1)

    return main_window


def main():
    main_window = init2()
    main_window.mainloop()


main()
