#coding:utf8
from . import main
from flask import render_template,jsonify,request
import requests
import re
import json


@main.route('/')
def Home():
    '''首页'''
    return render_template('Home.html')

@main.route('/search')
def search():
    r = request.args.get('songn')
    try:
        url = 'http://localhost:3000/search?limit=8&keywords=%s '%r
        r_url = requests.get(url)
    except Exception as e:
        print 'request错误或者网络异常'
    data = r_url.json()
    # data = json.loads(data,encoding='UTF-8')

    music_list = []  # 用来装字典的
    music_id = []   #用来装歌曲id的
    music_val = data['result']['songs']

    for numb in music_val:
        music_dict = {} # 用来装歌手和歌名的,由于字典的key不能重复，而歌曲名会重复，所以每次for in需要重置字典，并添加到列表中
        music_id.append(numb['id']) # 歌曲id
        music_url = requests.get('http://localhost:3000/song/detail?ids=%s' %numb['id']) # 根据id获取歌曲详情
        music_url1 = music_url.json()
        song_url = music_url1['songs'][0]['al']['picUrl']  # 拿到歌曲封面url
        song_name = numb['artists'][0]['name']  #歌手名字
        music_name = numb['name']
        music_dict[music_name] = [song_name,song_url] # 歌手名，和歌曲封面
        music_list.append(music_dict)

    # print music_id
    # return music_url
    return render_template('search.html',music_list=music_list)

