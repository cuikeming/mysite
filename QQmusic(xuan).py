import requests, json, pymysql,re
#获取歌手歌曲列表
while True:
    #如果想翻页修改链接中的 &p=
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json=1&cr=1&p=1&n=20&w={}"
    new_url = url.format(str(input("请输入你要下载的歌曲或歌星：")))
    req = requests.get(new_url)
    # print(req.text[9:-1])
    data = json.loads(req.text[9:-1])
    songs = data["data"]["song"]["list"]
    i = 0
    mid_list = []
    title_list = []
    for song in songs:
        i+=1
        title = song["title"]
        mid = song["mid"]
        mid_list.append(mid)
        title_list.append(title)
        print("{0}:{1}".format(i,title))
        pass
    num = int(input("请输入你要下载的歌曲序号(如：1):"))
    print(num)
    # 拼接params并请求得到歌曲文件所有请求详情
    params = {
        "data": '{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"5779709973","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"5779709973","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":20,"cv":0}}'%mid_list[num-1]
    }
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    req1 = requests.get(url, params=params)
    data2 = json.loads(req1.text)
    # 得到歌曲的详情页链接并请求
    purl = data2["req_0"]["data"]["midurlinfo"][0]["purl"]
    detail_url = "http://111.202.85.148/amobile.music.tc.qq.com/"+purl
    print(detail_url)
    req2 = requests.get(detail_url)
    with open("songsdata/"+title_list[num-1]+".mp3", "wb+") as f:
        f.write(req2.content)
    y_n = str(input("是否继续下载歌曲,如(y/n)："))
    if y_n.lower() == "y":
        continue
    elif y_n == 'n':
        break
    else:
        print("输入有误，请重新输入")
