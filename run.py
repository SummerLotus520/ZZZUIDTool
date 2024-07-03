import pytesseract
from PIL import ImageGrab
import pyautogui
import pygetwindow as gw

def click_center(window):
    # 计算窗口中心点坐标
    center_x = window.left + window.width / 2
    center_y = window.top + window.height / 2

    # 点击窗口中心点
    pyautogui.click(center_x, center_y)

def click_on_text(text, window):
    # 截取指定窗口的快照
    screenshot = ImageGrab.grab(window.box)

    # 使用pytesseract识别文字
    d = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT, lang='chi_sim')

    # 遍历所有识别到的文字，如果找到匹配的文字，就点击它
    for i in range(len(d['text'])):
        if d['text'][i] == text:
            x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
            pyautogui.click(window.left + x + w / 2, window.top + y + h / 2)
            break

# 找到名为"绝区零"的窗口
window = gw.getWindowsWithTitle('绝区零')[0]

# 循环点击窗口中心
while True:
    click_center(window)

    # 如果出现“取消”按钮，则点击
    if '取消' in pytesseract.image_to_string(ImageGrab.grab(window.box), lang='chi_sim'):
        click_on_text('取消', window)
