import pygame
import random

# ゲームの初期化
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('テトリス風ゲーム')

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# テトリミノの形状定義
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# テトリミノの色
COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

# ゲームボードの設定
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30
BOARD_X = (screen_width - BOARD_WIDTH * BLOCK_SIZE) // 2
BOARD_Y = screen_height - BOARD_HEIGHT * BLOCK_SIZE - 20

# ゲームボードの初期化
board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# テトリミノクラス
class Tetrimino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.color = COLORS[self.shape_idx]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        # 回転処理（時計回り）
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.shape[r][c]
        
        # 回転後の形状が有効かチェック
        old_shape = self.shape
        self.shape = rotated
        if not self.is_valid_position():
            self.shape = old_shape
    
    def move_left(self):
        self.x -= 1
        if not self.is_valid_position():
            self.x += 1
    
    def move_right(self):
        self.x += 1
        if not self.is_valid_position():
            self.x -= 1
    
    def move_down(self):
        self.y += 1
        if not self.is_valid_position():
            self.y -= 1
            return False
        return True
    
    def is_valid_position(self):
        for r in range(len(self.shape)):
            for c in range(len(self.shape[0])):
                if self.shape[r][c] == 0:
                    continue
                
                # ボード外チェック
                if self.y + r >= BOARD_HEIGHT or self.x + c < 0 or self.x + c >= BOARD_WIDTH:
                    return False
                
                # 他のブロックとの衝突チェック
                if self.y + r >= 0 and board[self.y + r][self.x + c] != 0:
                    return False
        
        return True
    
    def lock(self):
        for r in range(len(self.shape)):
            for c in range(len(self.shape[0])):
                if self.shape[r][c] == 0:
                    continue
                
                if self.y + r >= 0:
                    board[self.y + r][self.x + c] = self.color

# 行が揃っているかチェックして消去
def clear_lines():
    lines_cleared = 0
    for y in range(BOARD_HEIGHT - 1, -1, -1):
        if all(board[y]):
            for y2 in range(y, 0, -1):
                board[y2] = board[y2 - 1][:]
            board[0] = [0] * BOARD_WIDTH
            lines_cleared += 1
    return lines_cleared

# ゲームボードの描画
def draw_board():
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] != 0:
                pygame.draw.rect(screen, board[y][x], 
                                [BOARD_X + x * BLOCK_SIZE, 
                                 BOARD_Y + y * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.rect(screen, WHITE, 
                                [BOARD_X + x * BLOCK_SIZE, 
                                 BOARD_Y + y * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE], 1)

# テトリミノの描画
def draw_tetrimino(tetrimino):
    for r in range(len(tetrimino.shape)):
        for c in range(len(tetrimino.shape[0])):
            if tetrimino.shape[r][c] != 0:
                pygame.draw.rect(screen, tetrimino.color, 
                                [BOARD_X + (tetrimino.x + c) * BLOCK_SIZE, 
                                 BOARD_Y + (tetrimino.y + r) * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.rect(screen, WHITE, 
                                [BOARD_X + (tetrimino.x + c) * BLOCK_SIZE, 
                                 BOARD_Y + (tetrimino.y + r) * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE], 1)

# ゲームオーバーチェック
def is_game_over():
    return any(board[0])

# ゲームループ
def main():
    clock = pygame.time.Clock()
    current_tetrimino = Tetrimino()
    fall_time = 0
    fall_speed = 500  # ミリ秒
    score = 0
    font = pygame.font.SysFont(None, 36)
    
    running = True
    game_over = False
    
    while running:
        # 時間経過によるテトリミノの落下
        fall_time += clock.get_rawtime()
        clock.tick()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_tetrimino.move_left()
                    elif event.key == pygame.K_RIGHT:
                        current_tetrimino.move_right()
                    elif event.key == pygame.K_DOWN:
                        current_tetrimino.move_down()
                    elif event.key == pygame.K_UP:
                        current_tetrimino.rotate()
                    elif event.key == pygame.K_SPACE:
                        # ハードドロップ
                        while current_tetrimino.move_down():
                            pass
        
        if not game_over:
            # 自動落下
            if fall_time >= fall_speed:
                fall_time = 0
                if not current_tetrimino.move_down():
                    current_tetrimino.lock()
                    lines = clear_lines()
                    score += lines * 100
                    
                    # 新しいテトリミノ
                    current_tetrimino = Tetrimino()
                    if not current_tetrimino.is_valid_position():
                        game_over = True
        
        # 画面描画
        screen.fill(BLACK)
        
        # ボード枠の描画
        pygame.draw.rect(screen, WHITE, 
                        [BOARD_X - 2, BOARD_Y - 2, 
                         BOARD_WIDTH * BLOCK_SIZE + 4, 
                         BOARD_HEIGHT * BLOCK_SIZE + 4], 2)
        
        draw_board()
        if not game_over:
            draw_tetrimino(current_tetrimino)
        
        # スコア表示
        score_text = font.render(f"スコア: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        if game_over:
            game_over_text = font.render("ゲームオーバー", True, RED)
            screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 30))
            restart_text = font.render("Rキーで再スタート", True, WHITE)
            screen.blit(restart_text, (screen_width // 2 - 100, screen_height // 2 + 10))
            
            # リスタート
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                board.clear()
                board.extend([[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)])
                current_tetrimino = Tetrimino()
                score = 0
                game_over = False
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
