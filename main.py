import requests
import regex as re
import time
import matplotlib.pyplot as plt

cookie = "SESSDATA=***"



regex_aid = r'"aid":([0-9]+),'
regex_title = r'h1 data-title="(.*?)"'
regex_date = r'itemprop="uploadDate" content="(.*?)"'
regex_emoji = r'\[(.*?)\]'
comment_api = "https://api.bilibili.com/x/v2/reply"

def main():
    emoji_count = {}
    vid = input("输入BV号：")
    url = "https://www.bilibili.com/video/" + vid
    headers = {
        "cookie": cookie,
        "referer": url,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    }
    response = requests.get(url, headers=headers).text
    aid = re.findall(regex_aid, response)[0]
    title = re.findall(regex_title, response)[0]
    date = re.findall(regex_date, response)[0]
    print("标题：", title, "上传日期：", date)
    if not aid:
        print("aid获取失败")
        return
    params = {
        "type": "1",
        "oid": aid,
        "pn": "1",
        "nohot": "0",
        "sort": "1",
        "ps": "20"
    }
    response = requests.get(comment_api, headers=headers, params=params).json()
    comments = response["data"]["replies"]
    pages = response["data"]["page"]["count"] // 20
    for i in range(pages):
        cnt=0
        for comment in comments:
            like = comment["like"]
            if like > 300:
                cnt+=1
                ctime = comment["ctime"]
                content = comment["content"]["message"]
                emoji = re.findall(regex_emoji, content)
                for e in set(emoji):
                    if e in emoji_count:
                        emoji_count[e] += like
                    else:
                        emoji_count[e] = like
                user = comment["member"]["uname"]
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime)), like, user, content, sep='\t')
        if cnt==0:
            print("无更多热评")
            break
        params["pn"] = str(i + 2)
        response = requests.get(comment_api, headers=headers, params=params).json()
        comments = response["data"]["replies"]
    print("表情统计：")
    for e in emoji_count:
        print(e, emoji_count[e])
    plt.rcParams['font.family'] = ['SimHei']
    plt.bar(emoji_count.keys(), emoji_count.values())
    plt.show()

if __name__ == "__main__":
    main()
