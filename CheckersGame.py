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
        self._players_list = []      # list of player names
        self._player_objects = []      # list of player objects

    def create_player(self, player_name, piece_color):
        """Uses composition to create a Player object that represents one of the two players in the game, using their
        name and the color piece they are playing with."""
        new_player = Player(player_name, piece_color)
        self._player_objects.append(new_player)  # adds the 2 players to a list of valid players
        self._players_list.append(player_name)
        if piece_color == "Black":          # initializes black pieces as first player in the game
            self._players_turn = player_name
        return new_player

    def get_players_turn(self):
        """Returns the name of the player who is to play the next turn"""
        return self._players_turn

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Moves a particular player's piece to a new location on the board following the rules of checkers, and removes
        it from its previous spot on the board"""
        try:
            starting_list = list(starting_square_location)    # turns starting tuple coordinates into a list to iterate through easier
            for x in starting_list:
                if x < 0 or x > 7:
                    raise InvalidSquare           # raises error if player tries to move a piece from out of bounds
        except InvalidSquare:
            print("InvalidSquare Error: You attempted to move from a square on the board that doesn't exist")

        starting_square = self._board[starting_list[0]][starting_list[1]]    # assigns variable to the starting location on the board

        try:
            destination_list = list(destination_square_location)
            for y in destination_list:
                if y < 0 or y > 7:
                    raise InvalidSquare              # raises error if player tries to move to a square out of bounds
        except InvalidSquare:
            print("InvalidSquare Error: You attempted to move to a square on the board that doesn't exist")

        destination_square = self._board[destination_list[0]][destination_list[1]]   # assigns a variable to the destination square

        try:
            if player_name in self._players_list:
                pass
            else:
                raise InvalidPlayer      # raises error if player attempts to move with a player name that is unassigned to one of the two different colored pieces
        except InvalidPlayer:
            print("InvalidPlayer Error: " + player_name + " is not a valid player in this game")

        try:
            for player in self._player_objects:
                if player.get_player_name() == player_name and self._players_turn == player_name:
                    current_player = player  # assigns a variable to the player who is currently attempting to move
                    current_color = player.get_player_piece_color()  # assigns variable to the color of the piece that is being moved by the current player
                    if player_name in self._players_list:
                        if player_name != self._players_turn:      # raises error if the current player is trying to play out of turn
                            raise OutofTurn
                        if starting_square == current_color or starting_square == (current_color + "_king") or \
                                starting_square == (current_color + "_Triple_King"):
                            pass
                        else:
                            raise InvalidSquare
                        if destination_square is not None:
                            raise InvalidSquare
                        if destination_square is None:          # assigns current player's piece to king status if they move to the opposite end of the board
                            if current_color == "White" and destination_list[0] == 7 or \
                                    current_color == "Black" and destination_list[0] == 0:
                                self._board[destination_list[0]][
                                    destination_list[1]] = current_color + "_king"
                            else:                 # assigns current player's piece to tripe king status if they move their king back to their original end of the board
                                if starting_square == "White_king" and destination_list[0] == 0 or \
                                        starting_square == "Black_king" and destination_list[0] == 7:
                                    self._board[destination_list[0]][
                                        destination_list[1]] = current_color \
                                                               + "_Triple_King"
                                else:                # simply moves the current player's king piece without needing to change it's status
                                    if starting_square == "White_king" and destination_square is None or \
                                            starting_square == "Black_king" and destination_square is None:
                                        self._board[destination_list[0]][
                                            destination_list[1]] = current_color + "_king"
                                        row_diff = destination_list[0] - starting_list[0]
                                        col_diff = destination_list[1] - starting_list [1]
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
                                        while current_row != destination_list[0] and current_col != destination_list[1]:
                                            if self._board[current_row][current_col] == "Black" or self._board[current_row][current_col] == "White":
                                                print(self._board[current_row][current_col])
                                                current_player.increase_captured_piece_count(1)
                                            if starting_square != self._board[current_row][current_col] and (self._board[current_row][current_col] == "Black_king" or self._board[current_row][current_col] == "White_king"):
                                                print(self._board[current_row][current_col])
                                                current_player.increase_captured_piece_count(2)
                                            if self._board[current_row][current_col] == "Black_Triple_King" or self._board[current_row][current_col] == "White_Triple_King":
                                                print(self._board[current_row][current_col])
                                                current_player.increase_captured_piece_count(3)
                                            self._board[current_row][current_col] = None
                                            current_row += row_step
                                            current_col += col_step
                                    else:     # simply moves the current player's triple king piece without needing to change it's status
                                        if starting_square == "White_Triple_King" and destination_square is None or \
                                                starting_square == "Black_Triple_King" and destination_square is None:
                                            self._board[destination_list[0]][
                                                destination_list[1]] = current_color + "Triple_King"
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
                                                if (current_color == "Black" and self._board[current_row][current_col] == "White" ) or ( \
                                                        current_color == "White" and self._board[current_row][current_col] == "Black"):
                                                    print(self._board[current_row][current_col])
                                                    current_player.increase_captured_piece_count(1)
                                                if (current_color == "Black" and self._board[current_row][
                                                    current_col] == "White_king") or (current_color == "White" and self._board[current_row][
                                                            current_col] == "Black_king"):
                                                    print(self._board[current_row][current_col])
                                                    current_player.increase_captured_piece_count(2)
                                                if starting_square != self._board[current_row][current_col] and \
                                                        (current_color == "Black" and self._board[current_row][
                                                    current_col] == "White_Triple_King") or (
                                                        current_color == "White" and self._board[current_row][
                                                    current_col] == "Black_Triple_King"):
                                                    print(self._board[current_row][current_col])
                                                    current_player.increase_captured_piece_count(3)
                                                self._board[current_row][current_col] = None
                                                current_row += row_step
                                                current_col += col_step
                                        else:         # assumes piece is not a king or triple king and checks to see if it has jumped an opponent's piece in a regular diagonal jump
                                            if starting_square == "Black" or starting_square == "White":
                                                if (starting_list[0] + destination_list[0]) % 2 == 0 and \
                                                        (starting_list[1] + destination_list[1]) % 2 == 0:
                                                    jumped_0 = int((starting_list[0] + destination_list[0]) / 2)
                                                    jumped_1 = int((starting_list[1] + destination_list[1]) / 2)
                                                    if self._board[jumped_0][jumped_1] != current_color and not None:    # checks if jumped piece is the opponent's
                                                        current_player.increase_captured_piece_count(1)  # increases current's captures piece count by 1
                                                        if "king" or "King" in self._board[jumped_0][jumped_1]:   # checks if jumped piece is at least a king
                                                            current_player.increase_captured_piece_count(1)   # increases current captures by 1 if above condition met
                                                            if "Triple" in self._board[jumped_0][jumped_1]:    # checks if jumped piece is a triple king
                                                                current_player.increase_captured_piece_count(1)  # increases current captures by 3 for a total of 3 captures in one move if above condition is met
                                                    self._board[jumped_0][jumped_1] = None  # sets jumped location to None
                                            self._board[destination_list[0]][
                                                destination_list[1]] = current_color   # moves current piece to destination spot on board
                    self._board[starting_list[0]][starting_list[1]] = None   # changes current's previous location to None
                    if current_color == "Black":
                        for x in self._player_objects:
                            if x.get_player_piece_color() == "White":
                                self._players_turn = x.get_player_name()
                    if current_color == "White":
                        for x in self._player_objects:
                            if x.get_player_piece_color() == "Black":
                                self._players_turn = x.get_player_name()
                    return current_player.get_captured_pieces_count()     # returns the total number of pieces captured by current player
        except OutofTurn:
            print("OutofTurn Error: It is not your turn")
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

    def increase_captured_piece_count(self, amount):
        """takes amount of pieces as a parameter and increases a player's captured piece count by that much"""
        self._captured_pieces_count += amount

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


game = Checkers()

Player1 = game.create_player("Lucy", "Black")
Player2 = game.create_player("Jack", "White")

print(game.play_game("Lucy", (7, 6), (4, 0)))
print(game.play_game("Jack", (0, 1), (7, 6)))
print(game.play_game("Lucy", (5, 0), (4, 1)))
print(game.play_game("Jack", (7, 6), (4, 3)))
game.print_board()
