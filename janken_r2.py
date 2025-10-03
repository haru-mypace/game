# じゃんけんゲーム
import random
import tkinter as tk

root = tk.Tk()
root.title('最初の画面')
root.geometry('600x500')

label0 = tk.Label(text = "ジャンケンをします。")
label1 = tk.Label(text = "グーチョキパーのどれかを選択してください。")
label0.pack()
label1.pack()

win = "結果：あなたの勝ちです。"
drow = "結果：あいこです。"
lose = "結果：あなたの負けです。"

def gu():
	player = 0
	var0.set("プレイヤー：グー")
	canvas.delete("all")
	canvas.create_image(150,150, image = img0)
	# コンピューターの手を決定
	com = random.randint(0, 2)
	if com == 0:
		var1.set("コンピュータ：グー")
		canvas.create_image(450,150, image = img0)
	elif com == 1:
		var1.set("コンピュータ：チョキ")
		canvas.create_image(450,150, image = img1)
	else:
		var1.set("コンピュータ：パー")
		canvas.create_image(450,150, image = img2)
	# じゃんけんの勝敗を判定する
	j = (player - com + 3) % 3
	if j == 0:
		var2.set(drow)
	elif j == 1:
		var2.set(lose)
	else:
		var2.set(win)

def tyoki():
	player = 1
	var0.set("プレイヤー：チョキ")
	canvas.delete("all")
	canvas.create_image(150,150, image = img1)
	# コンピューターの手を決定
	com = random.randint(0, 2)
	if com == 0:
		var1.set("コンピュータ：グー")
		canvas.create_image(450,150, image = img0)
	elif com == 1:
		var1.set("コンピュータ：チョキ")
		canvas.create_image(450,150, image = img1)
	else:
		var1.set("コンピュータ：パー")
		canvas.create_image(450,150, image = img2)
	# じゃんけんの勝敗を判定する
	j = (player - com + 3) % 3
	if j == 0:
		var2.set(drow)
	elif j == 1:
		var2.set(lose)
	else:
		var2.set(win)

def pa():
	player = 2
	var0.set("プレイヤー：パー")
	canvas.delete("all")
	canvas.create_image(150,150, image = img2)
	# コンピューターの手を決定
	com = random.randint(0, 2)
	if com == 0:
		var1.set("コンピュータ：グー")
		canvas.create_image(450,150, image = img0)
	elif com == 1:
		var1.set("コンピュータ：チョキ")
		canvas.create_image(450,150, image = img1)
	else:
		var1.set("コンピュータ：パー")
		canvas.create_image(450,150, image = img2)
	# じゃんけんの勝敗を判定する
	j = (player - com + 3) % 3
	if j == 0:
		var2.set(drow)
	elif j == 1:
		var2.set(lose)
	else:
		var2.set(win)

button0 = tk.Button(text = "グー", command = gu)
button1 = tk.Button(text = "チョキ", command = tyoki)
button2 = tk.Button(text = "パー", command = pa)
button0.pack()
button1.pack()
button2.pack()

var0 = tk.StringVar(root)
var1 = tk.StringVar(root)
var2 = tk.StringVar(root)
var0.set("")
var1.set("")
var2.set("")
label2 = tk.Label(textvariable = var0)
label3 = tk.Label(textvariable = var1)
label4 = tk.Label(textvariable = var2)
label2.pack()
label3.pack()
label4.pack()

canvas = tk.Canvas(width = 600, height = 300)
canvas.pack(side = tk.BOTTOM)
img0 = tk.PhotoImage(file = "goo.png", width = 250, heigh = 250)
img1 = tk.PhotoImage(file = "choki.png", width = 190, heigh = 260)
img2 = tk.PhotoImage(file = "par.png", width = 270, heigh = 260)

label5 = tk.Label(text = "プレイヤー")
label6 = tk.Label(text = "コンピュータ")
label5.place(x = 130, y = 480)
label6.place(x = 430, y = 480)

root.mainloop()
