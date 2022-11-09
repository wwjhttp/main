from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from random import randint
import os

from time import time

app = Flask(__name__)
CORS(app, supports_credentials=True)
user_data = {}

user = {'别鹤': 888}


def set_filename(filename, filelist):  # 设置文件名， 防止文件重名
    while True:
        numb = randint(0, 100)
        filename = filename[0:filename.index('.') - 1] + f'({numb})' + filename[filename.index('.'):]
        if filename not in filelist:
            return filename


def funcion(_ip):
    _ip = str(_ip)
    ct = time()
    data_secs = round((ct - int(ct)) * 1000)
    if _ip not in user.keys():
        user[_ip] = data_secs
        return True
    time_ed = user[_ip]
    if data_secs < time_ed:
        new_t = data_secs + 1000 - time_ed
        user[_ip] = data_secs
        return False if new_t < 130 else True
    elif data_secs > time_ed:
        new_t = data_secs - time_ed
        user[_ip] = data_secs
        return False if new_t < 130 else True
    elif time_ed == data_secs:
        return False


def p_r():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        user_ip = request.environ['REMOTE_ADDR']
    else:
        user_ip = request.environ['HTTP_X_FORWARDED_FOR']

    return funcion(user_ip)


# @app.route('/favicon.ico', methods=['POST', 'GET'])  # 返回 favicon.ico图片
# def favicon_png():
#     return send_file(r'image/主页背景.ico')


@app.route('/tool/uploadfile_page', methods=['POST', 'GET'])  # 返回网站页面
def uploadfiler():
    return send_file(r'html_data/uploadfile.html')


@app.route('/fun/uploadimg', methods=['POST', 'GET'])  # 返回网站页面
def uploadfunimg():
    # return send_file(r'html_data/UploadFunImg.html')
    return send_file(r'html_data/UploadFunImg.html')


# ##########
@app.route('/tool/download_page', methods=['POST', 'GET'])  # 返回网站页面
def download_page():
    return send_file(r'html_data/download.html')


@app.route('/ce', methods=['POST', 'GET'])  # 返回网站页面
def ce():
    return send_file(r'html_data/ce1.html')


@app.route('/aboutme', methods=['POST', 'GET'])  # 返回网站页面
def aboutme():
    return send_file(r'html_data/aboutme.html')


@app.route('/tool-list', methods=['POST', 'GET'])  # 返回网站页面
def tool():
    return send_file(r'html_data/tool_list.html')


@app.route('/fun', methods=['POST', 'GET'])  # 返回网站页面
def fun():
    return send_file(r'html_data/fun.html')


@app.route('/', methods=['POST', 'GET'])  # 返回网站页面
def start():
    return send_file(r'html_data/index.html')


@app.route('/login', methods=['POST', 'GET'])  # 返回网站页面
def login_page():
    return send_file(r'html_data/login.html')


# ************* ^ 上方文件返回区 下方功能接口区  *********

# 登陆接口
#
#
# @app.route('/new_login/updata', methods=['post', 'get'])
# def Login_updata():
#     data = request.get_json()
#     print(data)
#     user_name = data['name']
#     pasword = int(data['password'])
#     dict = {
#         'code': 0,
#         'url': ''
#     }
#
#     if user_name in user.keys():
#         if pasword == user[user_name]:
#             dict['code'] = 200
#             dict['url'] = new_file_url
#         else:
#             dict['code'] = 400
#             dict['msg'] = '密码错误'
#     else:
#         dict['code'] = 400
#         dict['msg'] = '用户名错误'
#     return jsonify(dict)


@app.route('/fun/UpFunFile', methods=['POST', 'GET'])  # 搞笑图片文件上传接口
def UpFunFile():
    filenamelist = []
    data = request.files.getlist("file")
    msg = 'True'
    try:
        for file in data:
            filename = file.filename
            ce = ['png', 'PNG','JPG','jpeg', 'jpg', 'ico', 'tif', 'gif', 'psd', 'raw', 'svg']
            filename_lost = filename[filename.rindex('.') + 1:]
            if filename_lost not in ce:
                msg = f'<h1>{filename}: 该文件格式错误</h1>'
                return msg
            filelist = os.listdir('image/fun/')
            if filename in filelist:
                filename = set_filename(filename, filelist)
            file.save(os.path.join('image/fun', filename))
            filenamelist.append('<br>' + filename)

        if msg == 'True':
            return f'<h1>文件上传成功 文件名-{"".join(filenamelist)}</h1>'
        else:
            return msg
    except Exception as a:
        return '文件上传失败' + str(a)


@app.route('/tool/uploadfile', methods=['POST', 'GET'])  # tool 文件上传接口 
def uploadfile():

    filenamelist = []
    data = request.files.getlist("file")
    try:
        for file in data:
            filename = file.filename
            filelist = os.listdir('upload/')
            if filename in filelist:
                filename = set_filename(filename, filelist)
            file.save(os.path.join('upload/', filename))
            filenamelist.append('<br>' + filename)

        return f'<h1>文件上传成功 文件名-{"".join(filenamelist)}</h1>'
    except Exception as a:
        return '文件上传失败' + str(a)


@app.route('/tool/download_file/<filename>', methods=['POST', 'GET'])
def download_file(filename):

    return send_file('upload/' + filename)  # tool 文件下载接口


@app.route('/get_img/<filename>', methods=['POST', 'GET'])  # 获取image/文件夹下的图片
def get_img(filename):
    path = 'image/' + filename
    try:
        return send_file(path)
    except OSError:
        return jsonify({'msg': f'该文件{filename}不存在'})


@app.route('/fun/get_img/<filename>', methods=['POST', 'GET'])  # 获取搞笑图片接口
def function2(filename):
    path = 'image/fun/' + filename
    try:
        return send_file(path)
    except OSError:
        pass


@app.route('/function1', methods=['POST', 'GET'])
def function1():
    """
    负责fun.html里图片列表
    注: fun.html会先请求这个接口， 然后接口会返回一个(图片文件名)的列表， 例如['a.png', 'b.png']
    列表里的图片文件是随机的， 然后fun.html会根据列表里的文件名请求相应的图片
    :return: list
    """
    data = request.get_json()
    png_list = os.listdir('image/fun/')
    ret_data = {
        'list_': [],
        'msg': ''
    }
    # 暂无更多
    while True:
        if len(ret_data['list_']) < 20:
            if len(png_list) == 0:
                ret_data['msg'] = '暂无更多'
                return jsonify(ret_data)
            name = png_list[randint(0, len(png_list) - 1)]
            if name not in data['list_']:
                ret_data['list_'].append(name)
                del png_list[png_list.index(name)]
            else:
                del png_list[png_list.index(name)]

        else:
            return jsonify(ret_data)


@app.route('/tool/get_file/<filename>', methods=['POST', 'GET'])  # tool 文件下载预览接口
def get_file(filename):
    # 简单粗暴的文件类别分辨
    filename_lost = filename[filename.rindex('.') + 1:]
    if filename_lost in ['html', 'htm']:
        with open(f'upload/{filename}') as file:
            data = file.read()
        data = "<xmp style='font-size: 20px;'>" + data + '</xmp>'
        return data
    if filename_lost in ['MOV', 'mp4', 'wmv', 'asf', 'asx', 'rm', 'rmvb', 'mpg', 'mpeg', 'mpe', '3gp', 'mvo', 'm4v',
                         'avi', 'dat', 'mkv', 'flv', 'vob']:
        url = '/tool/download_file/' + filename
        data = f"""<video style='overflow: auto; width:100%;' controls><source src="{url}"  type="video/mp4"></video>"""
        return data
    if filename_lost in ['png', 'jpeg', 'jpg', 'ico', 'tif', 'gif', 'psd', 'raw', 'svg']:
        url = '/tool/download_file/' + filename
        data = f"""<img style="width: 100%; height: 98vh; object-fit: contain;" src="{url}" alt="图片加载失败">"""
        return data
    else:
        return send_file('upload/' + filename)


@app.route('/tool/get_file_list', methods=['POST', 'GET'])  # tool 获取 upload/ 文件列表
def get_file_list():
    filelist = os.listdir('upload/')
    return str(filelist)


if __name__ == '__main__':  # 开启服务
    app.run(host='0.0.0.0', port=80)
