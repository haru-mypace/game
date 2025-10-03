import pygame

# 画面の大きさ
WIDTH  = 700
HEIGHT = 480
# 色の設定
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)

# ボールの座標
ball_x = 10
ball_y = 10
# ボールの速さ
ball_dx = 5
ball_dy = 5

# パドルの座標
paddle_x = 250

pygame.init()  # Pygameを初期化
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 画面作成
clock = pygame.time.Clock()  # 時計作成
running  = True  # 実行継続フラグ

score = 0  # スコアを初期化
scoreboard = "score: " + str(score)
scoreboard.encode('utf-8')
font = pygame.font.Font(None, 50)

while running:
	pygame.display.update()  # 画面を更新
	screen.fill(BLACK)       # 画面を塗りつぶす
	text = font.render(scoreboard, True, (255, 255, 255))
	screen.blit(text, (0, 0))

	for event in pygame.event.get():  # イベント
		if event.type == pygame.QUIT: running = False  # 終了

	# 下壁に当たった場合
	if(ball_y >= 470):
		pygame.mixer.music.load("8bit失敗2.mp3")  # 効果音読み込み
		pygame.mixer.music.play(1)            # 効果音再生
		pygame.time.wait(1000)
		pygame.quit()
	# 上壁に当たった場合
	if(ball_y <=  10): ball_dy =  5
	# 右壁に当たった場合
	if(ball_x >= 690): ball_dx = -5
	# 左壁に当たった場合
	if(ball_x <=  10): ball_dx =  5
	# パドルに当たった場合
	if(((paddle_x - 10) <= ball_x <= (paddle_x + 110)) and ball_y == 410 and ball_dy == 5):
		ball_dy = -5
		pygame.mixer.music.load("sound.mp3")  # 効果音読み込み
		pygame.mixer.music.play(1)            # 効果音再生
		score += 1
		scoreboard = "score: " + str(score)
		scoreboard.encode('utf-8')

	# ボール位置を更新
	ball_x += ball_dx
	ball_y += ball_dy

	# ボールを描画
	pygame.draw.circle(screen, WHITE, (ball_x, ball_y), 10)

	# キー操作（左右矢印）でバトルを移動
	press = pygame.key.get_pressed()
	if(press[pygame.K_LEFT]  and paddle_x >   0): paddle_x -= 5
	if(press[pygame.K_RIGHT] and paddle_x < 600): paddle_x += 5

	# パドルを描画
	rect = pygame.Rect(paddle_x, 420, 100, 20)  # Rect(左座標, 上座標, 幅, 高さ)
	pygame.draw.rect(screen, BLUE, rect)

	pygame.display.flip()  # 画面を更新（※ flip：入れ替え）
	clock.tick(60)         # 描画処理の間隔調整（60 FPS）

pygame.quit()
