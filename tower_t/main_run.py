import os
import tkinter as tk
import webbrowser
from tkinter import messagebox

from PIL import Image, ImageTk

from tower_t.tower_extract import get_tower_img_from_url, get_random_tower


def download_tower_images():
    try:
        get_tower_img_from_url('https://www.shenpowang.com/taluopai/jieshi/', mp_run=True)
        messagebox.showinfo("下载完成", "塔罗牌图片已下载完成！")
    except Exception as e:
        messagebox.showerror("下载失败", f"下载过程中出现错误：{e}")


def draw_tower_cards():
    try:
        num = int(entry_num.get())
        if num <= 0:
            messagebox.showerror("输入错误", "请输入一个正整数！")
            return

        results = get_random_tower(num, './tower_img', prob_0=0.65)
        display_cards(results)
    except Exception as e:
        messagebox.showerror("错误", f"抽取过程中出现错误：{e}")


def clear_results():
    for widget in results_frame.winfo_children():
        widget.destroy()
    messagebox.showinfo("清空完成", "已清空所有输出！")


def display_cards(results):
    for widget in results_frame.winfo_children():
        widget.destroy()

    row_frame = None
    for idx, (name, reverse) in enumerate(results):
        if idx % NUM_CARDS_PER_ROW == 0:
            row_frame = tk.Frame(results_frame)
            row_frame.pack(side=tk.TOP, padx=10, pady=10)

        img_path = os.path.join('./tower_img', f'{name}.gif')
        image = Image.open(img_path)

        # 如果是逆位，旋转180度
        if reverse:
            image = image.rotate(180, expand=True)

        photo = ImageTk.PhotoImage(image)

        card_frame = tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, borderwidth=2, relief=tk.GROOVE)
        card_frame.pack(side=tk.LEFT, padx=10, pady=10)
        card_frame.pack_propagate(False)

        label_image = tk.Label(card_frame, image=photo)
        label_image.image = photo
        label_image.pack()

        label_name = tk.Label(card_frame, text=name, font=FONT, wraplength=CARD_WIDTH)
        label_name.pack()

        label_status = tk.Label(card_frame, text=f"{'逆位🔮' if reverse else '正位✨'}",
                                fg='red' if reverse else 'green', font=FONT)
        label_status.pack()


def open_url():
    webbrowser.open('https://www.shenpowang.com/taluopai/jieshi/')


if __name__ == '__main__':
    FONT = ('Arial', 10)
    CARD_WIDTH = 150
    CARD_HEIGHT = 230
    NUM_CARDS_PER_ROW = 3
    root = tk.Tk()
    root.title("塔罗牌占卜")

    frame_controls = tk.Frame(root)
    frame_controls.pack(pady=10)

    btn_download = tk.Button(frame_controls, text="🔄 下载塔罗牌", command=download_tower_images, font=FONT)
    btn_download.pack(side=tk.LEFT, padx=10)

    btn_draw = tk.Button(frame_controls, text="🃏 抽取塔罗牌", command=draw_tower_cards, font=FONT)
    btn_draw.pack(side=tk.LEFT, padx=10)

    entry_num = tk.Entry(frame_controls, width=5, font=FONT)
    entry_num.insert(0, '3')
    entry_num.pack(side=tk.LEFT)

    label_num = tk.Label(frame_controls, text="张", font=FONT)
    label_num.pack(side=tk.LEFT, padx=5)

    btn_clear = tk.Button(frame_controls, text="☀️ 清空", command=clear_results, font=FONT)
    btn_clear.pack(side=tk.LEFT, padx=10)

    btn_open_url = tk.Button(frame_controls, text="🔗 打开塔罗牌网站", command=open_url, font=FONT)
    btn_open_url.pack(side=tk.LEFT, padx=10)

    results_frame = tk.Frame(root)
    results_frame.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
