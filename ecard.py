#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-23 14:48:11
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8

"""
retrieve and save my ecard consume detail
"""

import csv
import random
import time

import requests

DETAIL = []


def one_moonth(year=2019, month=12, page=1, total=0):
    global DETAIL
    url = "http://218.199.85.15/pcard/gettrjndataList.action"
    headers = {
        "Cookie": "JSESSIONID={xxx}",
        "Referer": "http://218.199.85.15/pcard/pcard/acchistrjn.action",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    post_data = {
        "page": f"{page}",
        "rp": "10",
        "sortname": "jndatetime",
        "sortorder": "desc",
        "query": "",
        "qtype": "",
        "accquary": "215799",
        "trjnquary": f"{year}-{month:02}",
    }

    print(f"retrieve {year}-{month} page {page} data...")
    r = requests.post(url, headers=headers, data=post_data)
    data = r.json()

    for row in data["rows"]:
        # bank card transfer
        if row["cell"][5] == "0":
            continue
        e_time = row["cell"][0]
        e_money = row["cell"][3][1:]
        e_hall = row["cell"][8].strip()
        temp = [e_time, e_money, e_hall]
        DETAIL.append(temp)

    total += 10
    if total < data["total"]:
        time.sleep(random.randint(1000, 2000) / 1000)
        one_moonth(year, month, page + 1, total)
    else:
        dump_as_csv(year, month)


def dump_as_csv(year, month):
    global DETAIL
    print(f"save {year}-{month} data...")
    with open(f"csv/{year}-{month}.csv", "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["e_time", "e_money", "e_hall"])
        writer.writerows(DETAIL)
    DETAIL = []


if __name__ == "__main__":
    for month in range(1, 13):
        one_moonth(2020, month=month)
