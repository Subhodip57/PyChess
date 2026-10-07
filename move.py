class Move:
    def __init__(self, from_row, from_col, to_row, to_col, promotion = None, is_castling = False, is_en_passant = False):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.promotion = promotion #QUEEN BISHOP ROOK KNIGHT
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant

    def __str__(self):
        """Convert move to algebric notation"""
        files = 'abcdefgh'
        from_square = f"{files[self.from_col]}{self.from_row + 1}"
        to_square = f"{files[self.to_col]}{self.to_row + 1}"

        if self.promotion:
            piece_symbols = {QUEEN: 'q', ROOK: 'r', BISHOP: 'b', KNIGHT: 'n'}
            return f"{from_square}{to_square}{piece_symbols[self.promotion]}"

        return f"{from_square}{to_square}"

    def __repr__(self):
        return self.__str__()