# Author: Carolynn Wicker
# GitHub username: wickerc
# Date: 03/18/2023
# Description: A class called Checkers that allows two people to play the game of Checkers and a class called Player
# that creates a player object in the game. This is a variation of the original Checkers game with modified rules.

class OutofTurn(Exception):
    """user-defined exception for if a player tries to move when it is not their turn"""
    pass


class InvalidSquare(Exception):
    """user-defined exception for if a player tries to move a piece that doesn't belong to them or to or from a square
    on the board that doesn't exist"""
    pass


class InvalidPlayer(Exception):
    """user-defined exception for if a player name entered to make a move is not a valid Player"""
    pass


class Checkers:
    """A variation of the original Checkers game with modified rules."""

    def __init__(self):
        """Initializing the game board to its starting position where no pieces have been moved yet."""
        self._board = [[None, "White", None, "White", None, "White", None, "White"],
                       ["White", None, "White", None, "White", None, "White", None],
                       [None, "White", None, "White", None, "White", None, "White"],
                       [None, None, None, None, None, None, None, None, ],
                       [None, None, None, None, None, None, None, None, ],
                       ["Black", None, "Black", None, "Black", None, "Black", None, ],
                       [None, "Black", None, "Black", None, "Black", None, "Black"],
                       ["Black", None, "Black", None, "Black", None, "Black", None, ]]
        self._players_turn = None
        self._players_list = []  # list of player names
        self._player_objects = []  # list of player objects

    def create_player(self, player_name, piece_color):
        """Uses composition to create a Player object that represents one of the two players in the game, using their
        name and the color piece they are playing with."""
        new_player = Player(player_name, piece_color)
        self._player_objects.append(new_player)  # adds the 2 players to a list of valid players
        self._players_list.append(player_name)
        if piece_color == "Black":  # initializes black pieces as first player in the game
            self._players_turn = player_name
        return new_player

    def get_players_turn(self):
        """Returns the name of the player who is to play the next turn"""
        return self._players_turn

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Moves a particular player's piece to a new location on the board following the rules of checkers, and removes
        it from its previous spot on the board"""
        try:
            starting_list = list(
                starting_square_location)  # turns starting tuple coordinates into a list to iterate through easier
            for x in starting_list:
                if x < 0 or x > 7:
                    raise InvalidSquare  # raises error if player tries to move a piece from out of bounds
        except InvalidSquare:
            print("InvalidSquare Error: You attempted to move from a square on the board that doesn't exist")

        starting_list = list(starting_square_location)
        starting_square = self._board[starting_list[0]][starting_list[1]]
        # assigns variable to the starting location on the board

        try:
            destination_list = list(destination_square_location)
            for y in destination_list:
                if y < 0 or y > 7:
                    raise InvalidSquare
                    # raises error if player tries to move to a square out of bounds
        except InvalidSquare:
            print("InvalidSquare Error: You attempted to move to a square on the board that doesn't exist")

        destination_list = list(destination_square_location)
        destination_square = self._board[destination_list[0]][destination_list[1]]
        # assigns a variable to the destination square

        try:
            if player_name in self._players_list:
                pass
            else:
                raise InvalidPlayer  # raises error if player attempts to move with a player name that is
                # unassigned to one of the two different colored pieces
        except InvalidPlayer:
            print("InvalidPlayer Error: " + player_name + " is not a valid player in this game")

        try:
            for player in self._player_objects:
                if player.get_player_name() == player_name and self._players_turn == player_name:
                    current_player = player  # assigns a variable to the player who is currently attempting to move
                    current_color = player.get_player_piece_color()
                    # assigns variable to the color of the piece that is being moved by the current player
                    if player_name in self._players_list:
                        if player_name != self._players_turn:
                            # raises error if the current player is trying to play out of turn
                            raise OutofTurn
                        if starting_square == current_color or starting_square == (current_color + "_king") or \
                                starting_square == (current_color + "_Triple_King"):
                            pass         # this means the player is attempting to move from a valid square
                        else:
                            raise InvalidSquare
                        if destination_square is not None:
                            raise InvalidSquare
                        if destination_square is None:
                            if starting_square == "White" and destination_list[0] == 7 or \
                                    starting_square == "Black" and destination_list[0] == 0:
                                self._board[destination_list[0]][destination_list[1]] = current_color + "_king"
                                print(self._board[destination_list[0]][destination_list[1]])
                                current_player.increase_king_count(1)   # if piece gets to opp. end of board
                            if starting_square == "White_king" and destination_list[0] == 0 or \
                                    starting_square == "Black_king" and destination_list[0] == 7:
                                self._board[destination_list[0]][
                                    destination_list[1]] = current_color \
                                                           + "_Triple_King"
                                current_player.increase_triple_king_count(1)
                                # if king returns to original side of board
                            else:
                                if starting_square == "White_king" or starting_square == "Black_king":
                                    self._board[destination_list[0]][
                                        destination_list[1]] = current_color + "_king"
                                    # normal king move
                                if starting_square == "White_Triple_King" or starting_square == "Black_Triple_King":
                                    self._board[destination_list[0]][
                                        destination_list[1]] = current_color + "Triple_King"
                                    # normal triple king move
                                else:
                                    if starting_square == "White" and destination_list[0] < 7 or \
                                            starting_square == "Black" and destination_list[0] > 0:
                                        self._board[destination_list[0]][destination_list[1]] = current_color
                                    # normal piece move
                        # the below sequence of code checks to see if there are any captures for the recent move
                        # and adjusts the capture count if so
                        row_diff = destination_list[0] - starting_list[0]
                        col_diff = destination_list[1] - starting_list[1]
                        if row_diff < 0:
                            row_step = - 1
                        else:
                            row_step = 1
                        if col_diff < 0:
                            col_step = -1
                        else:
                            col_step = 1
                        current_row = starting_list[0]
                        current_col = starting_list[1]
                        while current_row != destination_list[0] and current_col != \
                                destination_list[1]:
                            if (current_color == "Black" and
                                self._board[current_row][current_col] == "White") or \
                                    (current_color == "White" and
                                     self._board[current_row][current_col] == "Black"):
                                current_player.increase_captured_piece_count(1)
                            if (current_color == "Black" and self._board[current_row][
                                current_col] == "White_king") or \
                                    (current_color == "White" and
                                     self._board[current_row][
                                         current_col] == "Black_king"):
                                current_player.increase_captured_piece_count(1)
                            if starting_square != self._board[current_row][current_col] and \
                                    (current_color == "Black" and self._board[current_row][
                                        current_col] == "White_Triple_King") or (
                                    current_color == "White" and self._board[current_row][
                                    current_col] == "Black_Triple_King"):
                                current_player.increase_captured_piece_count(1)
                            self._board[current_row][current_col] = None
                            current_row += row_step
                            current_col += col_step
                    self._board[starting_list[0]][starting_list[1]] = None
                    if current_color == "Black":
                        for x in self._player_objects:
                            if x.get_player_piece_color() == "White":
                                self._players_turn = x.get_player_name()
                    if current_color == "White":
                        for x in self._player_objects:
                            if x.get_player_piece_color() == "Black":
                                self._players_turn = x.get_player_name()
                    return current_player.get_captured_pieces_count()
                    # returns the captured piece count for the player
                    # who just played
        except OutofTurn:
            print("OutofTurn Error: It is not your turn")
        except InvalidSquare:
            print("InvalidSquare Error: You attempted to move to or from an invalid square")

    def get_checker_details(self, square_location):
        """takes as a parameter a square_location on the board and returns the checker details present in the
        square_location"""
        try:
            square_location_list = list(
                square_location)  # turns starting tuple coordinates into a list to iterate through easier
            for x in square_location_list:
                if x < 0 or x > 7:
                    raise InvalidSquare  # raises error if player tries to move a piece from out of bounds
        except InvalidSquare:
            print("InvalidSquare Error: This is not a location on the board")

        square_location_list = list(square_location)
        square_details = self._board[square_location_list[0]][square_location_list[1]]
        return square_details

    def get_board(self):
        """returns the current board in the form of an array"""
        return self._board

    def print_board(self):
        """prints the current board in the form of an array"""
        print(self._board)

    def game_winner(self):
        """returns the name of the player who won the game or "Game has not ended" if the game is not over yet"""
        for player in self._player_objects:
            if player.get_captured_pieces_count() == 12:
                return player.get_player_name()
            else:
                return "Game has not ended"


class Player:
    """Player object represents a player in the game, which is added in the Checkers class in the create_player
    method using composition"""

    def __init__(self, player_name, piece_color):
        """Initializes the components of a player object; their name and piece color."""
        self._player_name = player_name
        self._piece_color = piece_color
        self._captured_pieces_count = 0
        self._king_count = 0
        self._triple_king_count = 0

    def increase_captured_piece_count(self, amount):
        """takes amount of pieces as a parameter and increases a player's captured piece count by that much"""
        self._captured_pieces_count += amount

    def increase_king_count(self, amount):
        """takes amount of kings as a parameter and increases a player's king count by that much"""
        self._king_count += amount

    def increase_triple_king_count(self, amount):
        """takes amount of triple kings as a parameter and increases a player's triple king count by that much"""
        self._triple_king_count += amount

    def get_player_name(self):
        """returns the name of a player"""
        return self._player_name

    def get_player_piece_color(self):
        """returns the color of pieces that a player is using"""
        return self._piece_color

    def get_king_count(self):
        """returns the number of king pieces that a player has"""
        return self._king_count

    def get_triple_king_count(self):
        """returns the number of triple king pieces that a player has"""
        return self._triple_king_count

    def get_captured_pieces_count(self):
        return self._captured_pieces_count

