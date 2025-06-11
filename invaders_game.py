import pygame
import random
import sys

# ゲームの初期化
pygame.init()

# 画面サイズの設定
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('インベーダー風ゲーム')

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.shoot_delay = 250  # ミリ秒
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        # キー入力による移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # 画面端での制限
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return Bullet(self.rect.centerx, self.rect.top)
        return None

# 敵クラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # 1: 右, -1: 左
        self.speed = 2
    
    def update(self):
        self.rect.x += self.speed * self.direction

# 弾クラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10  # 上向きに移動するので負の値
    
    def update(self):
        self.rect.y += self.speed
        # 画面外に出たら削除
        if self.rect.bottom < 0:
            self.kill()

# 敵の弾クラス
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 7
    
    def update(self):
        self.rect.y += self.speed
        # 画面外に出たら削除
        if self.rect.top > HEIGHT:
            self.kill()

# ゲームクラス
class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # 日本語フォントの設定
        try:
            # macOSで利用可能な日本語フォントを試みる
            self.font = pygame.font.Font('/Library/Fonts/SourceHanCodeJP.ttc', 36)
        except:
            try:
                # 一般的な日本語フォントを試みる
                self.font = pygame.font.Font('/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc', 36)
            except:
                # フォールバック: システムのデフォルトフォント
                self.font = pygame.font.SysFont(None, 36)
                print("警告: 日本語フォントが見つかりませんでした。文字化けする可能性があります。")
        
        self.running = True
        self.game_over = False
        self.score = 0
        self.level = 1
        
        # スプライトグループの作成
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        
        # プレイヤーの作成
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # 敵の作成
        self.create_enemies()
        
        # 敵の移動方向変更タイマー
        self.enemy_move_down = False
        self.last_enemy_direction_change = pygame.time.get_ticks()
        self.enemy_direction_change_delay = 2000  # 2秒ごとに方向変更
        
        # 敵の射撃タイマー
        self.last_enemy_shot = pygame.time.get_ticks()
        self.enemy_shot_delay = 1000  # 1秒ごとに射撃
    
    def create_enemies(self):
        # 敵を5行8列で配置
        for row in range(5):
            for col in range(8):
                enemy = Enemy(col * 80 + 80, row * 60 + 50)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
    
    def events(self):
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = self.player.shoot()
                    if bullet:
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()  # ゲームリセット
    
    def update(self):
        if not self.game_over:
            # スプライトの更新
            self.all_sprites.update()
            
            # 敵の方向変更
            now = pygame.time.get_ticks()
            if now - self.last_enemy_direction_change > self.enemy_direction_change_delay:
                self.last_enemy_direction_change = now
                self.enemy_move_down = True
                for enemy in self.enemies:
                    enemy.direction *= -1
            
            if self.enemy_move_down:
                for enemy in self.enemies:
                    enemy.rect.y += 20
                self.enemy_move_down = False
            
            # 敵の射撃
            if now - self.last_enemy_shot > self.enemy_shot_delay and self.enemies:
                self.last_enemy_shot = now
                shooting_enemy = random.choice(self.enemies.sprites())
                enemy_bullet = EnemyBullet(shooting_enemy.rect.centerx, shooting_enemy.rect.bottom)
                self.all_sprites.add(enemy_bullet)
                self.enemy_bullets.add(enemy_bullet)
            
            # 弾と敵の衝突判定
            hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
            for hit in hits:
                self.score += 100
            
            # 敵の弾とプレイヤーの衝突判定
            hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
            if hits:
                self.game_over = True
            
            # 敵とプレイヤーの衝突判定
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hits:
                self.game_over = True
            
            # 敵が画面下部に到達したらゲームオーバー
            for enemy in self.enemies:
                if enemy.rect.bottom > HEIGHT - 50:
                    self.game_over = True
            
            # 敵を全滅させたら次のレベルへ
            if len(self.enemies) == 0:
                self.level += 1
                self.enemy_direction_change_delay = max(500, self.enemy_direction_change_delay - 200)
                self.enemy_shot_delay = max(200, self.enemy_shot_delay - 100)
                self.create_enemies()
    
    def draw(self):
        # 描画処理
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        # スコアとレベルの表示
        score_text = self.font.render(f"スコア: {self.score}", True, WHITE)
        level_text = self.font.render(f"レベル: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (WIDTH - 150, 10))
        
        if self.game_over:
            game_over_text = self.font.render("ゲームオーバー", True, RED)
            restart_text = self.font.render("Rキーでリスタート", True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
            self.screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
        
        pygame.display.flip()
    
    def run(self):
        # ゲームループ
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        
        pygame.quit()
        sys.exit()

# ゲーム実行
if __name__ == "__main__":
    game = Game()
    game.run()
