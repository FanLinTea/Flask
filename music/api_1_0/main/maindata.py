# coding:utf8
import redis
from . import main
from flask import render_template,request,jsonify,g,redirect
import requests
import random
from flask_login import login_required,current_user
from music.models import My_music
from music import db

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
        song_list =  data['playlist']['tracks']
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
            songcnd_url = requests.get('http://localhost:3000/music/url?id=%s' % ids)
            songcnd_url1 = songcnd_url.json()
            music_url1 = music_url.json()
            song_url = music_url1['songs'][0]['al']['picUrl']  # 拿到歌曲封面url
            song_name = music_url1['songs'][0]['ar'][0]['name']  # 歌手名字
            music_name = music_url1['songs'][0]['name']
            songcdn = songcnd_url1['data'][0]['url']  #  音乐的url链接
            song_key = 'song_key%s' %random.randint(0,100000) # 由于接受url作为参数传递会出现页面获取不到数据
            Music_REDIS.set(song_key, songcdn,ex=60*60*24)  # 所以先把地址保存到reids
            song2_url = 'song_url%s' %random.randint(0,100000)#11
            Music_REDIS.set(song2_url, song_url,ex=60*60*24)  #11
            daysong_dact[music_name] = [song_name, song_url,song_key,song2_url,ids]#11

        #  以下是为了获取Billboard榜单的歌曲信息
        Billboard_url = requests.get('http://localhost:3000/top/list?idx=6')
        Billboard_json = Billboard_url.json()
        Billboard_list_data = Billboard_json['playlist']['tracks']
        Billboard_list = {}

        for i in Billboard_list_data:
            if len(Billboard_list) >7:
                break
            Billboard_list[i['name']] = [i['ar'][0]['name'],i['al']['picUrl']]
        Music_REDIS.set('daysong_dact',daysong_dact,ex=60)
        Music_REDIS.set('Billboard_list',Billboard_list,ex=60)
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

        songcnd_url = requests.get('http://localhost:3000/music/url?id=%s' % numb['id'])
        songcnd_url1 = songcnd_url.json()
        songcdn = songcnd_url1['data'][0]['url']  # 音乐的url链接
        song_key = 'song_key%s' % random.randint(0, 100000)
        Music_REDIS.set(song_key, songcdn, ex=60 * 60 * 24)

        music_url1 = music_url.json()
        song_url = music_url1['songs'][0]['al']['picUrl']  # 拿到歌曲封面url
        song2_url = 'song_url%s' % random.randint(0, 100000)  # 11
        Music_REDIS.set(song2_url, song_url, ex=60 * 60 * 24)  # 11

        song_name = numb['artists'][0]['name']  # 歌手名字
        music_name = numb['name']
        music_dict[music_name] = [song_name, song_url,song_key,song2_url,numb['id']]  # 歌手名，和歌曲封面
        music_list.append(music_dict)

    return render_template('search.html', music_list=music_list)

@main.route('/musicplays/<url>/<path:img_url>/<pname>/<songname>')
def dailyupdate(url,img_url,pname,songname):
    url = Music_REDIS.get(url)
    img_url = Music_REDIS.get(img_url)

    return render_template('musicplay.html',url=url,img_url=img_url,pname=pname,songname=songname)


@main.route('/collection',methods=['POST'])
def collection():
    #  用于收藏音乐的接口
    try:  # 由于此接口由ajax调用，login_required装饰不能让未登录者调转到登录页面
        user_id = current_user.id
    except:
        return jsonify(erro='nologin')  # 因此在拿不到用户Id的时候返回一个数据来让ajax跳转页面。
    music_id = request.form.get('id')
    musics = My_music.query.filter_by(music_id=music_id).first()
    if not musics:
        col = My_music(user_id=user_id,music_id=music_id)
        db.session.add(col)
        db.session.commit()
    return render_template('login.html')



@login_required
@main.route('/mymusic')
def mymusic():
    try:
        user_id = current_user.id
    except Exception as e:
        return redirect('/login')
        print e
    id = My_music.query.filter_by(user_id=user_id).all()
    music_id = [a.music_id for a in id]

    music_list = {}
    for a in music_id:
        music_url = requests.get('http://localhost:3000/song/detail?ids=%s' % a)
        music_url1 = music_url.json()
        song_url = music_url1['songs'][0]['al']['picUrl']  # 拿到歌曲封面url
        song_name = music_url1['songs'][0]['ar'][0]['name']  # 歌手名字
        music_name = music_url1['songs'][0]['name']
        song2_url = 'song_url%s' % random.randint(0, 100000)  # 11
        Music_REDIS.set(song2_url, song_url, ex=60 * 60 * 24)  # 11

        songcnd_url = requests.get('http://localhost:3000/music/url?id=%s' % a)
        songcnd_url1 = songcnd_url.json()
        songcdn = songcnd_url1['data'][0]['url']  # 音乐的url链接
        song_key = 'song_key%s' % random.randint(0, 100000)
        Music_REDIS.set(song_key, songcdn, ex=60 * 60 * 24)
        music_dict = [song_name, song_url,song2_url, song_key]
        music_list[music_name] = music_dict

        # url = Music_REDIS.get(url)
        # img_url = Music_REDIS.get(img_url)
    return render_template('mymusic.html', music_list=music_list)