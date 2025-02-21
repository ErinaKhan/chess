# Function to generate a FEN string for a given chess position
# This is written in a beginner-friendly way with less efficient practices
def generate_fen(board, turn, castling, en_passant, halfmove, fullmove):
    """
    Generates a FEN string given the board position and game state.
    
    :param board: List of strings representing ranks from 8 to 1.
    :param turn: 'w' or 'b' indicating which side is to move.
    :param castling: String indicating castling rights (e.g., 'KQkq' or '-').
    :param en_passant: En passant target square (e.g., 'e3') or '-'.
    :param halfmove: Halfmove clock for the fifty-move rule.
    :param fullmove: Fullmove number.
    :return: FEN string.
    """
    
    # Function to compress a rank into FEN format
    def compress_rank(rank):
        compressed = ""
        empty_count = 0  # Counter for empty squares
        for i in range(len(rank)):
            if rank[i] == ' ':  # Check if empty square
                empty_count += 1  # Increment empty counter
            else:
                if empty_count > 0:  # If there were empty squares, add the count
                    compressed += str(empty_count)
                    empty_count = 0  # Reset empty counter
                compressed += rank[i]  # Add the piece
        
        # If there are empty squares left at the end, add them
        if empty_count > 0:
            compressed += str(empty_count)
        
        return compressed  # Return compressed rank
    
    # Compress the board into FEN notation
    board_fen = ""
    for i in range(len(board)):
        board_fen += compress_rank(board[i])
        if i != len(board) - 1:
            board_fen += "/"  # Add '/' separator between ranks
    
    # Build the full FEN string with all components
    fen_string = board_fen + " " + turn + " " + castling + " " + en_passant + " " + str(halfmove) + " " + str(fullmove)
    
    return fen_string  # Return the FEN string

# Example usage:
# Define the default board position as a list of strings
# Each string represents a rank (row) on the board
default_board = [
    "rnbqkbnr",  # Rank 8
    "pppppppp",  # Rank 7
    "        ",  # Rank 6
    "        ",  # Rank 5
    "        ",  # Rank 4
    "        ",  # Rank 3
    "PPPPPPPP",  # Rank 2
    "RNBQKBNR"   # Rank 1
]

# Generate the FEN string for the initial position
fen = generate_fen(default_board, 'w', 'KQkq', '-', 0, 1)

# Print the generated FEN string
print(fen)
