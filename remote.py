from flask import Flask, send_from_directory, request
import pyautogui
import pygetwindow as gw
import socket
import webbrowser

app = Flask(__name__)

APP_TITLES = {
    "wmp": "Media Player",
    "mpc": "Media Player Classic",
    "bsplayer": "BS.Player",
    "brave": "Brave"
}

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def focus_app(title_fragment):
    for window in gw.getWindowsWithTitle(title_fragment):
        if window.isMinimized:
            window.restore()
        window.activate()
        return True
    return False

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('static', 'style.css')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/control/<app>/<action>')
def control(app, action):
    print("🔍 Open Windows:")
    for w in gw.getAllWindows():
        if w.title:
            print(f"→ {w.title}")

    app_title = APP_TITLES.get(app.lower())
    if not app_title:
        return f"Unknown app: {app}", 400

    if not focus_app(app_title):
        return f"App window not found: {app_title}", 404

    if action == "pause":
        pyautogui.press('space')
    elif action == "volumeup":
        pyautogui.press('volumeup')
    elif action == "volumedown":
        pyautogui.press('volumedown')
    else:
        return f"Unknown action: {action}", 400

    return f"{app} -> {action}", 200

if __name__ == '__main__':
    ip = get_ip()
    print(f"📱 Access this from your phone: http://{ip}:5000")
    webbrowser.open(f"http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000)
