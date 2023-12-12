from flask import Flask, render_template, request
from flask_socketio import SocketIO
import mysql.connector
import eventlet

eventlet.monkey_patch()

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
# MySQL数据库连接配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "test"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 从右边输入框获取SQL
        sql_text = request.json.get("query_text")
        # 执行SQL
        table_headers, table_rows = fetch_devices(sql_text)
        result = {"table_headers":table_headers, "table_rows":table_rows}
        
        return result

    # 初始页面加载时也需要生成动态表格
    table_headers, table_rows = fetch_devices("")
    return render_template("index.html", table_headers=table_headers, table_rows=table_rows)

@app.route("/query", methods=["POST"])
def query():
    # 从右边输入框获取用户输入的查询内容
    query_text = request.form.get("query_text")
    
    return query_text

def fetch_devices(sql):
    print(sql)
    if(sql == ""):
        sql = "select * from device"
    try:
        # 连接到MySQL数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 执行查询操作
        query = sql
        cursor.execute(query)

        # 获取查询结果
        result = cursor.fetchall()

        # 获取字段名
        headers = [i[0] for i in cursor.description]

        # 关闭游标和连接
        cursor.close()
        conn.close()

        return headers, result

    except mysql.connector.Error as e:
        print("Error while fetching data from MySQL:", e)
        return [], []
    
@socketio.on('audio')
def handle_audio(data):
    # Handle audio data here, and save it to a file
    with open('audio.wav', 'wb') as f:
        f.write(data)
    # result = model.transcribe("audio.wav")
    # simplified_text = zhconv.convert(result["text"], 'zh-cn')
    socketio.emit('saved',"simplified_text")
    
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, keyfile='key.pem', certfile='cert.pem')