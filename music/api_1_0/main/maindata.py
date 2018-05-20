# coding:utf8
import redis

from . import main
from flask import render_template, jsonify, request
import requests
import random
import time
import json

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
Music_REDIS = redis.StrictRedis()

@main.route('/')
def Home():
    # 由于接口返回数据太慢，当第一次访问主页后，把数据放到redis中，提高下次访问速度
    if not Music_REDIS.get('Billboard_list') and not Music_REDIS.get('daysong_dact'):
        #  以下是为了获得随机推荐歌曲的信息
        url = 'http://localhost:3000/playlist/detail?id=2233124290'
        r_url = requests.get(url)
        data = r_url.json()
        song_list =  data['result']['tracks']
        daysong = []
        daysong_dact = {}
        daysong1 = []

        for id in song_list:
            song_id = id['id']
            daysong.append(song_id)

        while len(daysong1) != 8: # 生成随机的歌曲id
            data = daysong[random.randint(0,len(daysong))]
            daysong1.append(data)

        for ids in daysong1: # 获得随机歌曲的信息
            music_url = requests.get('http://localhost:3000/song/detail?ids=%s' % ids)  # 根据id获取歌曲详情
            music_url1 = music_url.json()
            song_url = music_url1['songs'][0]['al']['picUrl']  # 拿到歌曲封面url
            song_name = music_url1['songs'][0]['ar'][0]['name']  # 歌手名字
            music_name = music_url1['songs'][0]['name']
            daysong_dact[music_name] = [song_name, song_url]

        #  以下是为了获取Billboard榜单的歌曲信息
        Billboard_url = requests.get('http://localhost:3000/top/list?idx=6')
        Billboard_json = Billboard_url.json()
        Billboard_list_data = Billboard_json['playlist']['tracks']
        Billboard_list = {}

        for i in Billboard_list_data:
            if len(Billboard_list) >7:
                break
            Billboard_list[i['name']] = [i['ar'][0]['name'],i['al']['picUrl']]
        Music_REDIS.set('daysong_dact',daysong_dact,ex=60*10)
        Music_REDIS.set('Billboard_list',Billboard_list,ex=60*10)
    else:
        daysong_dact =eval(Music_REDIS.get('daysong_dact'))
        Billboard_list = eval(Music_REDIS.get('Billboard_list'))

    return render_template('Home.html', daysong_dact=daysong_dact,Billboard_list=Billboard_list)
    # return render_template('Home.html')


@main.route('/search')
def search():
    '''搜索接口'''
    r = request.args.get('songn')
    try:
        url = 'http://localhost:3000/search?limit=8&keywords=%s ' % r
        r_url = requests.get(url)
    except Exception as e:
        print 'request错误或者网络异常'
    data = r_url.json()

    music_list = []  # 用来装字典的
    music_id = []  # 用来装歌曲id的
    music_val = data['result']['songs']

    for numb in music_val:
        music_dict = {}  # 用来装歌手和歌名的,由于字典的key不能重复，而歌曲名会重复，所以每次for in需要重置字典，并添加到列表中
        music_id.append(numb['id'])  # 歌曲id
        music_url = requests.get('http://localhost:3000/song/detail?ids=%s' % numb['id'])  # 根据id获取歌曲详情
        music_url1 = music_url.json()
        song_url = music_url1['songs'][0]['al']['picUrl']  # 拿到歌曲封面url
        song_name = numb['artists'][0]['name']  # 歌手名字
        music_name = numb['name']
        music_dict[music_name] = [song_name, song_url]  # 歌手名，和歌曲封面
        music_list.append(music_dict)

    return render_template('search.html', music_list=music_list)

# @main.route('/dupdate')
# def dailyupdate():

    # return '%s'%daysong
