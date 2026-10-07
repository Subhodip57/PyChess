# Piece Types

EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

# Colors
WHITE = 8
BLACK = 16

# Example: White pawn = WHITE | PAWN = 9
# Example: Black king = BLACK | KING = 22

# piece = WHITE | QUEEN # 13
# piece_type = piece & 7 # Gets QUEEN
# color = piece & 24      # Gets WHITE (8)