import random
import time
import tkinter.messagebox
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
holes = []
player_one_score = 0
player_two_score = 0
warning_unit = 0
turn_label = Label(None)
player_one_score_label = Label(None)
player_two_score_label = Label(None)

# TODO: de sters printurile


def is_game_over():
    global player_one_score, player_two_score
    if player_one_score >= 24:
        return True
    if player_two_score >= 24:
        return True
    return False


def show_winner(main_window):
    global holes, player_one_score, player_two_score
    winner_frame = Frame(main_window, bg=boardgame_background_color, height=main_window_height, width=main_window_width,
                         highlightthickness=20, highlightbackground=boardgame_background_color)
    winner_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    winner_frame.tkraise()

    winning_text = ""
    if player_one_score >= 24:
        winning_text = "The winner is PLAYER ONE!"
    elif player_two_score >= 24:
        winning_text = "The winner is PLAYER TWO!"
    else:
        for i in range(6, 12):
            player_one_score += holes[i]
        for i in range(0, 6):
            player_two_score += holes[i]
        winning_text = "After collecting all the stones,\nThe winner is PLAYER ONE!"
        if player_two_score > player_one_score:
            winning_text = "After collecting all the stones,\nThe winner is PLAYER TWO!"
        elif player_two_score == player_one_score:
            winning_text = "Well, we'll just have to call it a draw."

    winner_label = Label(winner_frame, text=winning_text, bg=active_button_color, padx=10, pady=2.5,
                         font=("Lucida Calligraphy", 30, "bold"))
    winner_label.place(relx=0.5, rely=0.5, anchor=CENTER)


def verify_breaking_rule(copy_holes, pressed_button, player):
    """
    Functia valideaza regula conform careia adversarul nu poate ramane fara pietre in urma adunarii punctelor obtinute
    dupa o mutare. Astfel simulam mutarea jucatorului si verificam la final starea casutelor adversarului, adica
    verificam la final ca macar o casuta a adversarului sa aiba pietre.
    :param copy_holes: o copie a listei holes, care tine evidenta pietrelor din casute
    :param pressed_button: mutarea care trebuie validata
    :param player: jucatorul care a facut mutarea
    :return: True in cazul in care regula este incalcata si False altfel
    """
    final_position = pressed_button
    for i in range(0, copy_holes[pressed_button]):
        final_position = get_next_position_in_weird_circle(final_position)
        if final_position == pressed_button:
            continue
        copy_holes[final_position] += 1
    if player == "player one":
        while 0 <= final_position <= 5:
            if 2 <= copy_holes[final_position] <= 3:
                copy_holes[final_position] = 0
                final_position = get_previous_position_in_weird_circle(final_position)
            else:
                break
        still_have_stones = False
        for i in range(0, 6):
            if copy_holes[i] != 0:
                still_have_stones = True
        if still_have_stones:
            return False
    else:
        while 6 <= final_position <= 11:
            if 2 <= copy_holes[final_position] <= 3:
                copy_holes[final_position] = 0
                final_position = get_previous_position_in_weird_circle(final_position)
            else:
                break
        still_have_stones = False
        for i in range(6, 12):
            if copy_holes[i] != 0:
                still_have_stones = True
        if still_have_stones:
            return False
    return True


def is_opponent_starving(copy_holes, pressed_button, player):
    if player == "player one":
        for i in range(0, 6):
            if copy_holes[i] != 0:
                return False
        final_position = pressed_button
        for i in range(0, copy_holes[pressed_button]):
            final_position = get_next_position_in_weird_circle(final_position)
            if final_position == pressed_button:
                continue
            copy_holes[final_position] += 1
        for i in range(0, 6):
            if copy_holes[i] != 0:
                return False
    else:
        for i in range(6, 12):
            if copy_holes[i] != 0:
                return False
        final_position = pressed_button
        for i in range(0, copy_holes[pressed_button]):
            final_position = get_next_position_in_weird_circle(final_position)
            if final_position == pressed_button:
                continue
            copy_holes[final_position] += 1
        for i in range(6, 12):
            if copy_holes[i] != 0:
                return False
    return True


def valid_move(pressed_button):
    """
    Functia valideaza o miscare pe care un jucator vrea sa o faca. Conform regulilor o miscare este
    valida daca jucatorul alege pietre din cadrul casutelor lui (de pe partea lui de tabla), daca
    acesta nu il lasa pe adversar fara pietre cu aceasta mutare, si daca nu il infometeaza pe adversar, adica el
    deja nu mai are pietre iar jucatorul este obligat sa-i ofere.
    :param pressed_button: Reprezinta pozitia casutei aleasa de jucator pentru a muta
    :return: Functia returneaza o tupla. Primul element al tuplei este True daca mutarea este valida,
    si False in caz contrar. Al doilea element al tuplei reprezinta un cod de eroare in caz ca mutarea
    nu este valida, pentru a afisa motivul in mod corespunzator, si None in caz de validitate.
    """
    global turn
    if 0 <= pressed_button <= 5 and turn == "player_two":
        if holes[pressed_button] == 0:
            return False, "empty hole"

        copy_holes = holes.copy()
        if is_opponent_starving(copy_holes, pressed_button, "player two"):
            return False, "starving"

        copy_holes = holes.copy()
        is_rule_broken = verify_breaking_rule(copy_holes, pressed_button, "player two")
        if is_rule_broken:
            return False, "rule break"

        return True, None
    if 6 <= pressed_button <= 11 and turn == "player_one":
        if holes[pressed_button] == 0:
            return False, "empty hole"

        copy_holes = holes.copy()
        if is_opponent_starving(copy_holes, pressed_button, "player one"):
            return False, "starving"

        copy_holes = holes.copy()
        is_rule_broken = verify_breaking_rule(copy_holes, pressed_button, "player one")
        if is_rule_broken:
            return False, "rule break"

        return True, None
    return False, "incorrect hole"


def get_next_position_in_weird_circle(current_position):
    position_to_change = current_position
    if 6 <= current_position <= 10:
        position_to_change = current_position + 1
    elif 1 <= current_position <= 5:
        position_to_change = current_position - 1
    elif current_position == 0:
        position_to_change = 6
    elif current_position == 11:
        position_to_change = 5
    return position_to_change


def get_previous_position_in_weird_circle(current_position):
    position_to_change = current_position
    if 7 <= current_position <= 11:
        position_to_change = current_position - 1
    elif 0 <= current_position <= 4:
        position_to_change = current_position + 1
    elif current_position == 5:
        position_to_change = 11
    elif current_position == 4:
        position_to_change = 0
    return position_to_change


def calculate_points(last_modified_hole_position, player):
    # print("calculate_points; position:", last_modified_hole_position)
    global holes
    # print("holes:", holes)
    points = 0
    current_position = last_modified_hole_position
    if player == "player one":
        # print("calculate points, player one turn")
        while 0 <= current_position <= 5:
            # print("current_pos: ", current_position)
            if 2 <= holes[current_position] <= 3:
                points += holes[current_position]
                holes[current_position] = 0
                current_position = get_previous_position_in_weird_circle(current_position)
            else:
                break
            # print("holes", holes)
    else:
        # print("calculate points, player two turn")
        while 6 <= current_position <= 11:
            # print("current_pos: ", current_position)
            if 2 <= holes[current_position] <= 3:
                points += holes[current_position]
                holes[current_position] = 0
                current_position = get_previous_position_in_weird_circle(current_position)
            else:
                break
            # print("holes", holes)
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


def move(starting_position, canvas, player):
    global holes
    position_to_change = starting_position
    for i in range(0, holes[starting_position]):
        position_to_change = get_next_position_in_weird_circle(position_to_change)
        if position_to_change == starting_position:
            i -= 1
            continue
        holes[position_to_change] += 1
    holes[starting_position] = 0
    draw_holes(canvas, False)

    points = calculate_points(position_to_change, player)
    return points


def choose_to_move2(position_button, canvas, main_window):  # player two move
    global player_two_score, player_two_score_label, turn, turn_label, warning_unit
    is_valid, error = valid_move(position_button)
    if not is_valid:
        if error == "incorrect hole":
            turn_label.config(font=("Arial", 9+warning_unit, "bold"))
            warning_unit += 1
        elif error == "rule break":
            tkinter.messagebox.showwarning(title="Rule break", message="You will leave your opponent without stones!")
        elif error == "starving":
            tkinter.messagebox.showwarning("Rule break", message="Your opponent is starving! You must give him stones!")
        elif error == "empty hole":
            tkinter.messagebox.showwarning(title="Empty hole", message="What are you supposed to move?!")
    else:
        warning_unit = 0
        turn_label.config(font=("Arial", 9))

        points = move(position_button, canvas, "player two")
        if points != 0:
            player_two_score += points
            main_window.after(1000, lambda: player_one_score_label.config(text=
                                                                          f"Player Two Score: {str(player_one_score)}"))

            draw_holes(canvas, False)

        if not is_game_over():
            turn = "player_one"
            turn_label.config(text="It is player one turn!")
        else:
            show_winner(main_window)


def choose_to_move1(position_button, canvas, main_window):  # player one move
    global player_one_score, player_one_score_label, turn, turn_label, warning_unit
    is_valid, error = valid_move(position_button)
    if not is_valid:
        if error == "rule break":
            tkinter.messagebox.showwarning(title="Rule break", message="You will leave your opponent without stones!")
        elif error == "starving":
            tkinter.messagebox.showwarning("Rule break", message="Your opponent is starving! You must give him stones!")
        elif error == "empty hole":
            tkinter.messagebox.showwarning(title="Empty hole", message="What are you supposed to move?!")
        elif error == "incorrect hole":
            turn_label.config(font=("Arial", 9 + warning_unit, "bold"))
            warning_unit += 1
        return False
    else:
        warning_unit = 0
        turn_label.config(font=("Arial", 9))

        points = move(position_button, canvas, "player one")
        if points != 0:
            player_one_score += points
            main_window.after(1000, lambda: player_one_score_label.config(text=
                                                                          f"Player One Score: {str(player_one_score)}"))
            draw_holes(canvas, False)

        if not is_game_over():
            turn = "player_two"
            turn_label.config(text="It is player two turn!")
        else:
            show_winner(main_window)
        return True


def possible_moves_for_player2_aka_bot():
    global holes
    possible_moves = []
    for i in range(0, 6):
        if valid_move(i)[0]:
            possible_moves.append(i)
    return possible_moves


def make_move_for_bot(canvas, main_window):
    global player_two_score, player_two_score_label, turn, turn_label
    bot_moves = possible_moves_for_player2_aka_bot()
    chosen_move = random.choice(bot_moves)

    points = move(chosen_move, canvas, "player two")
    if points != 0:
        player_two_score += points
        player_two_score_label.config(text=f"Player Two Score: {str(player_two_score)}")
        draw_holes(canvas, False)

    if not is_game_over():
        turn = "player_one"
        turn_label.config(text="It is player one turn!")
    else:
        show_winner(main_window)


def play_with_bot(position_button, canvas, main_window):  # player one move, then bot
    global turn, turn_label
    success = choose_to_move1(position_button, canvas, main_window)
    if not success:
        return

    turn = "player_two"
    turn_label.config(text="Player two is moving...")

    main_window.after(4000, lambda: make_move_for_bot(canvas, main_window))


def draw_board(main_window, no_of_players):
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
    draw_holes(canvas, True)
    buttons = []
    for i in range(0, 6):
        buttons.append(Button(canvas, text="Choose hole", bg=button_color, activebackground=active_button_color,
                              font=("Arial", 12, "bold"),
                              command=lambda position=i: choose_to_move2(position, canvas, main_window)))
        buttons[i].place(x=95 + 130 * i, y=40)
    for i in range(6, 12):
        buttons.append(Button(canvas, text="Choose hole", bg=button_color, activebackground=active_button_color,
                              font=("Arial", 12, "bold"),
                              command=lambda position=i: choose_to_move1(position, canvas, main_window)
                              if no_of_players == 2 else play_with_bot(position, canvas, main_window)))
        buttons[i].place(x=95 + 130 * (i - 6), y=380)
    turn_label = Label(canvas, text="It is player One turn!", bg=boardgame_background_color)
    turn_label.place(x=10, y=10)

    player_one_score_label = Label(canvas, text=f"Player One Score: {str(player_one_score)}",
                                   bg=boardgame_background_color, font=("Arial", 10, "bold"))
    player_one_score_label.place(x=400, y=420)

    player_two_score_label = Label(canvas, text=f"Player Two Score: {str(player_two_score)}",
                                   bg=boardgame_background_color, font=("Arial", 10, "bold"))
    player_two_score_label.place(x=400, y=10)

    force_finnish_button = Button(canvas, text="Finnish the game now", bg=button_color,
                                  activebackground=active_button_color, font=("Arial", 10, "bold"),
                                  command=lambda: show_winner(main_window))
    force_finnish_button.place(x=780, y=417)

    return buttons, canvas


def init_game():
    global holes, player_one_score, player_two_score
    for i in range(0, 12):              # 4 4 4 4 4 4 <- player2
        holes.append(4)                 # 4 4 4 4 4 4 <- player1
    player_one_score = 0
    player_two_score = 0


def one_player_game_init(main_window):
    global turn, holes
    init_game()
    buttons, canvas = draw_board(main_window, 1)


def two_players_game(main_window):
    global turn, holes
    init_game()
    buttons, canvas = draw_board(main_window, 2)


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
