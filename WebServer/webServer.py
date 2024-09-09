# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os
import urllib.parse

app = Flask(__name__)

# 设置文件上传路径
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 设置日志上传路径
LOG_FOLDER = os.path.join(os.getcwd(), 'logs')
app.config['LOG_FOLDER'] = LOG_FOLDER

# 设置文件大小限制 (例如，限制为16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 主页展示上传表单和文件列表
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string('''
    <!doctype html>
    <title>File Server</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data action="{{ url_for('upload_file') }}">
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <h2>Files</h2>
    <ul>
      {% for file in files %}
        <li>
          <a href="{{ url_for('download_file', filename=urllib.parse.quote(file)) }}">{{ file }}</a>
          <form method="post" action="{{ url_for('delete_file', filename=urllib.parse.quote(file)) }}" style="display:inline;">
            <button type="submit">Delete</button>
          </form>
        </li>
      {% endfor %}
    </ul>
    ''', files=files, urllib=urllib)

# 文件上传处理
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('index'))

# 文件下载处理
@app.route('/uploads/<filename>')
def download_file(filename):
    filename = urllib.parse.unquote(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Attempting to send file from {file_path}")  # Debugging information
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")  # Debugging information
        return "File not found", 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 文件删除处理
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        filename = urllib.parse.unquote(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Attempting to delete file from {file_path}")  # Debugging information
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"File deleted: {file_path}")  # Debugging information
        else:
            print(f"File not found: {file_path}")  # Debugging information
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")  # Debugging information
        return str(e), 404

#以上是上传下载删除文件的操作

# 定义一个带参数的路由
@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/logs', methods=['POST'])
def log():
    player_id = request.headers.get('PlayerID')
    if not player_id:
        return "Player_ID header is missing", 400
    
    player_name = request.headers.get('PlayerName')
    if not player_name:
        return "player_Name header is missing", 400
    
    player_level = request.headers.get('PlayerLevel')
    if not player_level:
        return "player_Level header is missing", 400
    
    timeStr = request.headers.get('TimeStamp')
    if not timeStr:
        return "timeStr header is missing", 400

    log_message = request.data.decode('utf-8')
    player_log_folder = os.path.join(LOG_FOLDER, player_id)
    log_file_path = os.path.join(player_log_folder, 'log.txt')

    # 如果玩家日志文件夹不存在，则创建
    if not os.path.exists(player_log_folder):
        os.makedirs(player_log_folder)

    # 创建log.txt文件
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as log_file:
            log_file.write('')

    with open(log_file_path, 'a') as log_file:
        log_file.write(log_message + '\n')

    print(f"PlayerId:{player_id} PlayerName:{player_name} player_level:{player_level} timeStr:{timeStr}\n{log_message}")  # Debugging information
    return "Log received", 200

# 使用自定义函数作为路由
@app.route('/logout', methods=['POST'])
def logOut():
    player_id = request.headers.get('PlayerID')
    if not player_id:
        return "Player_ID header is missing", 400
    
    player_name = request.headers.get('PlayerName')
    if not player_name:
        return "player_Name header is missing", 400
    
    player_level = request.headers.get('PlayerLevel')
    if not player_level:
        return "player_Level header is missing", 400
    
    timeStr = request.headers.get('TimeStamp')
    if not timeStr:
        return "timeStr header is missing", 400
    
    player_log_folder = os.path.join(LOG_FOLDER, player_id)
    log_file_path = os.path.join(player_log_folder, 'log.txt')

    # 如果玩家日志文件夹不存在，则异常404
    if not os.path.exists(log_file_path):
        return "Player log txt does not exist", 404

    with open(log_file_path, 'a') as log_file:
        log_file.write(f'============================================Player:{player_id} at {timeStr} logout===================================================')
        log_file.close()

    return "Log out received", 200

if __name__ == '__main__':
    app.run(debug=True)