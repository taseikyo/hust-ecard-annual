#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-23 15:41:06
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8

import calendar
import csv
import glob
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.font_manager import FontProperties

myfont = FontProperties(fname="SourceHanSansCN-Light.otf")

sns.set(
    style="ticks",
    font=myfont.get_name(),
    rc={
        "figure.figsize": [16, 9],
        "text.color": "white",
        "axes.labelcolor": "white",
        "axes.edgecolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "axes.facecolor": "#443941",
        "figure.facecolor": "#443941",
    },
)

# 不全，需要手动添加
HALLS = {
    "东一",
    "集贤楼",
    "自助售货机",
    "西一",
    "百品屋",
    "集锦园",
    "校园网",
    "图书馆",
    "东学超市",
    "东三",
    "紫荆园",
    "百景",
    "喻园",
}


def merge_all_files(year=2019):
    """
    汇总所有月份的 csv
    """
    files = glob.glob("csv/*.csv")
    df = pd.concat([pd.read_csv(file) for file in files])
    df.to_csv(f"csv/{year}.csv", index=False, encoding="utf-8-sig")


def draw_consume_times(year=2019):
    """
    按月份显示消费次数
    """
    times = {}
    for x in range(1, 13):
        with open(f"csv/{year}-{x}.csv", encoding="utf-8") as f:
            lines = f.readlines()
        times[x] = len(lines) - 1
    print(times)
    plt.figure(figsize=(16, 6))
    plt.plot(list(times.keys()), list(times.values()), label="消费次数", color="white")
    plt.legend()
    # 图上画出数据
    x = range(1, len(times) + 1)
    y_text = list(times.values())
    for i in range(len(times)):
        plt.text(x[i], y_text[i] + 2, y_text[i], ha="center", fontsize=12)

    plt.grid(False)
    plt.xlabel("月份", fontsize=16)
    plt.ylabel("次数", fontsize=16)
    plt.xticks(range(14), [""] + calendar.month_name[1:13] + [""])
    plt.title("每月的消费次数", fontsize=20)
    plt.show()


def get_all_windows_halls(year=2019):
    """
    食堂窗口 & 食堂
    """
    halls = defaultdict(int)
    windows = defaultdict(int)
    for x in range(1, 13):
        with open(f"csv/{year}-{x}.csv", encoding="utf-8") as f:
            next(f)
            reader = csv.reader(f)
            for row in reader:
                windows[row[-1]] += 1
                has_found = False
                for hall in HALLS:
                    if row[-1].find(hall) >= 0:
                        has_found = True
                        halls[hall] += 1
                        break
                if not has_found:
                    halls[row[-1]] += 1
    print(halls)
    with open("csv/halls.csv", "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["e_hall", "e_count"])
        writer.writerows(halls.items())
    with open("csv/windows.csv", "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["e_windows", "e_count"])
        writer.writerows(windows.items())


def draw_bars(path, title, colname, rotate=0):
    df = pd.read_csv(path)
    df = df.sort_values("e_count", ascending=False)
    print(df.head(10))
    plt.figure(figsize=(16, 6))
    plt.bar(df[f"{colname}"], df.e_count, label="消费次数", color="white")
    plt.legend()
    # plt.grid(False)
    # 图上画出数据
    x = range(len(df.e_count) + 1)
    y_text = list(df.e_count)
    for i in range(len(df.e_count)):
        plt.text(x[i], y_text[i] + 2, y_text[i], ha="center", fontsize=12)
    plt.xlabel(title, fontsize=16)
    plt.ylabel("次数", fontsize=16)
    plt.xticks(rotation=rotate)
    plt.title(f"{title}的消费次数", fontsize=20)
    plt.tight_layout()
    plt.show()


def draw_hour_times(year=2019):
    hours = defaultdict(int)
    with open(f"csv/{year}.csv", encoding="utf-8") as f:
        next(f)
        for line in f:
            hour = int(line.split(":")[0].split(" ")[1])
            hours[hour] += 1
    print(hours)
    plt.figure(figsize=(16, 6))
    x, y = [], []
    for i, j in sorted(hours.items(), key=lambda x: x[0]):
        x.append(i)
        y.append(j)
    print(x, y)
    plt.plot(x, y, label="消费次数", color="white")
    plt.xlabel("小时", fontsize=16)
    plt.ylabel("次数", fontsize=16)
    plt.title("每时间段的消费次数", fontsize=20)
    plt.xticks(range(x[0], x[-1]+1))
    # 图上画出数据
    for i in range(len(hours)):
        plt.text(x[i]+0.1, y[i] + 2, y[i], ha="center", fontsize=12)
    plt.show()

def max_continue_times(year=2019):
    """
    最大连续次数
    """
    max_time = 0
    cur_time = 1
    max_hall = None
    pre_element = None
    with open(f"csv/{year}.csv", encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            if row[2] == pre_element:
                cur_time += 1
                if max_time < cur_time:
                    max_time = cur_time
                    max_hall = pre_element
            else:
                pre_element = row[2]
                cur_time = 1
    print(f"在 {year}，你连续在 {max_hall} 窗口消费了 {max_time} 次，看来你很喜欢这个窗口！")


def get_total_money_time(year=2019):
    """
    总消费次数、钱数
    """
    df = pd.read_csv(f"csv/{year}.csv")
    print(f"在 {year}，你一共消费了 {len(df)} 次，共花费 {df.e_money.sum()} 元！")


if __name__ == "__main__":
    merge_all_files(2020)
    draw_consume_times(2020)
    get_all_windows_halls(2020)
    draw_bars("csv/halls.csv", "食堂", "e_hall")
    draw_bars("csv/windows.csv", "食堂窗口", "e_windows", 35)
    draw_hour_times(2020)
    max_continue_times(2020)
    get_total_money_time(2020)
