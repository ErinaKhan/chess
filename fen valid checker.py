def is_valid_fen(fen):
    fields = fen.split()
    if len(fields) != 6:
        return False  # FEN must have exactly 6 parts
    
    piece_placement, active_color, castling, en_passant, halfmove, fullmove = fields
    
    # Check if the board has 8 rows
    ranks = piece_placement.split('/')
    if len(ranks) != 8:
        return False
    
    # Check if each rank adds up to 8 squares
    for rank in ranks:
        count = 0
        for char in rank:
            if char.isdigit():
                count += int(char)
            else:
                count += 1
        if count != 8:
            return False
    
    # Check if active color is 'w' or 'b'
    if active_color not in ('w', 'b'):
        return False
    
    # Check castling rights (must be valid or '-')
    valid_castling = set("KQkq-")
    if any(c not in valid_castling for c in castling):
        return False
    
    # Check en passant target square (must be valid or '-')
    valid_en_passant = [f"{c}{n}" for c in "abcdefgh" for n in "36"] + ["-"]
    if en_passant not in valid_en_passant:
        return False
    
    # Check if halfmove and fullmove are numbers
    if not (halfmove.isdigit() and fullmove.isdigit()):
        return False
    
    return True

# Example Usage:
fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
print(is_valid_fen(fen_string))  # Expected output: True