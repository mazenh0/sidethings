import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
HIGHLIGHT = (186, 202, 68)
SELECT = (246, 246, 105)

# Piece representations
PIECES = {
    'K': '\u2654', 'Q': '\u2655', 'R': '\u2656', 'B': '\u2657', 'N': '\u2658', 'P': '\u2659',
    'k': '\u265A', 'q': '\u265B', 'r': '\u265C', 'b': '\u265D', 'n': '\u265E', 'p': '\u265F'
}


class Piece:
    def __init__(self, color, piece_type, row, col):
        self.color = color  # 'white' or 'black'
        self.piece_type = piece_type  # 'K', 'Q', 'R', 'B', 'N', 'P'
        self.row = row
        self.col = col
        self.has_moved = False

    def get_symbol(self):
        if self.color == 'white':
            return PIECES[self.piece_type.upper()]
        else:
            return PIECES[self.piece_type.lower()]

    def move(self, row, col):
        self.row = row
        self.col = col
        self.has_moved = True


class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_turn = 'white'
        self.selected_piece = None
        self.valid_moves = []
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.setup_board()

    def setup_board(self):
        # Black pieces
        self.board[0][0] = Piece('black', 'R', 0, 0)
        self.board[0][1] = Piece('black', 'N', 0, 1)
        self.board[0][2] = Piece('black', 'B', 0, 2)
        self.board[0][3] = Piece('black', 'Q', 0, 3)
        self.board[0][4] = Piece('black', 'K', 0, 4)
        self.board[0][5] = Piece('black', 'B', 0, 5)
        self.board[0][6] = Piece('black', 'N', 0, 6)
        self.board[0][7] = Piece('black', 'R', 0, 7)
        for col in range(COLS):
            self.board[1][col] = Piece('black', 'P', 1, col)

        # White pieces
        self.board[7][0] = Piece('white', 'R', 7, 0)
        self.board[7][1] = Piece('white', 'N', 7, 1)
        self.board[7][2] = Piece('white', 'B', 7, 2)
        self.board[7][3] = Piece('white', 'Q', 7, 3)
        self.board[7][4] = Piece('white', 'K', 7, 4)
        self.board[7][5] = Piece('white', 'B', 7, 5)
        self.board[7][6] = Piece('white', 'N', 7, 6)
        self.board[7][7] = Piece('white', 'R', 7, 7)
        for col in range(COLS):
            self.board[6][col] = Piece('white', 'P', 6, col)

    def get_piece(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        if piece:
            # Update king position if moving king
            if piece.piece_type == 'K':
                if piece.color == 'white':
                    self.white_king_pos = (end_row, end_col)
                else:
                    self.black_king_pos = (end_row, end_col)

            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None
            piece.move(end_row, end_col)
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def get_valid_moves(self, row, col):
        piece = self.get_piece(row, col)
        if not piece or piece.color != self.current_turn:
            return []

        moves = []

        if piece.piece_type == 'P':
            moves = self._get_pawn_moves(piece)
        elif piece.piece_type == 'R':
            moves = self._get_rook_moves(piece)
        elif piece.piece_type == 'N':
            moves = self._get_knight_moves(piece)
        elif piece.piece_type == 'B':
            moves = self._get_bishop_moves(piece)
        elif piece.piece_type == 'Q':
            moves = self._get_queen_moves(piece)
        elif piece.piece_type == 'K':
            moves = self._get_king_moves(piece)

        # Filter out moves that would put own king in check
        valid_moves = []
        for move in moves:
            if not self._would_be_in_check(piece, move):
                valid_moves.append(move)

        return valid_moves

    def _get_pawn_moves(self, piece):
        moves = []
        direction = -1 if piece.color == 'white' else 1
        start_row = 6 if piece.color == 'white' else 1

        # Move forward one square
        new_row = piece.row + direction
        if 0 <= new_row < ROWS and self.board[new_row][piece.col] is None:
            moves.append((new_row, piece.col))

            # Move forward two squares from starting position
            if piece.row == start_row:
                new_row2 = piece.row + 2 * direction
                if self.board[new_row2][piece.col] is None:
                    moves.append((new_row2, piece.col))

        # Capture diagonally
        for dcol in [-1, 1]:
            new_row = piece.row + direction
            new_col = piece.col + dcol
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                target = self.board[new_row][new_col]
                if target and target.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    def _get_rook_moves(self, piece):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row = piece.row + dr * i
                new_col = piece.col + dc * i

                if not (0 <= new_row < ROWS and 0 <= new_col < COLS):
                    break

                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def _get_knight_moves(self, piece):
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for dr, dc in knight_moves:
            new_row = piece.row + dr
            new_col = piece.col + dc

            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                target = self.board[new_row][new_col]
                if target is None or target.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    def _get_bishop_moves(self, piece):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row = piece.row + dr * i
                new_col = piece.col + dc * i

                if not (0 <= new_row < ROWS and 0 <= new_col < COLS):
                    break

                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def _get_queen_moves(self, piece):
        return self._get_rook_moves(piece) + self._get_bishop_moves(piece)

    def _get_king_moves(self, piece):
        moves = []
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in king_moves:
            new_row = piece.row + dr
            new_col = piece.col + dc

            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                target = self.board[new_row][new_col]
                if target is None or target.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    def _would_be_in_check(self, piece, move):
        # Simulate the move
        end_row, end_col = move
        start_row, start_col = piece.row, piece.col
        original_piece = self.board[end_row][end_col]

        # Make temporary move
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None
        original_pos = (piece.row, piece.col)
        piece.row, piece.col = end_row, end_col

        # Update king position temporarily if moving king
        if piece.piece_type == 'K':
            if piece.color == 'white':
                old_king_pos = self.white_king_pos
                self.white_king_pos = (end_row, end_col)
            else:
                old_king_pos = self.black_king_pos
                self.black_king_pos = (end_row, end_col)

        # Check if king is in check
        in_check = self.is_in_check(piece.color)

        # Undo the move
        self.board[start_row][start_col] = piece
        self.board[end_row][end_col] = original_piece
        piece.row, piece.col = original_pos

        # Restore king position if it was moved
        if piece.piece_type == 'K':
            if piece.color == 'white':
                self.white_king_pos = old_king_pos
            else:
                self.black_king_pos = old_king_pos

        return in_check

    def is_in_check(self, color):
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos

        # Check if any opponent piece can attack the king
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    # Get moves without check validation to avoid infinite recursion
                    if piece.piece_type == 'P':
                        moves = self._get_pawn_attacks(piece)
                    elif piece.piece_type == 'R':
                        moves = self._get_rook_moves(piece)
                    elif piece.piece_type == 'N':
                        moves = self._get_knight_moves(piece)
                    elif piece.piece_type == 'B':
                        moves = self._get_bishop_moves(piece)
                    elif piece.piece_type == 'Q':
                        moves = self._get_queen_moves(piece)
                    elif piece.piece_type == 'K':
                        moves = self._get_king_moves(piece)
                    else:
                        moves = []

                    if king_pos in moves:
                        return True
        return False

    def _get_pawn_attacks(self, piece):
        moves = []
        direction = -1 if piece.color == 'white' else 1

        for dcol in [-1, 1]:
            new_row = piece.row + direction
            new_col = piece.col + dcol
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                moves.append((new_row, new_col))

        return moves

    def is_checkmate(self):
        if not self.is_in_check(self.current_turn):
            return False

        # Check if any piece can make a valid move
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == self.current_turn:
                    if len(self.get_valid_moves(row, col)) > 0:
                        return False
        return True

    def is_stalemate(self):
        if self.is_in_check(self.current_turn):
            return False

        # Check if any piece can make a valid move
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == self.current_turn:
                    if len(self.get_valid_moves(row, col)) > 0:
                        return False
        return True


class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.selected_square = None
        self.font = pygame.font.Font(None, 80)
        self.small_font = pygame.font.Font(None, 36)

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK

                # Highlight selected square
                if self.selected_square == (row, col):
                    color = SELECT
                # Highlight valid moves
                elif (row, col) in self.board.valid_moves:
                    color = HIGHLIGHT

                pygame.draw.rect(self.screen, color,
                               (col * SQUARE_SIZE, row * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece:
                    symbol = piece.get_symbol()
                    text = self.font.render(symbol, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                      row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    self.screen.blit(text, text_rect)

    def draw_status(self):
        status_text = f"{self.board.current_turn.capitalize()}'s Turn"

        if self.board.is_checkmate():
            winner = 'Black' if self.board.current_turn == 'white' else 'White'
            status_text = f"Checkmate! {winner} Wins!"
        elif self.board.is_stalemate():
            status_text = "Stalemate! Draw!"
        elif self.board.is_in_check(self.board.current_turn):
            status_text += " (Check!)"

        text = self.small_font.render(status_text, True, (255, 255, 255))
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, WIDTH, 40))
        self.screen.blit(text, (10, 10))

    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if self.board.is_checkmate() or self.board.is_stalemate():
            return

        # If a piece is selected and clicking on valid move
        if self.selected_square and (row, col) in self.board.valid_moves:
            start_row, start_col = self.selected_square
            self.board.move_piece(start_row, start_col, row, col)
            self.selected_square = None
            self.board.valid_moves = []
        else:
            # Select a piece
            piece = self.board.get_piece(row, col)
            if piece and piece.color == self.board.current_turn:
                self.selected_square = (row, col)
                self.board.valid_moves = self.board.get_valid_moves(row, col)
            else:
                self.selected_square = None
                self.board.valid_moves = []

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.draw_board()
            self.draw_pieces()
            self.draw_status()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = ChessGame()
    game.run()
