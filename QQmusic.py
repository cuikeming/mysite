import requests, json, pymysql,re

connection = pymysql.connect()#mysql数据库
cursor = connection.cursor()

#获取歌手歌曲列表
#批量20首歌曲
url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json=1&cr=1&p=1&n=20&w={}"
new_url = url.format(str(input("请输入你要下载的歌曲或歌星：")))
req = requests.get(new_url)
# print(req.text[9:-1])
data = json.loads(req.text[9:-1])
songs = data["data"]["song"]["list"]
# 将歌曲名及歌曲的mid存储到mids
for song in songs:
    title = song["title"]
    mid = song["mid"]
# 拼接params并请求得到歌曲文件所有请求详情
    params = {
        "data": '{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"5779709973","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"5779709973","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":20,"cv":0}}'%mid
    }
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    req1 = requests.get(url, params=params)
    data2 = json.loads(req1.text)
    # 得到歌曲的详情页链接并请求
    purl = data2["req_0"]["data"]["midurlinfo"][0]["purl"]
    detail_url = "http://111.202.85.148/amobile.music.tc.qq.com/"+purl
    print(detail_url)
    req2 = requests.get(detail_url)
    with open("songsdata/"+mid+".mp3", "wb+") as f:
        f.write(req2.content)
    print(title+" downloading")
    file_path = "songsdata/"+mid+".mp3"
    sql = '''insert into songs_music(name, mid, purl) values ('%s', '%s', '%s')''' %(title, file_path, purl)
    cursor.execute(sql)
    connection.commit()

