# テトリス風ブロック落下ゲーム
# https://note.com/ayase_tukihi/n/nad84241d6e08
# https://note.com/ayase_tukihi/n/n0e31d366dd71
#
#【操作方法】
#　　方向： 左キー「←」，右キー「→」，下キー「↓」，
#　　回転：「スペースキー」
#

import tkinter as tk
from queue import Queue  # キュー：押されたキーを管理
import numpy as np
from random import randint
from time import time

GAME_W, GAME_H	=	 10, 18   # 10ブロック×18ブロック
SCN_W, SCN_H		= 400, 720  # 420px×720px
BLOCK_W, BLOCK_H = SCN_W // GAME_W, SCN_H // GAME_H  # １ブロック：40px×40px
TIMER_WAIT = 50  # 50msec，即ち，20fps
g_pos = {'x': 0, 'y': 0}  # 操作中ブロックパターンの座標
g_events = Queue()  # 押されたキーを格納・管理するためのキュー

# ある時からの経過秒数(ミリ秒)を整数化
get_time = lambda: time() * 1000

# ブロック単位の座標が画面の外に出ているかを調べる。
out_of_screen = lambda x, y: x < 0 or x >= GAME_W or y < 0 or y >= GAME_H

# ゲームを初期化
def init_game():
	global g_buf, g_pat, g_time, g_scene
	# g_buf：配置済みブロックを管理する 10×18 の配列(リスト)，全て「0」
	g_buf = [[0 for _ in range(GAME_W)] for _ in range(GAME_H)]
	# g_pat：操作中ブロックパターンを表す配列(リスト)，
	# g_time：前回ブロックパターンを落下させたときの時間
	# g_scene：ゲーム内の状況を示すフラグ，「0」プレイ中，「1」ゲームオーバー
	g_pat, g_time, g_scene = None, get_time(), 0 # g_scene = 0: Playing, 1: Game Over

# ブロックパターンの作成（６種類）
def create_pattern():
	pats = [
		['0100', '0100', '0100', '0100'],  # Ｉ型
		['0000', '0100', '0110', '0100'],  # Ｔ型
		['0000', '0110', '0100', '0100'],  # Ｊ型
		['0000', '0110', '0010', '0010'],  # Ｌ型
		['0000', '0010', '0110', '0100'],  # Ｚ型
		['0000', '0100', '0110', '0010']]  # Ｓ型
	p = pats[randint(0, 5)]
	p = list(map(lambda x: [int(v) for v in x], p))  # 0と1がカンマ区切りのリストを作成
	for _ in range(randint(1, 4)):
		ndarray = np.array(p, int)
		# 数回（回数はランダム）パターンを回転（即ち，90度，180度，270度，360度）
		p = np.rot90(ndarray).tolist()
	return p

# patにブロックパターンを受け取り，その左上座標を x, y に受け取る。
# そして，配置済みブロックと操作中ブロックパターンの衝突判定を行う。
def is_crashed(pat, x, y):
	for i in range(4):
		for j in range(4):
			if pat[i][j]:
				# 座標(x, y)が，画面外でないか，操作中ブロックパターンの１ブロックと配置済みのブロックが衝突していないかを調べる。
				if out_of_screen(j + x, i + y) or pat[i][j] & g_buf[i + y][j + x]:
					return True
	return False

# １つのブロックを tkinter の Canvas に描画
def draw_one_block(canvas, x, y):
	if not out_of_screen(x, y):
		x1, y1 = x * BLOCK_W, y * BLOCK_H
		x2, y2 = x1 + BLOCK_W - 1, y1 + BLOCK_H - 1
		canvas.create_rectangle(x1, y1, x2, y2, fill='white', width=0, tag='objects')

# 配置済みのブロックと操作中のブロックパターンを描画
def draw_game(canvas):
	canvas.delete('objects')

	for i in range(GAME_W):
		for j in range(GAME_H):
			if g_buf[j][i]:
				draw_one_block(canvas, i, j)

	if g_pat:
		for i in range(4):
			for j in range(4):
				if g_pat[i][j]:
					draw_one_block(canvas, j + g_pos['x'], i + g_pos['y'])

	if g_scene == 1:
		canvas.create_rectangle(40, SCN_H // 2 - 50, SCN_W - 40, SCN_H // 2 + 50, 
			fill='gray', tag='objects')
		canvas.create_text(SCN_W // 2, SCN_H // 2, text='Game Over\n\nPlease Space Key', 
			font=('Monospace', 14, 'bold'), justify='center', fill='white', anchor='center', tag='objects')

# 押されたキーを g_events（キュー）に詰める。
def key_events(e):
	if e.keysym in ('Left', 'Right', 'Down', 'space'):
		g_events.put(e.keysym)

# メインループ（タイマーで繰り返し呼び出されるコールバック関数）。
def main_proc(root, canvas):
	global g_buf, g_pat, g_time, g_scene

	# 押されたキーを g_events（キュー）から取り出し，それに対する処理を行う。
	# main_proc() が１回呼ばれると，１つのキー操作を処理。
	if (e := g_events.get() if not g_events.empty() else None) is not None:
		if g_scene == 0 and g_pat is not None:
			# 左右方向キーを処理し，移動できる状態であれば，ブロックパターンの座標を上書き。
			if   e == 'Left' :  g_pos['x'] += -1 if not is_crashed(g_pat, g_pos['x'] - 1, g_pos['y']) else 0
			elif e == 'Right':  g_pos['x'] += 1  if not is_crashed(g_pat, g_pos['x'] + 1, g_pos['y']) else 0
			# Spaceキーによる回転。
			elif e == 'space':  g_pat = pat if not is_crashed(pat := np.rot90(np.array(g_pat, int)).tolist(), **g_pos) else g_pat
		# ゲームオーバーのときのSpaceキーの処理，Spaceキーが押されるとゲームを初期化。
		elif g_scene == 1 and e == 'space':
			init_game()

	if g_scene == 0:
		# 操作しているブロックパターンは，地面か他のブロックの上に降り立つと，g_bufに情報が移動。
		# g_buf に移動したとき，操作中のブロックパターンが入っている g_pat は None でクリア。
		# g_pat がNoneであったら，新たに操作するブロックパターンを生成。
		if g_pat is None:
			g_pat = create_pattern()
			for top in range(4):
				if any(g_pat[top]):
					g_pos['x'], g_pos['y'] = (GAME_W - 4) // 2, -top
					break
			# 新たに操作するブロックパターンを生成したとき，配置済みブロックと衝突した場合はゲームオーバー。
			# （g_scene に １をセット）。
			g_scene = 1 if is_crashed(g_pat, **g_pos) else 0

		# get_time()（現在の時間）と前回落下処理をした時間を比較し，400ミリ秒以上経過したら処理をする。
		if get_time() - g_time > 400 or e == 'Down':
			# １つ落下した場合，配置済みブロックと衝突していないかを調べる。
			# 衝突する場合，ブロックパターンの操作は終了し，g_pat の内容を g_buf に移動。
			if is_crashed(g_pat, g_pos['x'], g_pos['y'] + 1):
				for y in range(4):
					for x in range(4):
						if not out_of_screen(g_pos['x'] + x, g_pos['y'] + y):
							# 一番上まで積み上がったとき，配置済みブロックを g_pat の０で上書きさせないためにビットOR（｜）を使用。
							g_buf[g_pos['y'] + y][g_pos['x'] + x] |= g_pat[y][x]
				# g_pat は g_buf に移動済みなのでNoneでクリア。
				g_pat = None
				# １行すべてに配置済みブロックがあるかを調べ，その場合は行を除外。
				new_buf = list(filter(lambda line: not all(line), g_buf))
				g_buf = [[0 for _ in range(GAME_W)] for _ in range(GAME_H - len(new_buf))] + new_buf
			# 衝突していないことが分かれば座標を１つ下へ進める。
			else:
				g_pos['y'] += 1

			# 前回落下処理を行った時間を更新。
			g_time = get_time()

	# main_proc()の呼び出しで更新された情報を画面に反映。
	draw_game(canvas)
	# main_proc()が今から何ミリ秒後に呼び出されるかを設定。
	root.after(TIMER_WAIT, main_proc, root, canvas)

# コードを実行すると __name__ というグローバル変数は '__main__' になる。
# モジュールとして使用した場合は何もしない。
if __name__ == '__main__':
	# tkinterのウインドウを生成。
	root = tk.Tk()
	root.title('テトリス風')
	root.geometry(f'{SCN_W}x{SCN_H}')
	# Canvasを生成し，ウインドウに配置。
	canvas = tk.Canvas(root, width=SCN_W, height=SCN_H, bg='black')
	canvas.place(x=0, y=0)
	# キーが押された場合，bind()を使用して key_events を処理。
	root.bind('<Key>', key_events)
	# ゲームを初期化。
	init_game()
	# main_proc() を指定時間後に呼び出す。
	root.after(TIMER_WAIT, main_proc, root, canvas)
	# tkinterがウインドウを制御するためのメインループ。
	root.mainloop()
