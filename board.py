class Board:
    def __init__(self):
        # 8x8 board, index [0][0] is a1, [7][7] is h8
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]

        # Game state
        self.to_move = WHITE
        self.castling_rights = {
            'K':True, # White kingside
            'Q':True, # White queenside
            'k':True, # Black kingside
            'q':True  # Black queenside
        }
        self.en_passant_square = None
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.setup_initial_position()

    def setup_initial_position(self):
        """Set up the standard starting position."""
        # Black pieces (rank 8 and 7)
        back_rank = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]
        for i in range(8):
            self.board[7][i] = WHITE | back_rank[i]
            self.board[6][i] = BLACK | PAWN

        # White pieces (rank 2 and 1)
        for i in range(8):
            self.board[1][i] = WHITE | PAWN
            self.board[0][i] = WHITE | back_rank[i]

    def piece_at(self, row, col):
        """"Get the piece at a given square. """
        return self.board[row][col]

    def is_sqare_attacked(self, row, col, by_color):
        """Check if a square is attacked by a given color."""
        # We'll implement this after move generation
        pass

    def generate_pawn_moves(self, row, col, moves):
        """Generate all pawn moves from a given square."""
        piece = self.board[row][col]
        color = piece & 24

        if color == WHITE:
            direction = 1
            start_row = 1
            promotion_row = 7
        else:
            direction = -1
            start_row = 6
            promotion_row = 0

        # Single push
        if self.board[row + direction][col] == EMPTY:
            if row + direction == promotion_row:
                for promo_piece in [QUEEN, ROOK, BISHOP, KNIGHT]:
                    moves.append(Move(row, col, row + direction, col, promotion=promo_piece))

            else:
                moves.append(Move(row, col, row+direction, col))

            # Double move from starting position
            if row == start_row and self.board[row + 2 * direction][col] == EMPTY:
                moves.append(Move(row, col, row+2*direction, col))

        # Captures
        for dcol in [-1,1]:
            new_col = col+dcol
            if 0 <= new_col < 8:
                new_row = row + direction
                target = self.board[new_row][new_col]

                # Regular capture
                if target != EMPTY and (target & 24) != color:
                    if new_row == promotion_row:
                        for promo_piece in [QUEEN, ROOK, BISHOP, KNIGHT]:
                            moves.append(Move(row, col, new_row, new_col, promotion= promo_piece))

                    else:
                        moves.append(Move(row, col, new_row, new_col))

                # En passant
                if self.en_passant_square == (new_row, new_col):
                    moves.append(Move(row, col, new_row, new_col, is_en_passant=True))

    def generate_knight_moves(self, row, col, moves):
        """Generate all knight moves from a given square."""
        piece = self.board[row][col]
        color = piece & 24

        knight_offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for drow, dcol, in knight_offsets:
            new_row, new_col = row+drow, col+dcol

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target == EMPTY or (target & 24) != color:
                    moves.append(Move(row,col,new_row, new_col))

    def generate_sliding_moves(self, row, col, moves, directions):
        """Generate moves for sliding pieces (bishop, rook, queen)."""
        piece = self.board[row][col]
        color = piece & 24

        for drow, dcol in directions:
            new_row, new_col = row+drow, col+dcol

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]

                if target == EMPTY:
                    moves.append(Move(row, col, new_row, new_col))
                elif (target & 24) != color:
                    moves.append(Move(row,col, new_row, new_col))
                    break # Can't move past a capture
                else:
                    break # Blocked by own piece

                new_row += drow
                new_col += dcol

    def generate_bishop_moves(self, row, col, moves):
        """Generate all bishop moves."""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.generate_bishop_moves(row, col, moves, directions)

    def generate_rook_moves(self, row, col, moves):
        """Generate all rook moves."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.generate_sliding_moves(row, col, moves, directions)

    def generate_queen_moves(self, row, col, moves):
        """Generate all queen moves"""
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        self.generate_sliding_moves(row, col, moves, directions)

    def generate_king_moves(self, row, col, moves):
        """Generate all king moves including castling."""
        piece = self.baord[row][col]
        color = piece & 24

        # Regular king moves
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if drow == 0 and dcol == 0:
                    continue

                new_row, new_col = row + drow, col+dcol

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target == EMPTY or (target & 24) != color:
                        moves.append(Move(row, col, new_row, new_col))

        # Castling
        if color == WHITE and row == 0:
            # Kingside
            if (self.castling_rights['K'] and
                self.board[0][5] == EMPTY and
                self.board[0][6] == EMPTY):
                moves.append(Move(0, 4,0, 6, is_castling=True))

            # Queenside
            if (self.castling_rights['Q'] and
                self.board[0][1] == EMPTY and
                self.board[0][2] == EMPTY and
                self.board[0][3] == EMPTY):
                moves.append(Move(7,4,7,6, is_castling=True))

        elif color == BLACK and row == 7:
            # Kingside
            if (self.castling_rights['k'] and
                self.board[7][5] == EMPTY and
                self.board[7][6] == EMPTY):
                moves.append(Move(7,4,7,2, is_castling=True))

            # Queenside
            if (self.castling_rights['q'] and
                self.board[7][1] == EMPTY and
                self.board[7][2] == EMPTY and
                self.board[7][3] == EMPTY):
                moves.append(Move(7,4,7,2, is_castling=True))

    def generate_pseudo_legal_moves(self):
        """Generate all pseudo-legal moves for the current position."""
        moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece == EMPTY or (piece & 24) != self.to_move:
                    continue

                piece_type = piece & 7

                if piece_type == PAWN:
                    self.generate_pawn_moves(row, col, moves)
                elif piece_type == KNIGHT:
                    self.generate_knight_moves(row,col, moves)
                elif piece_type == BISHOP:
                    self.generate_bishop_moves(row, col, moves)
                elif piece_type == ROOK:
                    self.generate_rook_moves(row, col, moves)
                elif piece_type == QUEEN:
                    self.generate_queen_moves(row, col, moves)
                elif piece_type == KING:
                    self.generate_king_moves(row, col, moves)

        return moves