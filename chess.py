import pygame
import sys
from copy import deepcopy
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

# Colors
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
HIGHLIGHT = (186, 202, 68)
SELECTED = (246, 246, 130)

# Piece values - QUEEN IS ABSOLUTE PRIORITY
PIECE_VALUES = {
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 9000, 'K': 20000,  # TĂNG GIÁ TRỊ HẬU LÊN 9000
    'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -9000, 'k': -20000
}

# Position tables (giữ nguyên)
PAWN_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 27, 27, 10,  5,  5],
    [0,  0,  0, 25, 25,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-25,-25, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [0,  0,  0,  5,  5,  0,  0,  0],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [0,  0, 5,  5,  5,  5,  0, -5],
    [-5,  0, 5,  5,  5,  5,  0, -5],
    [-10,  0, 5,  5,  5,  5,  0,-10],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_MIDDLE_GAME_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

KING_END_GAME_TABLE = [
    [-50,-30,-30,-30,-30,-30,-30,-50],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-50,-40,-30,-20,-20,-30,-40,-50]
]

def load_images():
    """Load piece images"""
    pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    
    unicode_symbols = {
        'wK': '♔', 'wQ': '♕', 'wR': '♖', 'wB': '♗', 'wN': '♘', 'wP': '♙',
        'bK': '♚', 'bQ': '♛', 'bR': '♜', 'bB': '♝', 'bN': '♞', 'bP': '♟'
    }
    
    for piece in pieces:
        img = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        
        try:
            font = pygame.font.SysFont('segoeuisymbol,dejavusans,freesans,arial', int(SQ_SIZE * 0.8))
        except:
            font = pygame.font.Font(None, int(SQ_SIZE * 0.8))
        
        if piece[0] == 'w':
            color = (255, 255, 255)
            outline_color = (0, 0, 0)
        else:
            color = (0, 0, 0)
            outline_color = (255, 255, 255)
        
        symbol = unicode_symbols[piece]
        center = (SQ_SIZE // 2, SQ_SIZE // 2)
        
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    text_outline = font.render(symbol, True, outline_color)
                    text_rect = text_outline.get_rect(center=(center[0] + dx, center[1] + dy))
                    img.blit(text_outline, text_rect)
        
        text = font.render(symbol, True, color)
        text_rect = text.get_rect(center=center)
        img.blit(text, text_rect)
        
        IMAGES[piece] = img

class ChessBoard:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.white_to_move = True
        self.move_log = []
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check_cache = {}
        
        # Thêm trạng thái nhập thành
        self.castle_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.castle_rights.wks, self.castle_rights.bks, 
                                              self.castle_rights.wqs, self.castle_rights.bqs)]
        
        # Biến để lưu nước đi phong cấp
        self.promotion_choice = None

    def make_move(self, move):
        """Execute a move"""
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        self.in_check_cache.clear()
        
        # Cập nhật vị trí vua
        if move.piece_moved == 'wK':
            self.white_king_pos = (move.end_row, move.end_col)
            # Mất quyền nhập thành sau khi vua di chuyển
            self.castle_rights.wks = False
            self.castle_rights.wqs = False
        elif move.piece_moved == 'bK':
            self.black_king_pos = (move.end_row, move.end_col)
            self.castle_rights.bks = False
            self.castle_rights.bqs = False
            
        # Xử lý phong cấp
        if move.is_pawn_promotion:
            # Mặc định phong thành hậu, nhưng có thể thay đổi sau
            promotion_piece = 'Q' if move.piece_moved[0] == 'w' else 'q'
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + promotion_piece
            
        # Xử lý nhập thành
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # Nhập thành cánh vua
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = '--'
            else:  # Nhập thành cánh hậu
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]
                self.board[move.end_row][move.end_col-2] = '--'
                
        # Cập nhật quyền nhập thành khi xe di chuyển
        if move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:  # Xe trái
                    self.castle_rights.wqs = False
                elif move.start_col == 7:  # Xe phải
                    self.castle_rights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:  # Xe trái
                    self.castle_rights.bqs = False
                elif move.start_col == 7:  # Xe phải
                    self.castle_rights.bks = False
                    
        # Cập nhật quyền nhập thành khi xe bị bắt
        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.castle_rights.wqs = False
                elif move.end_col == 7:
                    self.castle_rights.wks = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.castle_rights.bqs = False
                elif move.end_col == 7:
                    self.castle_rights.bks = False
        
        # Lưu trạng thái quyền nhập thành
        self.castle_rights_log.append(CastleRights(self.castle_rights.wks, self.castle_rights.bks,
                                                  self.castle_rights.wqs, self.castle_rights.bqs))

    def undo_move(self):
        """Undo a move"""
        if len(self.move_log) > 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            self.in_check_cache.clear()
            
            # Khôi phục vị trí vua
            if move.piece_moved == 'wK':
                self.white_king_pos = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_pos = (move.start_row, move.start_col)
                
            # Hoàn tác nhập thành
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # Nhập thành cánh vua
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1] = '--'
                else:  # Nhập thành cánh hậu
                    self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                    self.board[move.end_row][move.end_col+1] = '--'
            
            # Khôi phục quyền nhập thành
            self.castle_rights_log.pop()
            if len(self.castle_rights_log) > 0:
                self.castle_rights = self.castle_rights_log[-1]

    def get_valid_moves(self):
        """Get all valid moves"""
        # Lưu trạng thái quyền nhập thành hiện tại
        temp_castle_rights = CastleRights(self.castle_rights.wks, self.castle_rights.bks,
                                         self.castle_rights.wqs, self.castle_rights.bqs)
        
        moves = self.get_all_possible_moves()
        
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
            
        # Khôi phục quyền nhập thành (phòng trường hợp bị thay đổi trong quá trình kiểm tra)
        self.castle_rights = temp_castle_rights
            
        return moves

    def in_check(self):
        """Check if the king is in check"""
        if self.white_to_move:
            return self.square_under_attack(self.white_king_pos[0], self.white_king_pos[1])
        else:
            return self.square_under_attack(self.black_king_pos[0], self.black_king_pos[1])

    def square_under_attack(self, r, c):
        """Check if square (r, c) is under attack"""
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    def get_all_possible_moves(self):
        """Get all possible moves"""
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.get_pawn_moves(r, c, moves)
                    elif piece == 'R':
                        self.get_rook_moves(r, c, moves)
                    elif piece == 'N':
                        self.get_knight_moves(r, c, moves)
                    elif piece == 'B':
                        self.get_bishop_moves(r, c, moves)
                    elif piece == 'Q':
                        self.get_queen_moves(r, c, moves)
                    elif piece == 'K':
                        self.get_king_moves(r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        """Generate pawn moves"""
        if self.white_to_move:
            if self.board[r-1][c] == '--':
                # Di chuyển tiến 1 ô
                if r-1 == 0:  # Phong cấp
                    moves.append(Move((r, c), (r-1, c), self.board, is_pawn_promotion=True))
                else:
                    moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    if r-1 == 0:  # Phong cấp
                        moves.append(Move((r, c), (r-1, c-1), self.board, is_pawn_promotion=True))
                    else:
                        moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    if r-1 == 0:  # Phong cấp
                        moves.append(Move((r, c), (r-1, c+1), self.board, is_pawn_promotion=True))
                    else:
                        moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == '--':
                # Di chuyển tiến 1 ô
                if r+1 == 7:  # Phong cấp
                    moves.append(Move((r, c), (r+1, c), self.board, is_pawn_promotion=True))
                else:
                    moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    if r+1 == 7:  # Phong cấp
                        moves.append(Move((r, c), (r+1, c-1), self.board, is_pawn_promotion=True))
                    else:
                        moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    if r+1 == 7:  # Phong cấp
                        moves.append(Move((r, c), (r+1, c+1), self.board, is_pawn_promotion=True))
                    else:
                        moves.append(Move((r, c), (r+1, c+1), self.board))

    def get_rook_moves(self, r, c, moves):
        """Generate rook moves"""
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, r, c, moves):
        """Generate knight moves"""
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        """Generate bishop moves"""
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, r, c, moves):
        """Generate queen moves"""
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        """Generate king moves including castling"""
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                    
        # Thêm nước đi nhập thành
        if self.white_to_move:
            if self.castle_rights.wks and self.board[7][5] == '--' and self.board[7][6] == '--':
                if not self.square_under_attack(7, 4) and not self.square_under_attack(7, 5) and not self.square_under_attack(7, 6):
                    moves.append(Move((7, 4), (7, 6), self.board, is_castle_move=True))
            if self.castle_rights.wqs and self.board[7][1] == '--' and self.board[7][2] == '--' and self.board[7][3] == '--':
                if not self.square_under_attack(7, 4) and not self.square_under_attack(7, 3) and not self.square_under_attack(7, 2):
                    moves.append(Move((7, 4), (7, 2), self.board, is_castle_move=True))
        else:
            if self.castle_rights.bks and self.board[0][5] == '--' and self.board[0][6] == '--':
                if not self.square_under_attack(0, 4) and not self.square_under_attack(0, 5) and not self.square_under_attack(0, 6):
                    moves.append(Move((0, 4), (0, 6), self.board, is_castle_move=True))
            if self.castle_rights.bqs and self.board[0][1] == '--' and self.board[0][2] == '--' and self.board[0][3] == '--':
                if not self.square_under_attack(0, 4) and not self.square_under_attack(0, 3) and not self.square_under_attack(0, 2):
                    moves.append(Move((0, 4), (0, 2), self.board, is_castle_move=True))

class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks  # White king side
        self.bks = bks  # Black king side
        self.wqs = wqs  # White queen side
        self.bqs = bqs  # Black queen side

class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_pawn_promotion=False, is_castle_move=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        
        # Cờ cho phong cấp và nhập thành
        self.is_pawn_promotion = is_pawn_promotion
        self.is_castle_move = is_castle_move

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        # Thêm ký hiệu đặc biệt cho nhập thành
        if self.is_castle_move:
            if self.end_col - self.start_col == 2:  # Nhập thành cánh vua
                return "O-O"
            else:  # Nhập thành cánh hậu
                return "O-O-O"
                
        # Thêm ký hiệu cho phong cấp
        promotion_text = ""
        if self.is_pawn_promotion:
            promotion_text = "=Q"  # Mặc định phong hậu
            
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col) + promotion_text

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]

class ChessAI:
    def __init__(self, depth=4):
        self.depth = depth
        self.nodes_evaluated = 0
        self.transposition_table = {}

    def is_endgame(self, board):
        """Check if in endgame"""
        queens = 0
        minors = 0
        for r in range(8):
            for c in range(8):
                piece = board.board[r][c]
                if piece != '--':
                    if piece[1] == 'Q':
                        queens += 1
                    elif piece[1] in ['N', 'B']:
                        minors += 1
        return queens == 0 or (queens == 2 and minors <= 2)

    def evaluate_board(self, board):
        """Enhanced board evaluation"""
        if board.checkmate:
            return -99999 if board.white_to_move else 99999
        elif board.stalemate:
            return 0

        score = 0
        is_endgame = self.is_endgame(board)
        
        for r in range(8):
            for c in range(8):
                piece = board.board[r][c]
                if piece != '--':
                    piece_value = PIECE_VALUES[piece[1]]
                    
                    # Position bonus
                    position_bonus = 0
                    if piece[1] == 'P':
                        position_bonus = PAWN_TABLE[r][c] if piece[0] == 'w' else PAWN_TABLE[7-r][c]
                    elif piece[1] == 'N':
                        position_bonus = KNIGHT_TABLE[r][c] if piece[0] == 'w' else KNIGHT_TABLE[7-r][c]
                    elif piece[1] == 'B':
                        position_bonus = BISHOP_TABLE[r][c] if piece[0] == 'w' else BISHOP_TABLE[7-r][c]
                    elif piece[1] == 'R':
                        position_bonus = ROOK_TABLE[r][c] if piece[0] == 'w' else ROOK_TABLE[7-r][c]
                    elif piece[1] == 'Q':
                        position_bonus = QUEEN_TABLE[r][c] if piece[0] == 'w' else QUEEN_TABLE[7-r][c]
                    elif piece[1] == 'K':
                        if is_endgame:
                            position_bonus = KING_END_GAME_TABLE[r][c] if piece[0] == 'w' else KING_END_GAME_TABLE[7-r][c]
                        else:
                            position_bonus = KING_MIDDLE_GAME_TABLE[r][c] if piece[0] == 'w' else KING_MIDDLE_GAME_TABLE[7-r][c]
                    
                    if piece[0] == 'w':
                        score += piece_value + position_bonus
                    else:
                        score -= abs(piece_value) + position_bonus
        
        # Mobility bonus
        white_mobility = len(board.get_all_possible_moves()) if board.white_to_move else 0
        board.white_to_move = not board.white_to_move
        black_mobility = len(board.get_all_possible_moves()) if not board.white_to_move else 0
        board.white_to_move = not board.white_to_move
        
        score += (white_mobility - black_mobility) * 10
        
        # Thêm điểm thưởng cho nhập thành
        if board.castle_rights.wks or board.castle_rights.wqs:
            score += 50
        if board.castle_rights.bks or board.castle_rights.bqs:
            score -= 50
            
        return score

    def find_best_move(self, board):
        """Find best move with ABSOLUTE QUEEN PROTECTION"""
        self.nodes_evaluated = 0
        self.transposition_table.clear()
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            return None
        
        # ULTRA PRIORITY: Check for queen threats and handle them ABSOLUTELY
        queen_emergency_moves = self.get_queen_emergency_moves(board)
        if queen_emergency_moves:
            print("🚨🚨🚨 CRITICAL: QUEEN IN DANGER! Taking emergency action...")
            # Only consider moves that save the queen
            valid_moves = queen_emergency_moves
        
        best_move = None
        best_value = -float('inf') if board.white_to_move else float('inf')
        alpha = -float('inf')
        beta = float('inf')

        # Sort moves with queen safety as ABSOLUTE priority
        valid_moves.sort(key=lambda move: self.score_move(board, move), reverse=True)

        for move in valid_moves:
            # ABSOLUTE VETO: Reject any move that sacrifices queen for minor piece
            if self.is_queen_sacrifice(board, move):
                print(f"🚫 REJECTED: Queen sacrifice move {move.get_chess_notation()}")
                continue
                
            board.make_move(move)
            value = self.minimax(board, self.depth - 1, alpha, beta, not board.white_to_move)
            board.undo_move()

            if board.white_to_move:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)

        # DESPERATION: If no good moves, choose random safe move
        if best_move is None and valid_moves:
            safe_moves = [m for m in valid_moves if not self.is_queen_sacrifice(board, m)]
            if safe_moves:
                best_move = random.choice(safe_moves)
                print("⚠️ No optimal moves, choosing random safe move")
            else:
                best_move = valid_moves[0]
                print("💀 ALL MOVES RISK QUEEN! Choosing least bad option")

        print(f"Nodes: {self.nodes_evaluated}, Score: {best_value}, Move: {best_move.get_chess_notation() if best_move else 'None'}")
        return best_move

    def is_queen_sacrifice(self, board, move):
        """ABSOLUTE CHECK: Is this move sacrificing queen for inferior piece?"""
        # If not capturing with queen, check if queen will be captured
        if move.piece_moved[1] != 'Q':
            # Find queen position
            queen_square = None
            queen_color = 'w' if board.white_to_move else 'b'
            for r in range(8):
                for c in range(8):
                    if board.board[r][c] == queen_color + 'Q':
                        queen_square = (r, c)
                        break
                if queen_square:
                    break
            
            if not queen_square:
                return False
            
            # Simulate the move
            original_piece = board.board[move.end_row][move.end_col]
            board.board[move.end_row][move.end_col] = move.piece_moved
            board.board[move.start_row][move.start_col] = '--'
            
            # Check if queen becomes attacked AND can be captured by inferior piece
            enemy_color = 'b' if board.white_to_move else 'w'
            queen_attacked = self.is_square_attacked_by(board, queen_square[0], queen_square[1], enemy_color)
            
            if queen_attacked:
                # Check what pieces are attacking the queen
                attackers = self.get_attackers_to_square(board, queen_square[0], queen_square[1], enemy_color)
                # If any attacker has value less than queen, it's a sacrifice
                for attacker in attackers:
                    attacker_value = abs(PIECE_VALUES[attacker[1]])
                    if attacker_value < 9000:  # Queen value is 9000
                        # Restore board and return True
                        board.board[move.start_row][move.start_col] = move.piece_moved
                        board.board[move.end_row][move.end_col] = original_piece
                        return True
            
            # Restore board
            board.board[move.start_row][move.start_col] = move.piece_moved
            board.board[move.end_row][move.end_col] = original_piece
        
        # If moving queen, check if it's captured by inferior piece
        elif move.piece_moved[1] == 'Q':
            enemy_color = 'b' if move.piece_moved[0] == 'w' else 'w'
            will_be_captured = self.is_square_attacked_by(board, move.end_row, move.end_col, enemy_color)
            
            if will_be_captured:
                attackers = self.get_attackers_to_square(board, move.end_row, move.end_col, enemy_color)
                for attacker in attackers:
                    attacker_value = abs(PIECE_VALUES[attacker[1]])
                    if attacker_value < 9000 and move.piece_captured != '--':
                        captured_value = abs(PIECE_VALUES[move.piece_captured[1]])
                        if captured_value < 9000:  # Not trading queens
                            return True
        
        return False

    def get_queen_emergency_moves(self, board):
        """GET MOVES THAT ABSOLUTELY SAVE THE QUEEN - NO EXCEPTIONS"""
        queen_square = None
        queen_color = 'w' if board.white_to_move else 'b'
        
        # Find queen position
        for r in range(8):
            for c in range(8):
                if board.board[r][c] == queen_color + 'Q':
                    queen_square = (r, c)
                    break
            if queen_square:
                break
        
        if not queen_square:
            return []
        
        # Check if queen is under attack
        enemy_color = 'b' if board.white_to_move else 'w'
        queen_attacked = self.is_square_attacked_by(board, queen_square[0], queen_square[1], enemy_color)
        
        if not queen_attacked:
            return []
        
        print(f"🚨 QUEEN EMERGENCY at {self.square_to_notation(queen_square)}!")
        
        # Get ALL moves that save the queen
        emergency_moves = []
        valid_moves = board.get_valid_moves()
        
        for move in valid_moves:
            # Move queen to safety
            if move.start_row == queen_square[0] and move.start_col == queen_square[1]:
                board.make_move(move)
                still_attacked = self.is_square_attacked_by(board, move.end_row, move.end_col, enemy_color)
                board.undo_move()
                if not still_attacked:
                    emergency_moves.append(move)
                    print(f"   ✅ Queen escape: {move.get_chess_notation()}")
            # Capture the attacker
            else:
                # Check if this move captures a piece that's attacking the queen
                captures_attacker = False
                for attacker_pos in self.get_attacker_positions(board, queen_square[0], queen_square[1], enemy_color):
                    if move.end_row == attacker_pos[0] and move.end_col == attacker_pos[1]:
                        captures_attacker = True
                        break
                
                if captures_attacker:
                    emergency_moves.append(move)
                    print(f"   ✅ Capture attacker: {move.get_chess_notation()}")
                else:
                    # Check if move blocks the attack
                    board.make_move(move)
                    still_attacked = self.is_square_attacked_by(board, queen_square[0], queen_square[1], enemy_color)
                    board.undo_move()
                    if not still_attacked:
                        emergency_moves.append(move)
                        print(f"   ✅ Block attack: {move.get_chess_notation()}")
        
        return emergency_moves

    def get_attacker_positions(self, board, row, col, attacker_color):
        """Get positions of all pieces attacking a square"""
        attackers = []
        
        # Check pawn attacks
        pawn_direction = -1 if attacker_color == 'w' else 1
        if 0 <= row - pawn_direction < 8:
            if col > 0 and board.board[row - pawn_direction][col - 1] == attacker_color + 'P':
                attackers.append((row - pawn_direction, col - 1))
            if col < 7 and board.board[row - pawn_direction][col + 1] == attacker_color + 'P':
                attackers.append((row - pawn_direction, col + 1))
        
        # Check knight attacks
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board.board[r][c] == attacker_color + 'N':
                attackers.append((r, c))
        
        # Check sliding pieces
        # Rook/Queen - horizontal/vertical
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board.board[r][c]
                if piece != '--':
                    if piece in [attacker_color + 'R', attacker_color + 'Q']:
                        attackers.append((r, c))
                    break
                r += dr
                c += dc
        
        # Bishop/Queen - diagonal
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board.board[r][c]
                if piece != '--':
                    if piece in [attacker_color + 'B', attacker_color + 'Q']:
                        attackers.append((r, c))
                    break
                r += dr
                c += dc
        
        return attackers

    def get_attackers_to_square(self, board, row, col, attacker_color):
        """Get the types of pieces attacking a square"""
        attackers = []
        
        # Check pawn attacks
        pawn_direction = -1 if attacker_color == 'w' else 1
        if 0 <= row - pawn_direction < 8:
            if col > 0 and board.board[row - pawn_direction][col - 1] == attacker_color + 'P':
                attackers.append(attacker_color + 'P')
            if col < 7 and board.board[row - pawn_direction][col + 1] == attacker_color + 'P':
                attackers.append(attacker_color + 'P')
        
        # Check knight attacks
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board.board[r][c] == attacker_color + 'N':
                attackers.append(attacker_color + 'N')
        
        # Check sliding pieces
        # Rook/Queen - horizontal/vertical
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board.board[r][c]
                if piece != '--':
                    if piece in [attacker_color + 'R', attacker_color + 'Q']:
                        attackers.append(piece)
                    break
                r += dr
                c += dc
        
        # Bishop/Queen - diagonal
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board.board[r][c]
                if piece != '--':
                    if piece in [attacker_color + 'B', attacker_color + 'Q']:
                        attackers.append(piece)
                    break
                r += dr
                c += dc
        
        return attackers

    def square_to_notation(self, square):
        """Convert (row, col) to chess notation"""
        files = "abcdefgh"
        return files[square[1]] + str(8 - square[0])

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """Minimax with ABSOLUTE queen protection"""
        self.nodes_evaluated += 1

        if depth == 0 or board.checkmate or board.stalemate:
            return self.evaluate_board(board)

        valid_moves = board.get_all_possible_moves()
        
        # ULTRA filtering: Remove ANY move that risks queen at lower depths
        if depth < self.depth - 1:
            valid_moves = [move for move in valid_moves if not self.is_queen_sacrifice(board, move)]
            
        valid_moves.sort(key=lambda move: self.score_move(board, move), reverse=maximizing_player)

        if maximizing_player:
            max_eval = -float('inf')
            for move in valid_moves:
                board.make_move(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board.make_move(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def is_square_attacked_by(self, board, row, col, attacker_color):
        """Check if a square is attacked by a specific color"""
        # Check pawn attacks
        pawn_direction = -1 if attacker_color == 'w' else 1
        if 0 <= row - pawn_direction < 8:
            if col > 0 and board.board[row - pawn_direction][col - 1] == attacker_color + 'P':
                return True
            if col < 7 and board.board[row - pawn_direction][col + 1] == attacker_color + 'P':
                return True
        
        # Check knight attacks
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board.board[r][c] == attacker_color + 'N':
                return True
        
        # Check king attacks
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8 and board.board[r][c] == attacker_color + 'K':
                    return True
        
        # Check sliding pieces (Rook, Bishop, Queen)
        # Rook and Queen (horizontal/vertical)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board.board[r][c]
                if piece != '--':
                    if piece in [attacker_color + 'R', attacker_color + 'Q']:
                        return True
                    break
                r += dr
                c += dc
        
        # Bishop and Queen (diagonal)
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board.board[r][c]
                if piece != '--':
                    if piece in [attacker_color + 'B', attacker_color + 'Q']:
                        return True
                    break
                r += dr
                c += dc
        
        return False

    def score_move(self, board, move):
        """ABSOLUTE QUEEN PROTECTION scoring"""
        score = 0
        piece_value = abs(PIECE_VALUES[move.piece_moved[1]])
        
        # ULTRA PRIORITY: Queen protection
        if move.piece_moved[1] == 'Q':
            enemy_color = 'b' if move.piece_moved[0] == 'w' else 'w'
            destination_safe = not self.is_square_attacked_by(board, move.end_row, move.end_col, enemy_color)
            
            if not destination_safe:
                # Queen moving to attacked square = CATASTROPHIC
                score -= 50000  # Massive penalty
                # Only acceptable if trading queens
                if move.piece_captured == ('bQ' if move.piece_moved[0] == 'w' else 'wQ'):
                    score += 40000  # Queen trade is acceptable
            else:
                # Queen moving safely = good
                score += 200
        
        # Check if move sacrifices queen for minor piece
        if self.is_queen_sacrifice(board, move):
            score -= 100000  # ABSOLUTELY UNACCEPTABLE
        
        # Thêm điểm thưởng cho nhập thành
        if move.is_castle_move:
            score += 100
        
        # Thêm điểm thưởng cho phong cấp
        if move.is_pawn_promotion:
            score += 900  # Thưởng lớn cho phong cấp
        
        # Regular material evaluation
        if move.piece_captured != '--':
            captured_value = abs(PIECE_VALUES[move.piece_captured[1]])
            score += captured_value * 10
        
        # Positional bonuses
        center_distance = abs(3.5 - move.end_row) + abs(3.5 - move.end_col)
        score -= center_distance * 3
        
        # Development bonus
        if move.piece_moved[1] in ['N', 'B']:
            if move.start_row == (7 if move.piece_moved[0] == 'w' else 0):
                score += 30
        
        # Small randomness to avoid repetition
        score += random.randint(0, 3)
        
        return score

def draw_game_state(screen, board, valid_moves, sq_selected):
    """Draw the board and pieces"""
    draw_board(screen)
    highlight_squares(screen, board, valid_moves, sq_selected)
    draw_pieces(screen, board)

def draw_board(screen):
    """Draw the chess board"""
    colors = [WHITE, BLACK]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlight_squares(screen, board, valid_moves, sq_selected):
    """Highlight selected square and valid moves"""
    if sq_selected != ():
        r, c = sq_selected
        if board.board[r][c][0] == ('w' if board.white_to_move else 'b'):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(SELECTED)
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            
            s.fill(HIGHLIGHT)
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))

def draw_pieces(screen, board):
    """Draw the pieces"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board.board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_text(screen, text):
    """Draw text on screen"""
    font = pygame.font.SysFont("Arial", 32, True, False)
    text_object = font.render(text, 0, pygame.Color('Red'))
    text_location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, pygame.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    pygame.display.set_caption('Chess AI - ULTRA Queen Protection')
    
    board = ChessBoard()
    ai = ChessAI(depth=4)
    valid_moves = board.get_valid_moves()
    move_made = False
    load_images()
    
    running = True
    sq_selected = ()
    player_clicks = []
    game_over = False
    player_one = True
    player_two = False

    print("Hướng dẫn:")
    print("- Click chuột để di chuyển quân")
    print("- Nhấn Z để hoàn tác")
    print("- Nhấn R để bắt đầu ván mới")
    print("- AI đang chơi quân ĐEN")
    print("-" * 50)

    while running:
        human_turn = (board.white_to_move and player_one) or (not board.white_to_move and player_two)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = pygame.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    
                    if sq_selected == (row, col):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    
                    if len(player_clicks) == 2:
                        move = Move(player_clicks[0], player_clicks[1], board.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                board.make_move(valid_moves[i])
                                move_made = True
                                sq_selected = ()
                                player_clicks = []
                                print(f"Player move: {valid_moves[i].get_chess_notation()}")
                        if not move_made:
                            player_clicks = [sq_selected]
            
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    board.undo_move()
                    board.undo_move()
                    move_made = True
                    game_over = False
                    print("Đã hoàn tác 2 nước")
                if e.key == pygame.K_r:
                    board = ChessBoard()
                    valid_moves = board.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    game_over = False
                    ai.transposition_table.clear()
                    print("Bắt đầu ván mới!")
        
        # AI move
        if not game_over and not human_turn:
            print("AI đang suy nghĩ...")
            ai_move = ai.find_best_move(board)
            if ai_move:
                board.make_move(ai_move)
                move_made = True
                print(f"AI move: {ai_move.get_chess_notation()}")
        
        if move_made:
            valid_moves = board.get_valid_moves()
            move_made = False
        
        draw_game_state(screen, board, valid_moves, sq_selected)
        
        if board.checkmate:
            game_over = True
            if board.white_to_move:
                draw_text(screen, 'Black wins by checkmate!')
                print("ĐEN THẮNG!")
            else:
                draw_text(screen, 'White wins by checkmate!')
                print("TRẮNG THẮNG!")
        elif board.stalemate:
            game_over = True
            draw_text(screen, 'Stalemate!')
            print("HÒA!")
        
        clock.tick(MAX_FPS)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()