import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
BOARD_WIDTH = 800
LEGEND_WIDTH = 250
WIDTH, HEIGHT = BOARD_WIDTH + LEGEND_WIDTH, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS

# Colors
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
HIGHLIGHT = (186, 202, 68)
SELECT = (246, 246, 105)

# Piece representations (for legend)
PIECES = {
    'K': '\u2654', 'Q': '\u2655', 'R': '\u2656', 'B': '\u2657', 'N': '\u2658', 'P': '\u2659',
    'k': '\u265A', 'q': '\u265B', 'r': '\u265C', 'b': '\u265D', 'n': '\u265E', 'p': '\u265F'
}


class PieceRenderer:
    """Custom piece renderer with distinctive designs for each piece"""

    @staticmethod
    def draw_piece(surface, piece_type, color, x, y, size):
        """Draw a chess piece with custom design at the given position"""
        # Colors for pieces
        if color == 'white':
            piece_color = (240, 240, 240)
            outline_color = (60, 60, 60)
        else:
            piece_color = (40, 40, 40)
            outline_color = (200, 200, 200)

        center_x = x + size // 2
        center_y = y + size // 2

        if piece_type == 'P':  # Pawn
            PieceRenderer.draw_pawn(surface, piece_color, outline_color, center_x, center_y, size)
        elif piece_type == 'R':  # Rook
            PieceRenderer.draw_rook(surface, piece_color, outline_color, center_x, center_y, size)
        elif piece_type == 'N':  # Knight
            PieceRenderer.draw_knight(surface, piece_color, outline_color, center_x, center_y, size)
        elif piece_type == 'B':  # Bishop
            PieceRenderer.draw_bishop(surface, piece_color, outline_color, center_x, center_y, size)
        elif piece_type == 'Q':  # Queen
            PieceRenderer.draw_queen(surface, piece_color, outline_color, center_x, center_y, size)
        elif piece_type == 'K':  # King
            PieceRenderer.draw_king(surface, piece_color, outline_color, center_x, center_y, size)

    @staticmethod
    def draw_pawn(surface, color, outline, cx, cy, size):
        """Draw a pawn - simple design with round head"""
        scale = size / 100
        # Base
        pygame.draw.ellipse(surface, color, (cx - 20 * scale, cy + 20 * scale, 40 * scale, 15 * scale))
        pygame.draw.ellipse(surface, outline, (cx - 20 * scale, cy + 20 * scale, 40 * scale, 15 * scale), 2)
        # Body
        pygame.draw.ellipse(surface, color, (cx - 12 * scale, cy - 5 * scale, 24 * scale, 30 * scale))
        pygame.draw.ellipse(surface, outline, (cx - 12 * scale, cy - 5 * scale, 24 * scale, 30 * scale), 2)
        # Head
        pygame.draw.circle(surface, color, (int(cx), int(cy - 15 * scale)), int(10 * scale))
        pygame.draw.circle(surface, outline, (int(cx), int(cy - 15 * scale)), int(10 * scale), 2)

    @staticmethod
    def draw_rook(surface, color, outline, cx, cy, size):
        """Draw a rook - castle tower with crenellations"""
        scale = size / 100
        # Base
        pygame.draw.rect(surface, color, (cx - 22 * scale, cy + 20 * scale, 44 * scale, 12 * scale))
        pygame.draw.rect(surface, outline, (cx - 22 * scale, cy + 20 * scale, 44 * scale, 12 * scale), 2)
        # Body
        pygame.draw.rect(surface, color, (cx - 15 * scale, cy - 15 * scale, 30 * scale, 35 * scale))
        pygame.draw.rect(surface, outline, (cx - 15 * scale, cy - 15 * scale, 30 * scale, 35 * scale), 2)
        # Crenellations (castle top)
        for i in [-12, -4, 4, 12]:
            pygame.draw.rect(surface, color, (cx + i * scale - 3 * scale, cy - 25 * scale, 6 * scale, 10 * scale))
            pygame.draw.rect(surface, outline, (cx + i * scale - 3 * scale, cy - 25 * scale, 6 * scale, 10 * scale), 2)

    @staticmethod
    def draw_knight(surface, color, outline, cx, cy, size):
        """Draw a knight - horse head shape"""
        scale = size / 100
        # Base
        pygame.draw.ellipse(surface, color, (cx - 20 * scale, cy + 18 * scale, 40 * scale, 15 * scale))
        pygame.draw.ellipse(surface, outline, (cx - 20 * scale, cy + 18 * scale, 40 * scale, 15 * scale), 2)
        # Horse head (approximated with polygons)
        points = [
            (cx - 5 * scale, cy + 18 * scale),  # neck bottom
            (cx - 8 * scale, cy - 5 * scale),   # neck top
            (cx - 5 * scale, cy - 20 * scale),  # back of head
            (cx + 10 * scale, cy - 18 * scale), # nose
            (cx + 8 * scale, cy - 8 * scale),   # chin
            (cx + 2 * scale, cy + 5 * scale),   # chest
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, outline, points, 2)
        # Eye
        pygame.draw.circle(surface, outline, (int(cx + 2 * scale), int(cy - 12 * scale)), int(2 * scale))
        # Ear
        pygame.draw.circle(surface, color, (int(cx - 2 * scale), int(cy - 20 * scale)), int(4 * scale))
        pygame.draw.circle(surface, outline, (int(cx - 2 * scale), int(cy - 20 * scale)), int(4 * scale), 2)

    @staticmethod
    def draw_bishop(surface, color, outline, cx, cy, size):
        """Draw a bishop - tall piece with pointed top"""
        scale = size / 100
        # Base
        pygame.draw.ellipse(surface, color, (cx - 20 * scale, cy + 20 * scale, 40 * scale, 12 * scale))
        pygame.draw.ellipse(surface, outline, (cx - 20 * scale, cy + 20 * scale, 40 * scale, 12 * scale), 2)
        # Body (tapered)
        points = [
            (cx - 15 * scale, cy + 20 * scale),
            (cx - 10 * scale, cy - 10 * scale),
            (cx + 10 * scale, cy - 10 * scale),
            (cx + 15 * scale, cy + 20 * scale),
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, outline, points, 2)
        # Neck
        pygame.draw.ellipse(surface, color, (cx - 8 * scale, cy - 18 * scale, 16 * scale, 12 * scale))
        pygame.draw.ellipse(surface, outline, (cx - 8 * scale, cy - 18 * scale, 16 * scale, 12 * scale), 2)
        # Top (pointed)
        pygame.draw.circle(surface, color, (int(cx), int(cy - 22 * scale)), int(6 * scale))
        pygame.draw.circle(surface, outline, (int(cx), int(cy - 22 * scale)), int(6 * scale), 2)
        # Slot on top
        pygame.draw.line(surface, outline, (cx - 6 * scale, cy - 22 * scale), (cx + 6 * scale, cy - 22 * scale), 2)

    @staticmethod
    def draw_queen(surface, color, outline, cx, cy, size):
        """Draw a queen - crown with multiple points"""
        scale = size / 100
        # Base
        pygame.draw.ellipse(surface, color, (cx - 22 * scale, cy + 20 * scale, 44 * scale, 12 * scale))
        pygame.draw.ellipse(surface, outline, (cx - 22 * scale, cy + 20 * scale, 44 * scale, 12 * scale), 2)
        # Body (wider)
        points = [
            (cx - 18 * scale, cy + 20 * scale),
            (cx - 12 * scale, cy - 5 * scale),
            (cx + 12 * scale, cy - 5 * scale),
            (cx + 18 * scale, cy + 20 * scale),
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, outline, points, 2)
        # Crown base
        pygame.draw.rect(surface, color, (cx - 15 * scale, cy - 12 * scale, 30 * scale, 8 * scale))
        pygame.draw.rect(surface, outline, (cx - 15 * scale, cy - 12 * scale, 30 * scale, 8 * scale), 2)
        # Crown points (5 points)
        for i, x_offset in enumerate([-12, -6, 0, 6, 12]):
            height = 15 if i % 2 == 0 else 10
            point_x = cx + x_offset * scale
            pygame.draw.circle(surface, color, (int(point_x), int(cy - 12 * scale - height * scale)), int(3 * scale))
            pygame.draw.circle(surface, outline, (int(point_x), int(cy - 12 * scale - height * scale)), int(3 * scale), 2)

    @staticmethod
    def draw_king(surface, color, outline, cx, cy, size):
        """Draw a king - crown with cross on top"""
        scale = size / 100
        # Base
        pygame.draw.ellipse(surface, color, (cx - 22 * scale, cy + 20 * scale, 44 * scale, 12 * scale))
        pygame.draw.ellipse(surface, outline, (cx - 22 * scale, cy + 20 * scale, 44 * scale, 12 * scale), 2)
        # Body
        points = [
            (cx - 18 * scale, cy + 20 * scale),
            (cx - 12 * scale, cy - 5 * scale),
            (cx + 12 * scale, cy - 5 * scale),
            (cx + 18 * scale, cy + 20 * scale),
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, outline, points, 2)
        # Crown
        pygame.draw.rect(surface, color, (cx - 15 * scale, cy - 12 * scale, 30 * scale, 10 * scale))
        pygame.draw.rect(surface, outline, (cx - 15 * scale, cy - 12 * scale, 30 * scale, 10 * scale), 2)
        # Crown points (4 points)
        for x_offset in [-10, -3, 3, 10]:
            pygame.draw.circle(surface, color, (int(cx + x_offset * scale), int(cy - 12 * scale)), int(3 * scale))
            pygame.draw.circle(surface, outline, (int(cx + x_offset * scale), int(cy - 12 * scale)), int(3 * scale), 2)
        # Cross on top
        cross_y = cy - 22 * scale
        # Vertical line
        pygame.draw.line(surface, outline, (cx, cross_y - 8 * scale), (cx, cross_y + 8 * scale), int(3 * scale))
        # Horizontal line
        pygame.draw.line(surface, outline, (cx - 5 * scale, cross_y), (cx + 5 * scale, cross_y), int(3 * scale))


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
        self.pending_promotion = None  # (row, col) of pawn to promote
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

            # Check for pawn promotion
            if piece.piece_type == 'P':
                if (piece.color == 'white' and end_row == 0) or (piece.color == 'black' and end_row == 7):
                    self.pending_promotion = (end_row, end_col)
                    return  # Don't switch turns yet

            self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def promote_pawn(self, row, col, new_piece_type):
        """Promote a pawn to a new piece type (Q, R, B, or N)"""
        piece = self.board[row][col]
        if piece and piece.piece_type == 'P':
            piece.piece_type = new_piece_type
            self.pending_promotion = None
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
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE
                    PieceRenderer.draw_piece(self.screen, piece.piece_type, piece.color, x, y, SQUARE_SIZE)

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

    def draw_legend(self):
        # Draw legend background
        legend_x = BOARD_WIDTH
        pygame.draw.rect(self.screen, (40, 40, 40), (legend_x, 0, LEGEND_WIDTH, HEIGHT))

        # Title
        title = self.small_font.render("Piece Guide", True, (255, 255, 255))
        self.screen.blit(title, (legend_x + 20, 60))

        # White pieces
        white_title = self.small_font.render("White Pieces:", True, (255, 255, 255))
        self.screen.blit(white_title, (legend_x + 20, 120))

        white_pieces = [
            ('K', 'King'),
            ('Q', 'Queen'),
            ('R', 'Rook'),
            ('B', 'Bishop'),
            ('N', 'Knight'),
            ('P', 'Pawn')
        ]

        y_offset = 160
        for code, name in white_pieces:
            symbol = PIECES[code.upper()]
            symbol_text = self.font.render(symbol, True, (255, 255, 255))
            name_text = self.small_font.render(name, True, (255, 255, 255))
            self.screen.blit(symbol_text, (legend_x + 20, y_offset))
            self.screen.blit(name_text, (legend_x + 80, y_offset + 15))
            y_offset += 50

        # Black pieces
        black_title = self.small_font.render("Black Pieces:", True, (255, 255, 255))
        self.screen.blit(black_title, (legend_x + 20, y_offset + 20))

        y_offset += 60
        for code, name in white_pieces:
            symbol = PIECES[code.lower()]
            symbol_text = self.font.render(symbol, True, (255, 255, 255))
            name_text = self.small_font.render(name, True, (255, 255, 255))
            self.screen.blit(symbol_text, (legend_x + 20, y_offset))
            self.screen.blit(name_text, (legend_x + 80, y_offset + 15))
            y_offset += 50

    def draw_promotion_dialog(self):
        """Draw the pawn promotion selection dialog"""
        if not self.board.pending_promotion:
            return

        # Semi-transparent overlay
        overlay = pygame.Surface((BOARD_WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Dialog box
        dialog_width = 600
        dialog_height = 200
        dialog_x = (BOARD_WIDTH - dialog_width) // 2
        dialog_y = (HEIGHT - dialog_height) // 2

        pygame.draw.rect(self.screen, (60, 60, 60), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, (200, 200, 200), (dialog_x, dialog_y, dialog_width, dialog_height), 3)

        # Title
        title_text = self.small_font.render("Choose promotion piece:", True, (255, 255, 255))
        self.screen.blit(title_text, (dialog_x + 20, dialog_y + 20))

        # Promotion options
        row, col = self.board.pending_promotion
        piece = self.board.get_piece(row, col)
        promotion_pieces = [('Q', 'Queen'), ('R', 'Rook'), ('B', 'Bishop'), ('N', 'Knight')]

        button_width = 120
        button_height = 100
        button_spacing = 20
        start_x = dialog_x + 30

        for i, (piece_type, name) in enumerate(promotion_pieces):
            button_x = start_x + i * (button_width + button_spacing)
            button_y = dialog_y + 70

            # Button background
            pygame.draw.rect(self.screen, (100, 100, 100), (button_x, button_y, button_width, button_height))
            pygame.draw.rect(self.screen, (200, 200, 200), (button_x, button_y, button_width, button_height), 2)

            # Piece symbol
            if piece:
                symbol = PIECES[piece_type.upper() if piece.color == 'white' else piece_type.lower()]
                symbol_text = self.font.render(symbol, True, (255, 255, 255))
                symbol_rect = symbol_text.get_rect(center=(button_x + button_width // 2, button_y + 35))
                self.screen.blit(symbol_text, symbol_rect)

                # Piece name
                name_text = self.small_font.render(name, True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(button_x + button_width // 2, button_y + 80))
                self.screen.blit(name_text, name_rect)

    def handle_promotion_click(self, pos):
        """Handle clicks on the promotion dialog"""
        if not self.board.pending_promotion:
            return False

        dialog_width = 600
        dialog_height = 200
        dialog_x = (BOARD_WIDTH - dialog_width) // 2
        dialog_y = (HEIGHT - dialog_height) // 2

        button_width = 120
        button_height = 100
        button_spacing = 20
        start_x = dialog_x + 30
        button_y = dialog_y + 70

        promotion_pieces = ['Q', 'R', 'B', 'N']

        for i, piece_type in enumerate(promotion_pieces):
            button_x = start_x + i * (button_width + button_spacing)

            if (button_x <= pos[0] <= button_x + button_width and
                button_y <= pos[1] <= button_y + button_height):
                row, col = self.board.pending_promotion
                self.board.promote_pawn(row, col, piece_type)
                return True

        return False

    def handle_click(self, pos):
        # Check if clicking on promotion dialog
        if self.board.pending_promotion:
            if self.handle_promotion_click(pos):
                return

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
            self.draw_legend()
            self.draw_promotion_dialog()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = ChessGame()
    game.run()
