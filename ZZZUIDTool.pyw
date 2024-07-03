# 程序名称：ZZZUIDTool
# 作者：MOPELotus

import os
import sys
import ctypes
import pyautogui
import time
import keyboard
from tkinter import Tk, Label, StringVar
from queue import Queue
from threading import Thread

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # 默认点击位置
    x, y = 700, 650

    # 初始化点击状态和运行状态为False
    clicking = False
    running = True

    # 创建一个Tk窗口
    root = Tk()
    root.geometry("+0+0")  # 将窗口放在屏幕左上角
    root.overrideredirect(1)  # 移除窗口边框
    root.attributes('-topmost', 1)  # 确保窗口始终在最顶层

    # 创建四个StringVar来存储显示的文本
    text1 = StringVar()
    text1.set("连点已关闭")
    text2 = StringVar()
    text2.set("荷花制作")
    text3 = StringVar()
    text3.set("F8切换点击 Esc结束程序")
    text4 = StringVar()
    text4.set("将鼠标置于取消按钮后按下F1自定义坐标")

    # 在窗口上创建四个Label来显示文本
    label1 = Label(root, textvariable=text1)
    label1.pack()
    label2 = Label(root, textvariable=text2)
    label2.pack()
    label3 = Label(root, textvariable=text3)
    label3.pack()
    label4 = Label(root, textvariable=text4)
    label4.pack()

    # 创建一个队列来处理GUI更新
    queue = Queue()

    # 定义一个函数来切换点击状态
    def toggle_clicking(e):
        global clicking
        clicking = not clicking
        queue.put(('clicking', clicking))

    # 当F8键被按下时，切换点击状态
    keyboard.on_press_key("f8", toggle_clicking)

    # 当F1键被按下时，获取当前鼠标位置作为点击坐标
    keyboard.on_press_key("f1", lambda e: queue.put(('set_coords', pyautogui.position())))

    # 当Esc键被按下时，结束程序
    keyboard.on_press_key("esc", lambda e: queue.put(('exit', True)))

    # 每6.5秒点击两次，两次点击间隔为0.5秒
    def click_loop():
        global running
        while running:
            if clicking:
                pyautogui.click(x, y, clicks=2, interval=0.5)
            time.sleep(6.5)

    # 在一个新的线程中运行点击循环
    Thread(target=click_loop).start()

    # 在主线程中处理GUI更新
    while True:
        root.update()  # 更新Tk窗口
        while not queue.empty():
            command, value = queue.get()
            if command == 'clicking':
                if value:
                    text1.set("连点已启动")
                else:
                    text1.set("连点已关闭")
            elif command == 'set_coords':
                x, y = value
                text4.set(f"自定义坐标已设置为 ({x}, {y})")
            elif command == 'exit':
                running = False
                if root.winfo_exists():  # 检查Tk窗口是否存在
                    root.destroy()
                os._exit(0)  # 立即结束整个程序
else:
    # 如果不是管理员，那么重新启动脚本并请求管理员权限
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
