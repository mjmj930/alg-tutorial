要将你当前的 Flask-SocketIO 项目（你贴的代码）**打包为 `.exe` 文件**并实现结构清晰、打包稳定，以下是**完整分步骤操作**：

---

## ✅ 第一步：拆分结构为更适合打包的形式

### 1. 创建两个文件：

#### ✅ `app.py`（只负责定义应用逻辑，不运行）

```python
# ---- 必须最顶部 ----
import eventlet
eventlet.monkey_patch()

# ---- 其他导入必须在 monkey_patch 后 ----
import random
from flask import Flask, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="dist", static_url_path="")
socketio = SocketIO(app, async_mode="eventlet")

def generate_data1():
    return {
        "sensor": "temp",
        "value": round(random.uniform(20.0, 30.0), 2),
        "unit": "°C"
    }

def generate_data2():
    return {
        "sensor": "humidity",
        "value": round(random.uniform(40.0, 70.0), 2),
        "unit": "%"
    }

def background_data_sender():
    while True:
        socketio.emit("data1", generate_data1())
        socketio.emit("data2", generate_data2())
        socketio.sleep(1)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

@socketio.on("connect")
def on_connect():
    print("Client connected")
    socketio.start_background_task(target=background_data_sender)
```

---

#### ✅ `run_server.py`（作为启动入口）

```python
from app import app, socketio

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
```

---

## ✅ 第二步：创建 PyInstaller 打包配置

### 安装 PyInstaller（如果没装过）：

```bash
pip install pyinstaller
```

---

### 在项目根目录执行打包命令：

```bash
pyinstaller --onefile --add-data "dist;dist" run_server.py
```

解释：

| 参数                       | 含义                                             |
| ------------------------ | ---------------------------------------------- |
| `--onefile`              | 打包成一个单独的 `.exe`                                |
| `--add-data "dist;dist"` | 把前端静态资源 `dist/` 文件夹包含进 `.exe` 中（Windows 用 `;`） |
| `run_server.py`          | 启动入口为 run\_server.py                           |

---

## ✅ 第三步：打包后目录结构

打包成功后，你会得到以下文件结构：

```
your_project/
│
├── dist/
│   └── index.html  ← 前端文件
│
├── app.py
├── run_server.py
├── run_server.spec
└── dist/
    └── run_server.exe  ← 你要的可执行程序
```

你只需要：

* 把 `run_server.exe`
* 和前端文件夹 `dist/`

**打包在一起（如：压缩为 zip）就可以部署或发给别人使用了。**

---

## ✅ 补充注意

* 若在 Linux 打包，需加 `:` 替代 `;` → `--add-data "dist:dist"`
* 确保 `index.html` 是存在的，且在 `dist/` 目录中
* `eventlet` 对打包兼容性好，但首次运行 `.exe` 可能稍慢属正常

---

是否需要我生成一个完整的打包脚本 `.bat` 文件，或是帮你写好 `.spec` 文件方便管理？
