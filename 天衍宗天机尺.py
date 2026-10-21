# -*- coding: utf-8 -*-
import ctypes
# 解决Windows高分屏模糊问题
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

import random
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# 八卦
BAGUA = {
    '111': '乾', '110': '兑', '101': '离', '100': '震',
    '011': '巽', '010': '坎', '001': '艮', '000': '坤',
}

# 六十四卦
GUA_NAMES = {
    ('乾','乾'): '乾为天', ('兑','乾'): '天泽履', ('离','乾'): '天火同人', ('震','乾'): '天雷无妄',
    ('巽','乾'): '天风姤', ('坎','乾'): '天水讼', ('艮','乾'): '天山遁', ('坤','乾'): '天地否',
    ('乾','兑'): '泽天夬', ('兑','兑'): '兑为泽', ('离','兑'): '泽火革', ('震','兑'): '泽雷随',
    ('巽','兑'): '泽风大过', ('坎','兑'): '泽水困', ('艮','兑'): '泽山咸', ('坤','兑'): '泽地萃',
    ('乾','离'): '火天大有', ('兑','离'): '火泽睽', ('离','离'): '离为火', ('震','离'): '火雷噬嗑',
    ('巽','离'): '火风鼎', ('坎','离'): '火水未济', ('艮','离'): '火山旅', ('坤','离'): '火地晋',
    ('乾','震'): '雷天大壮', ('兑','震'): '雷泽归妹', ('离','震'): '雷火丰', ('震','震'): '震为雷',
    ('巽','震'): '雷风恒', ('坎','震'): '雷水解', ('艮','震'): '雷山小过', ('坤','震'): '雷地豫',
    ('乾','巽'): '风天小畜', ('兑','巽'): '风泽中孚', ('离','巽'): '风火家人', ('震','巽'): '风雷益',
    ('巽','巽'): '巽为风', ('坎','巽'): '风水涣', ('艮','巽'): '风山渐', ('坤','巽'): '风地观',
    ('乾','坎'): '水天需', ('兑','坎'): '水泽节', ('离','坎'): '水火既济', ('震','坎'): '水雷屯',
    ('巽','坎'): '水风井', ('坎','坎'): '坎为水', ('艮','坎'): '水山蹇', ('坤','坎'): '水地比',
    ('乾','艮'): '山天大畜', ('兑','艮'): '山泽损', ('离','艮'): '山火贲', ('震','艮'): '山雷颐',
    ('巽','艮'): '山风蛊', ('坎','艮'): '山水蒙', ('艮','艮'): '艮为山', ('坤','艮'): '山地剥',
    ('乾','坤'): '地天泰', ('兑','坤'): '地泽临', ('离','坤'): '地火明夷', ('震','坤'): '地雷复',
    ('巽','坤'): '地风升', ('坎','坤'): '地水师', ('艮','坤'): '地山谦', ('坤','坤'): '坤为地',
}

def da_yan_yao():
    remain = 49
    for _ in range(3):
        left = random.randint(1, remain - 1)
        right = remain - left
        right_after = right - 1
        left_mod = left % 4 or 4
        right_mod = right_after % 4 or 4
        gui_qi = 1 + left_mod + right_mod
        remain -= gui_qi
    return remain // 4

def bin_to_gua_name(yao_bin):
    xia, shang = yao_bin[0:3], yao_bin[3:6]
    xia_name, shang_name = BAGUA[xia], BAGUA[shang]
    return xia_name, shang_name, GUA_NAMES.get((xia_name, shang_name), '未知卦')

def center_window(w, h):
    """动态调整窗口大小并居中"""
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (w // 2)
    y = (window.winfo_screenheight() // 2) - (h // 2)
    window.geometry(f'{w}x{h}+{x}+{y}')

def start_divination():
    question = entry_question.get("1.0", tk.END).strip()
    if not question:
        question = "（未填写问题）"

    yaos = [da_yan_yao() for _ in range(6)]
    yao_names = {6: '老阴（变阳）', 7: '少阳', 8: '少阴', 9: '老阳（变阴）'}
    ben_bin = ''.join('1' if n in (7, 9) else '0' for n in yaos)
    bian_bin = ''.join('1' if n in (6, 7) else '0' for n in yaos)
    bian_yao_positions = [i + 1 for i, n in enumerate(yaos) if n in (6, 9)]

    xia_ben, shang_ben, ben_gua = bin_to_gua_name(ben_bin)
    xia_bian, shang_bian, bian_gua = bin_to_gua_name(bian_bin)

    output_lines = []
    output_lines.append("=" * 30)
    output_lines.append(f"问题：{question}")
    output_lines.append(f"起卦时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append("起卦方式：大衍筮法（电脑模拟）")
    output_lines.append("-" * 30)
    output_lines.append(f"六爻数字（从下往上）：{','.join(str(n) for n in yaos)}")
    output_lines.append(f"各爻：{' | '.join(f'{i+1}爻:{n}{yao_names[n]}' for i, n in enumerate(yaos))}")
    output_lines.append("-" * 30)
    output_lines.append(f"本卦：下{xia_ben} 上{shang_ben} -> {ben_gua}")
    output_lines.append("本卦阴阳（从下往上）：" + ' '.join('阳' if b == '1' else '阴' for b in ben_bin))

    if bian_yao_positions:
        output_lines.append(f"变爻：{'、'.join(f'第{p}爻' for p in bian_yao_positions)}")
        output_lines.append(f"变卦：下{xia_bian} 上{shang_bian} -> {bian_gua}")
        output_lines.append("变卦阴阳（从下往上）：" + ' '.join('阳' if b == '1' else '阴' for b in bian_bin))
    else:
        output_lines.append("变爻：无")
        output_lines.append("变卦：无（以本卦断）")

    output_lines.append("=" * 30)
    result_text = "\n".join(output_lines)

    text_result.config(state="normal")
    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, result_text)
    text_result.config(state="disabled")

    window.clipboard_clear()
    window.clipboard_append(result_text)
    window.update()

    # 你的专属 DeepSeek 路径
    shortcut_path = r"C:\Users\reze5\Desktop\DeepSeek.lnk"
    try:
        os.startfile(shortcut_path)
    except:
        pass

    frame_input.pack_forget()
    btn_start.pack_forget()
    
    center_window(800, 600)
    
    frame_result.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
    btn_reset.pack(side=tk.BOTTOM, pady=15)

def reset_ui():
    frame_result.pack_forget()
    btn_reset.pack_forget()
    
    center_window(800, 300)
    
    frame_input.pack(pady=5)
    btn_start.pack(pady=15)
    
    entry_question.delete("1.0", tk.END)
    text_result.config(state="normal")
    text_result.delete("1.0", tk.END)
    text_result.config(state="disabled")

def on_enter(event):
    start_divination()
    return "break"

def on_ctrl_enter(event):
    entry_question.insert(tk.INSERT, "\n")
    return "break"

window = tk.Tk()
window.title("龙问偷的天衍宗千机尺")

style = ttk.Style()
try:
    style.theme_use('vista')
except:
    pass

ttk.Label(window, text="随便用，反正是天衍的", font=("微软雅黑", 11)).pack(pady=15)

global frame_input, entry_question, btn_start, frame_result, text_result, btn_reset

frame_input = ttk.Frame(window)
frame_input.pack(pady=5)

entry_question = tk.Text(frame_input, width=50, height=4, font=("微软雅黑", 11))
entry_question.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_input = ttk.Scrollbar(frame_input, command=entry_question.yview)
scrollbar_input.pack(side=tk.RIGHT, fill=tk.Y)
entry_question.config(yscrollcommand=scrollbar_input.set)

entry_question.bind("<Return>", on_enter)
entry_question.bind("<Control-Return>", on_ctrl_enter)

btn_start = ttk.Button(window, text="摇一卦", command=start_divination)
btn_start.pack(pady=15)

frame_result = ttk.Frame(window)

scrollbar = ttk.Scrollbar(frame_result)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_result = tk.Text(frame_result, wrap=tk.WORD, font=("微软雅黑", 10), yscrollcommand=scrollbar.set, relief="flat", bg="#F9F9F9", state="disabled")
text_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=text_result.yview)

btn_reset = ttk.Button(window, text="再来一卦", command=reset_ui)

center_window(800, 300)
window.bind("<Escape>", lambda event: reset_ui())

window.mainloop()