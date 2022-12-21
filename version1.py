"""
@autor: Jinga Andreea
"""
import random
import tkinter.messagebox
from tkinter import *

# colors
color_palette = dict()
color_palette['main_window_background_color'] = "thistle2"
color_palette['button_color'] = "thistle"
color_palette['active_button_color'] = "thistle3"
color_palette['frame_background'] = "thistle4"
color_palette['boardgame_background_color'] = "misty rose"
color_palette['random_colour'] = ["misty rose", "tomato2", "DarkOrchid3"]
color_palette['board'] = "burlywood4"
color_palette['hole'] = "wheat4"
color_palette['canvas_background'] = "burlywood2"

# dimensions
main_window_width = 1000
main_window_height = 500

# global variables
turn = "player_one"
holes = []
player_one_score = 0
player_two_score = 0
warning_unit = 0
turn_label = None
player_one_score_label = None
player_two_score_label = None


def is_game_over():
    """
    Functia specifica daca jocul s-a terminat, adica daca vreunul dintre jucatori are mai mult de 24 de
    pietre dintr-un total de 48.
    :return: Functia returneaza True daca jocul s-a terminat, adica daca avem un castigator, si False altfel.
    """
    global player_one_score, player_two_score
    if player_one_score >= 24:
        return True
    if player_two_score >= 24:
        return True
    return False


def show_winner(main_window):
    """
    Functia se ocupa cu stabilirea si afisarea castigatorului jocului. Pentru a stabili castigatorul verificam scorul
    actual al fiecarui jucator, castigator fiind cel care are peste 24 de puncte. Daca niciun jucator nu are peste 24
    de puncte atunci jocul s-a terminat fortat si fiecare jucator primeste pietrele de pe partea lui de tabla. Astfel
    stabilirea jucatorului se va face dupa efectuarea acestui calcul. La final fereastra BoardGame va fi inlocuita cu
    winner_frame
    :param main_window: o referinta care window-ul principal peste care se va pune winner_frame
    :return: fara tip de return.
    """
    global holes, player_one_score, player_two_score
    winner_frame = Frame(main_window, bg=color_palette['boardgame_background_color'], height=main_window_height,
                         width=main_window_width, highlightthickness=20,
                         highlightbackground=color_palette['boardgame_background_color'])
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

    winner_label = Label(winner_frame, text=winning_text, bg=color_palette['active_button_color'], padx=10, pady=2.5,
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
    """
    Functia verifica incalcarea regulii "Adversarul nu trebuie să fie niciodată înfometat". Conform acestei reguli daca
    adversarul ramane fara pietre in urma mutarii lui, jucatorul este obligat sa alega o mutare care sa ii ofere pietre
    adversarului pentru mutarea viitoare. Functia verifica daca adversarul de afla in situatie de informetare, iar in
    acest caz simuleaza mutarea pentru a verifica daca acesta se va afla in stare de infometare si dupa mutare.
    :param copy_holes: o copie a listei de casute si pietre pe care se va simula mutarea
    :param pressed_button: mutarea aleasa de jucator
    :param player: jucatorul care face mutarea
    :return: Functia returneaza True in cazul in care in urma mutarii adversarul este infometat, False altfel
    """
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
    """
    Sensul de mutare al pietrelor este contrar acelor de ceasornic. Astfel deplasarea in lista holes cu 12 elemente
    se va face urmand sensul indicilor: 6, 7, 8, 9, 10, 11, 5, 4, 3, 2, 1, 9. Aceasta functie da urmatoarea pozitie
    care urmeaza in acest sens al deplasarii.
    :param current_position: pozitia initiala pe care ne aflam
    :return: pozitia finala dupa deplasare
    """
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
    """
    Sensul de mutare al pietrelor este contrar acelor de ceasornic. Astfel deplasarea in lista holes cu 12 elemente
    se va face urmand sensul indicilor: 6, 7, 8, 9, 10, 11, 5, 4, 3, 2, 1, 9. Aceasta functie da pozitia anterioara, cea
    de pe care am ajuns pe pozitia curenta.
    :param current_position: pozitia pe care ne aflam la inceput
    :return: pozitia anterioara
    """
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
    """
    Functia calculeaza punctele castigate de jucator intr-o runda astfel: se considera puncte castigate pietrele din
    toate casutele consecutive, incepand cu ultima casuta modificata de jucator, care contin 2 sau 3 pietre. Toate
    casutele din care se calculeaza punctele trebuie sa fie ale adversarului.
    :param last_modified_hole_position: ultima casuta in care jucatorul a pus o piatra
    :param player: jucatorul care a facut mutarea
    :return: numarul de puncte castigate
    """
    global holes
    points = 0
    current_position = last_modified_hole_position
    if player == "player one":
        while 0 <= current_position <= 5:
            if 2 <= holes[current_position] <= 3:
                points += holes[current_position]
                holes[current_position] = 0
                current_position = get_previous_position_in_weird_circle(current_position)
            else:
                break
    else:
        while 6 <= current_position <= 11:
            if 2 <= holes[current_position] <= 3:
                points += holes[current_position]
                holes[current_position] = 0
                current_position = get_previous_position_in_weird_circle(current_position)
            else:
                break
    return points


def draw_holes(canvas):
    """
    Functia de ocupa cu desenarea initiala a casutelor cu pietre pe tabla de joc si de redesenarea acestora dupa fiecare
    modificare adusa numarului de pietre dintr-o casuta (adica dupa o mutare si dupa colectarea punctelor).
    :param canvas: o referinta catre obiectul Canvas pe care se vor desena casutele
    """
    global holes
    first_row_of_holes = []
    second_row_of_holes = []
    for i in range(0, 6):
        first_row_of_holes.append(canvas.create_oval(100 + i * 130, 100, 200 + i * 130, 200, fill=color_palette['hole']))
        second_row_of_holes.append(canvas.create_oval(100 + i * 130, 250, 200 + i * 130, 350, fill=color_palette['hole']))
    for i, hole in enumerate(holes):
        if 0 <= i <= 5:
            canvas.create_text(150 + i * 130, 150, text=str(hole), font=("Arial", 25, "bold"))
        else:
            canvas.create_text(150 + (i - 6) * 130, 300, text=str(hole), font=("Arial", 25, "bold"))


def move(starting_position, canvas, player):
    """
    Functia face mutarea efectiva a pietrelor din casuta selectata de jucator, respectand regula Kroo, conform careia
    nu se pun pietre in casuta din care s-a inceput mutarea. L-a final redeseneaza casutele si calculeaza punctele
    castigate.
    :param starting_position: pozitia aleasa de jucator pentru a muta
    :param canvas: o referinta de tip canvas pentru redesenare
    :param player: jucatorul care face mutarea
    :return: numarul de puncte castigate
    """
    global holes
    position_to_change = starting_position
    for i in range(0, holes[starting_position]):
        position_to_change = get_next_position_in_weird_circle(position_to_change)
        if position_to_change == starting_position:
            i -= 1
            continue
        holes[position_to_change] += 1
    holes[starting_position] = 0
    draw_holes(canvas)

    points = calculate_points(position_to_change, player)
    return points


def choose_to_move2(position_button, canvas, main_window):  # player two move
    """
    Functie apelata de jucatorul doi, corespunzand casutelor din partea de sus a tablei. Functia valideaza mutarea
    aleasa de jucator si afiseaza un mesaj de eroare corespunzator in caz de invaliditate. Daca miscarea este corecta
    realizarea mutarea efectiva a pietrelor si calculeaza punctajul obtinut.
    :param position_button: mutarea aleasa de jucatro
    :param canvas: o referinta la obiectul canvas pentru redesenarea casutelor
    :param main_window: o referinta la obiectul window pentru afisare castigatorului la final
    """
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
            # player_two_score_label.config(text=f"Player Two Score: {str(player_two_score)}")
            main_window.after(500, lambda: player_two_score_label.config(
                text=f"Player Two Score: {str(player_two_score)}"))
            draw_holes(canvas)

        if not is_game_over():
            turn = "player_one"
            turn_label.config(text="It is player one turn!")
        else:
            show_winner(main_window)


def choose_to_move1(position_button, canvas, main_window):  # player one move
    """
    Functie apelata de jucatorul doi, corespunzand casutelor din partea de sus a tablei. Functia valideaza mutarea
    aleasa de jucator si afiseaza un mesaj de eroare corespunzator in caz de invaliditate. Daca miscarea este corecta
    realizarea mutarea efectiva a pietrelor si calculeaza punctajul obtinut.
    :param position_button: mutarea aleasa de jucatro
    :param canvas: o referinta la obiectul canvas pentru redesenarea casutelor
    :param main_window: o referinta la obiectul window pentru afisare castigatorului la final
    """
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
            player_one_score_label.config(text=f"Player One Score: {str(player_one_score)}")
            # main_window.after(500, lambda: player_one_score_label.config(
            #     text=f"Player One Score: {str(player_one_score)}"))
            draw_holes(canvas)

        if not is_game_over():
            turn = "player_two"
            turn_label.config(text="It is player two turn!")
        else:
            show_winner(main_window)
        return True


def possible_moves_for_player2_aka_bot():
    """
    Functia realizeaza o lista de mutari valide pentru jucatorul doi cand acesta este repreentat de calculator.
    :return: lista de mutari valide
    """
    global holes
    possible_moves = []
    for i in range(0, 6):
        if valid_move(i)[0]:
            possible_moves.append(i)
    return possible_moves


def make_move_for_bot(canvas, main_window):
    """
    Functia se ocupa de mutarea pietrelor pentru jucatorul doi cand acesta este reprezentat de calculator. Calculatorul
    va alege random o miscare din cele valide, va muta si i se vor calcula punctele obtinute.
    :param canvas: o referinta la o variabila de tip canvas pentru desenarea casutelor
    :param main_window: o referinta la o variabila de tip window pentru afisarea castigatorului
    """
    global player_two_score, player_two_score_label, turn, turn_label
    bot_moves = possible_moves_for_player2_aka_bot()
    chosen_move = random.choice(bot_moves)

    points = move(chosen_move, canvas, "player two")
    if points != 0:
        player_two_score += points
        player_two_score_label.config(text=f"Player Two Score: {str(player_two_score)}")
        draw_holes(canvas)

    if not is_game_over():
        turn = "player_one"
        turn_label.config(text="It is player one turn!")
    else:
        show_winner(main_window)


def play_with_bot(position_button, canvas, main_window):  # player one move, then bot
    """
    Functia de ocupa de miscarile in jocul single-player. La apasarea unui buton de catre jucatorul 1, se va realizare
    mutarea, iar apoi se va realizare si mutarea calculatorului.
    :param position_button: mutarea aleasa de jucatorul 1
    :param canvas: o referinta la o variabila de tip canvas pentru desenarea casutelor
    :param main_window: o referinta la o variabila de tip window pentru afisarea castigatorului
    """
    global turn, turn_label
    success = choose_to_move1(position_button, canvas, main_window)
    if not success:
        return

    turn = "player_two"
    turn_label.config(text="Player two is moving...")

    main_window.after(4000, lambda: make_move_for_bot(canvas, main_window))


def draw_board(main_window, no_of_players):
    """
    Functia de ocupa de desenarea tablei de joc, a casutelor initializare cu cate 4 pietre si a butoanelor
    corespunzatoare fiecarei mutari alese de jucatori
    :param main_window: o referinta la o variabila de tip window pentru desenare
    :param no_of_players: numarul de jucatori, adica daca jocul va fi single-player sau multi-player
    """
    global holes, player_two_score, player_one_score, turn_label, player_one_score_label, player_two_score_label
    one_player_frame = Frame(main_window, bg=color_palette['boardgame_background_color'], height=main_window_height,
                             width=main_window_width, highlightthickness=20,
                             highlightbackground=color_palette['boardgame_background_color'])
    one_player_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    one_player_frame.tkraise()

    canvas = Canvas(main_window, bg=color_palette['canvas_background'], height=main_window_height - 90,
                    width=main_window_width - 100, highlightthickness=20,
                    highlightbackground=color_palette['canvas_background'])
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    canvas.create_rectangle(70, 80, 880, 220, fill=color_palette['board'])
    canvas.create_rectangle(70, 230, 880, 370, fill=color_palette['board'])
    canvas.create_rectangle(160, 215, 190, 235, fill=color_palette['board'])
    canvas.create_rectangle(190, 215, 220, 235, fill=color_palette['board'])
    canvas.create_rectangle(730, 215, 760, 235, fill=color_palette['board'])
    canvas.create_rectangle(760, 215, 790, 235, fill=color_palette['board'])
    draw_holes(canvas)

    buttons = []
    for i in range(0, 6):
        buttons.append(Button(canvas, text="Choose hole", bg=color_palette['button_color'],
                              activebackground=color_palette['active_button_color'], font=("Arial", 12, "bold"),
                              command=lambda position=i: choose_to_move2(position, canvas, main_window)))
        buttons[i].place(x=95 + 130 * i, y=40)
    for i in range(6, 12):
        buttons.append(Button(canvas, text="Choose hole", bg=color_palette['button_color'],
                              activebackground=color_palette['active_button_color'],
                              font=("Arial", 12, "bold"),
                              command=lambda position=i: choose_to_move1(position, canvas, main_window)
                              if no_of_players == 2 else play_with_bot(position, canvas, main_window)))
        buttons[i].place(x=95 + 130 * (i - 6), y=380)
    turn_label = Label(canvas, text="It is player One turn!", bg=color_palette['boardgame_background_color'])
    turn_label.place(x=10, y=10)

    player_one_score_label = Label(canvas, text=f"Player One Score: {str(player_one_score)}",
                                   bg=color_palette['boardgame_background_color'], font=("Arial", 10, "bold"))
    player_one_score_label.place(x=400, y=420)

    player_two_score_label = Label(canvas, text=f"Player Two Score: {str(player_two_score)}",
                                   bg=color_palette['boardgame_background_color'], font=("Arial", 10, "bold"))
    player_two_score_label.place(x=400, y=10)

    force_finnish_button = Button(canvas, text="Finnish the game now", bg=color_palette['button_color'],
                                  activebackground=color_palette['active_button_color'], font=("Arial", 10, "bold"),
                                  command=lambda: show_winner(main_window))
    force_finnish_button.place(x=780, y=417)


def init_game():
    """
    Functia initializeaza partea de logica din joc, adica lista de pietre si scorul fiecarui jucator
    """
    global holes, player_one_score, player_two_score
    for i in range(0, 12):              # 4 4 4 4 4 4 <- player2
        holes.append(4)                 # 4 4 4 4 4 4 <- player1
    player_one_score = 0
    player_two_score = 0


def one_player_game_init(main_window):
    """
    Functia initializeaza jocul cu un singur jucator, specificand numarul 1 in apelul functiei de desenare draw_board.
    :param main_window: o referinta la o variabila de tip window pentru desenare
    """
    global turn, holes
    init_game()
    draw_board(main_window, 1)


def two_players_game(main_window):
    """
        Functia initializeaza jocul cu doi jucatori, specificand numarul 2 in apelul functiei de desenare draw_board.
        :param main_window: o referinta la o variabila de tip window pentru desenare
        """
    global turn, holes
    init_game()
    draw_board(main_window, 2)


def init2():
    """
    Functia deseneaza fereastra de start a jocului in care se poate alege numarul de jucatori care vor juca
    :return: o referinta de tip window folosita ulterior pentru desenare
    """
    main_window = Tk()
    main_window.title("Mancala")
    main_window.geometry(f"{main_window_width}x{main_window_height}")
    main_window.config(bg=color_palette['main_window_background_color'])

    start_frame = Frame(main_window, bg=color_palette['frame_background'], height=main_window_height-50,
                        width=main_window_width/5, highlightthickness=40,
                        highlightbackground=color_palette['frame_background'])
    start_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    title_label = Label(start_frame, text="Welcome to Owale!", bg=color_palette['frame_background'], padx=10, pady=2.5,
                        font=("Lucida Calligraphy", 20, "bold"))
    title_label.grid(row=1, ipadx=10, ipady=10, columnspan=2)
    players_label = Label(start_frame, text="How many players will play?", bg=color_palette['frame_background'],
                          padx=10, pady=15, font=("Arial", 14))
    players_label.grid(row=2, ipadx=10, ipady=10, columnspan=2)

    one_player_button = Button(start_frame, text="One player!", bg=color_palette['button_color'],
                               activebackground=color_palette['active_button_color'],
                               font=("Arial", 12, "bold"), command=lambda: one_player_game_init(main_window))
    one_player_button.grid(row=3, column=0, ipadx=10, ipady=5, columnspan=1)
    two_players_button = Button(start_frame, text="Two players!", bg=color_palette['button_color'],
                                activebackground=color_palette['active_button_color'],
                                font=("Arial", 12, "bold"), command=lambda: two_players_game(main_window))
    two_players_button.grid(row=3, column=1, ipadx=10, ipady=5, columnspan=1)

    return main_window


def main():
    """
    Functia main a programului care porneste fereastra grafica.
    """
    main_window = init2()
    main_window.mainloop()


main()
