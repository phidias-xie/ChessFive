#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:39:03 2020

@author: phidias.xie
@Email: phidiasxie@gmail.com
@History
1.0.0  第一版发布，可以正常对弈，判定胜负，无禁手规则
"""
VERSION='1.0.0'


import logging
#logging.basicConfig(level=logging.INFO)

import tkinter as tk
import tkinter.messagebox as msgbox



#定义棋盘大小
OFFSET=40
WIDTH=OFFSET*16
HEIGHT=OFFSET*16
RADIUS=15


#创建窗口
win = tk.Tk()
win.geometry('%dx%d' %(WIDTH,HEIGHT))
win.title('ChessFive')


#绘制棋盘背景
bg = tk.Canvas(win, bg='orange', width = WIDTH, height = HEIGHT)
bg.create_rectangle(OFFSET-1, OFFSET-1, OFFSET*15+1, OFFSET*15+1, width=3)
for x in range(OFFSET*2, OFFSET*15, OFFSET):
    bg.create_line(x, OFFSET, x, OFFSET*15)
    bg.create_line(OFFSET, x, OFFSET*15, x)
#for x in range(OFFSET, OFFSET*16, OFFSET):
#    bg.create_text(x, OFFSET/2, text=str(int(x/OFFSET)))
#    bg.create_text(OFFSET/2, x, text=str(int(x/OFFSET)))
bg.create_oval(OFFSET*4-2,  OFFSET*4-2,  OFFSET*4+2,  OFFSET*4+2,  fill='black')    
bg.create_oval(OFFSET*12-2, OFFSET*4-2,  OFFSET*12+2, OFFSET*4+2,  fill='black')    
bg.create_oval(OFFSET*4-2,  OFFSET*12-2, OFFSET*4+2,  OFFSET*12+2, fill='black')    
bg.create_oval(OFFSET*12-2, OFFSET*12-2, OFFSET*12+2, OFFSET*12+2, fill='black')    
bg.create_oval(OFFSET*8-2,  OFFSET*8-2,  OFFSET*8+2,  OFFSET*8+2,  fill='black')    
bg.pack()


#定义玩家
player = 1


#定义棋子类
class newchess(object):
    def __init__(self):
        self.st = 0  #棋子的状态 0：无棋子 1：黑棋 2：白棋
        self.img = None  #保存棋子的图形对象，以便于开新局的时候删除
        

#创建全部的棋子
chess = [[newchess() for n in range(0,15)] for n in range(0, 15)]


#判断是否存在五子连线
def ChessisFive(x, y):
    #横向判断
    num1 = 0
    for n in range(0, x+1):
        if chess[y][x-n].st == player: 
            num1 += 1
        else:
            break
    for n in range(x+1, 15):
        if chess[y][n].st == player: 
            num1 += 1
        else:
            break
    
    #纵向判断
    num2 = 0
    for n in range(0, y+1):
        if chess[y-n][x].st == player: 
            num2 += 1
        else:
            break
    for n in range(y+1, 15):
        if chess[n][x].st == player: 
            num2 += 1
        else:
            break
    
    #\判断
    num3 = 0
    x1, y1 = 0, 0
    for n in range(0, 15):
        x1, y1 = x-n, y-n
        if x1<0 or y1<0:
            break
        if chess[y1][x1].st == player: 
            num3 += 1
        else:
            break
    for n in range(0, 15):
        x1, y1 = x+1+n, y+1+n
        if x1>14 or y1>14:
            break
        if chess[y1][x1].st == player: 
            num3 += 1
        else:
            break
        
    #/判断
    num4 = 0
    for n in range(0, 15):
        x1, y1 = x-n, y+n
        if x1<0 or y1>14:
            break
        if chess[y1][x1].st == player: 
            num4 += 1
        else:
            break
    for n in range(0, 15):
        x1, y1 = x+1+n, y-1-n
        if x1>14 or y1<0:
            break
        if chess[y1][x1].st == player: 
            num4 += 1
        else:
            break
        
    logging.info('chess[%d,%d][-%d, |%d, \\%d, /%d]' %(x+1, y+1, num1, num2, num3, num4))
    if player==1:
        pass #可以添加黑棋禁手规则
        
    return num1>=5 or num2>=5 or num3>=5 or num4>=5
        
    
#处理用户鼠标点击，判断是否落棋，以及胜负
def LKeyClick(event):
    global player
    x1, x2 = int(event.x/OFFSET), event.x%OFFSET
    y1, y2 = int(event.y/OFFSET), event.y%OFFSET
    if x2 in range(RADIUS,OFFSET-RADIUS) or y2 in range(RADIUS,OFFSET-RADIUS):
        return
    if x2<RADIUS:
        x1 -= 1
    if y2<RADIUS:
        y1 -= 1
    
    if x1>=0 and y1>=0:
        if chess[y1][x1].st==0:
            chess[y1][x1].st = player
            chess[y1][x1].img = bg.create_oval((x1+1)*OFFSET-RADIUS, (y1+1)*OFFSET-RADIUS, (x1+1)*OFFSET+RADIUS, (y1+1)*OFFSET+RADIUS, fill='black' if player==1 else 'white')
            if ChessisFive(x1, y1):
                msgbox.showinfo('Game Over!', 'Black is Winner!' if player==1 else 'White is Winner')
                NewGame()
            else:
                if player==1:
                    player = 2
                else:
                    player = 1

def NewGame():
    global player
    for i in range(0, 15):
        for j in range(0, 15):
            chess[i][j].st = 0
            bg.delete(chess[i][j].img)
            chess[i][j].img = None
    player = 1
        

#绑定鼠标点击事件，开始主循环
bg.bind("<Button-1>", LKeyClick)
win.mainloop()

