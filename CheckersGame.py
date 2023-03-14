# Author: Carolynn Wicker
# GitHub username: wickerc
# Date: 03/06/2023
# Description: A class called Checkers that allows two people to play the game of Checkers. This is a variation of the
# original Checkers game with modified rules


class OutofTurn(Exception):
    """user-defined exception for if a player tries to move when it is not their turn"""
    pass


class InvalidSquare(Exception):
    """user-defined exception for if a player tries to move a piece that doesn't belong to them or to or from a square
    on the board that does not exist"""
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
        self._players_list = []

    def create_player(self, player_name, piece_color):
        """Uses composition to create a Player object that represents one of the two players in the game, using their
        name and the color piece they are playing with."""
        new_player = Player(player_name, piece_color)
        self._players_list.append(new_player.get_player_name())  # adds the 2 players to a list of valid players
        return new_player

    def get_players_turn(self):
        """Returns the name of the player who is to play the next turn"""
        return self._players_turn

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Moves a particular player's piece to a new location on the board following the rules of checkers, and removes 
        it from its previous spot on the board"""
        try:
            starting_list = list(starting_square_location)
            for x in starting_list:
                if x < 0 or x > 7:
                    raise InvalidSquare
        except InvalidSquare:
            print("InvalidSquare Error: You attempted to move from a square on the board that doesn't exist")

        starting_square = self._board[starting_list[0]][starting_list[1]]

        try:
            destination_list = list(destination_square_location)
            for y in destination_list:
                if y < 0 or y > 7:
                    raise InvalidSquare
        except InvalidSquare:
            print("InvalidSquare Error: You attempted to move to a square on the board that doesn't exist")

        destination_square = self._board[destination_list[0]][destination_list[1]]

        try:
            if player_name in self._players_list:
                pass
            else:
                raise InvalidPlayer
        except InvalidPlayer:
            print("InvalidPlayer Error: " + player_name + " is not a valid player in this game")

        try:
            if Player1.get_player_name() == player_name:
                if self._players_turn == Player2.get_player_name():
                    raise OutofTurn
                if Player2.get_player_piece_color() == starting_square or \
                        (Player2.get_player_piece_color() + "_king") == starting_square or \
                        (Player2.get_player_piece_color() + "Triple_King") == starting_square or \
                        destination_square is not None:
                    raise InvalidSquare
                if destination_square is None:
                    if Player1.get_player_piece_color() == "White" and destination_list[0] == 7 or \
                            Player1.get_player_piece_color() == "Black" and destination_list[0] == 0:
                        self._board[destination_list[0]][
                            destination_list[1]] = Player1.get_player_piece_color() + "_king"
                    else:
                        if starting_square == "White_king" and destination_list[0] == 0 or \
                                starting_square == "Black_king" and destination_list[0] == 7:
                            self._board[destination_list[0]][destination_list[1]] = Player1.get_player_piece_color()\
                                                                                    + "_Triple_King"
                        else:
                            if starting_square == "White_king" and destination_square is None or \
                                    starting_square == "Black_king" and destination_square is None:
                                self._board[destination_list[0]][destination_list[1]] = Player1.get_player_piece_color() + "_king"
                            else:
                                if starting_square == "White_Triple_King" and destination_square is None or \
                                        starting_square == "Black_Triple_King" and destination_square is None:
                                    self._board[destination_list[0]][
                                        destination_list[1]] = Player1.get_player_piece_color() + "Triple_King"
                                else:
                                    if (starting_list[0] + destination_list[0]) % 2 == 0 and \
                                            (starting_list[1] + destination_list[1]) % 2 == 0:
                                        jumped_0 = int((starting_list[0] + destination_list[0]) / 2)
                                        jumped_1 = int((starting_list[1] + destination_list[1]) / 2)
                                        if self._board[jumped_0][jumped_1] == Player2.get_player_piece_color():
                                            Player1._captured_pieces_count += 1
                                            self._board[jumped_0][jumped_1] = None
                                        if self._board[jumped_0][jumped_1] == Player2.get_player_piece_color() + "_king":
                                            Player1._captured_pieces_count += 2
                                            self._board[jumped_0][jumped_1] = None
                                        if self._board[jumped_0][jumped_1] == Player2.get_player_piece_color() + "Triple_King":
                                            Player1._captured_pieces_count += 3
                                            self._board[jumped_0][jumped_1] = None
                                    self._board[destination_list[0]][destination_list[1]] = Player1.get_player_piece_color()
                    self._board[starting_list[0]][starting_list[1]] = None
                    self._players_turn = Player.get_player_name(Player2)
                    return Player1.get_captured_pieces_count()
        except OutofTurn:
            print("OutofTurn Error: " + "It is " + Player2.get_player_name() + "'s" + " turn")
        except InvalidSquare:
            print("InvalidSquare Error: You attempted to move to or from an invalid square")

        else:
            try:
                if Player2.get_player_name() == player_name:
                    if self._players_turn == Player1.get_player_name():
                        raise OutofTurn
                    if Player1.get_player_piece_color() == starting_square or \
                            (Player1.get_player_piece_color() + "_king") == starting_square or \
                            (Player1.get_player_piece_color() + "Triple_King") == starting_square or \
                            destination_square is not None:
                        raise InvalidSquare
                    if destination_square is None:
                        if Player2.get_player_piece_color() == "White" and destination_list[0] == 7 or \
                                Player2.get_player_piece_color() == "Black" and destination_list[0] == 0:
                            self._board[destination_list[0]][
                                destination_list[1]] = Player2.get_player_piece_color() + "_king"
                        else:
                            if starting_square == "White_king" and destination_list[0] == 0 or \
                                    starting_square == "Black_king" and destination_list[0] == 7:
                                self._board[destination_list[0]][destination_list[1]] = Player2.get_player_piece_color() \
                                                                                        + "_Triple_King"
                            else:
                                if starting_square == "White_king" and destination_square is None or \
                                        starting_square == "Black_king" and destination_square is None:
                                    self._board[destination_list[0]][
                                        destination_list[1]] = Player2.get_player_piece_color() + "_king"
                                else:
                                    if starting_square == "White_Triple_King" and destination_square is None or \
                                            starting_square == "Black_Triple_King" and destination_square is None:
                                        self._board[destination_list[0]][
                                            destination_list[1]] = Player2.get_player_piece_color() + "Triple_King"
                                    else:
                                        if (starting_list[0] + destination_list[0]) % 2 == 0 and \
                                                (starting_list[1] + destination_list[1]) % 2 == 0:
                                            jumped_0 = int((starting_list[0] + destination_list[0]) / 2)
                                            jumped_1 = int((starting_list[1] + destination_list[1]) / 2)
                                            if self._board[jumped_0][jumped_1] == Player1.get_player_piece_color():
                                                Player2._captured_pieces_count += 1
                                                self._board[jumped_0][jumped_1] = None
                                            if self._board[jumped_0][jumped_1] == Player1.get_player_piece_color() + "_king":
                                                Player2._captured_pieces_count += 2
                                                self._board[jumped_0][jumped_1] = None
                                            if self._board[jumped_0][jumped_1] == Player1.get_player_piece_color() + "Triple_King":
                                                Player2._captured_pieces_count += 3
                                                self._board[jumped_0][jumped_1] = None
                                        self._board[destination_list[0]][destination_list[1]] = Player2.get_player_piece_color()
                        self._board[starting_list[0]][starting_list[1]] = None
                        self._players_turn = Player.get_player_name(Player1)
                        return Player2.get_captured_pieces_count()
            except OutofTurn:
                print("OutofTurn Error: " + "It is " + Player1.get_player_name() + "'s" + " turn")
            except InvalidSquare:
                print("InvalidSquare Error: You attempted to move to or from an invalid square")

    # def get_checker_details(self):

    def print_board(self):
        print(self._board)

    # def game_winner(self):


class Player:
    """Player object represents a player in the game, which is added in the Checkers class in the create_player
    method using composition"""

    def __init__(self, player_name, piece_color):
        """Initializes the components of a player object; their name and piece color."""
        self._player_name = player_name
        self._piece_color = piece_color
        self._captured_pieces_count = 0

    def get_player_name(self):
        """returns the name of a player"""
        return self._player_name

    def get_player_piece_color(self):
        """returns the color of pieces that a player is using"""
        return self._piece_color

    # def get_king_count(self):

    # def get_triple_king_count(self):

    def get_captured_pieces_count(self):
        return self._captured_pieces_count



