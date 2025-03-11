import time
import json
import requests
import threading
import tkinter as tk
import configparser
import os
import sys
import pystray
from tkinter import scrolledtext, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image



if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)  # 실행 파일 위치
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # 개발 환경
config_path = os.path.join(current_dir, "config.ini")
if not os.path.exists(config_path):
    print(f"❌ 설정 파일이 없습니다! {config_path} 위치에 config.ini 파일을 추가하세요.")
    sys.exit(1)
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")
server_ip = config.get("SERVER", "SERVER_IP")
watch_folder = config.get("WATCH_FOLDER", "FOLDER_SELECTED")
admin_id = config.get("USER", "ID")
admin_password = config.get("USER", "PASSWORD")

SERVER_URL = server_ip
watching = False
observer = None
retry_send_limit = config.get("RETRY", "SEND_LIMIT")  
retry_link_limit = config.get("RETRY", "LINK_LIMIT")  
server_check_running = True
watch_check_handler = 0

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            log_message(f"create directory {directory}.")
    except OSError:
        log_message("Error: Failed to create the directory.")

class JsonFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            time.sleep(1)  
            send_json(event.src_path)
            

def send_json(file_path, attempt=1):
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)

        response = requests.post(SERVER_URL, json=json_data)
        log_message(f"[✅] 전송 완료: {file_path}, 응답: {response.status_code}")
    except Exception as e:
        log_message(f"[❌] 전송 실패 ({attempt}/{retry_send_limit}): {file_path}")
        if attempt < retry_send_limit:
            time.sleep(3)  
            send_json(file_path, attempt + 1)

def start_watching(attempt=1):
    global observer, watching, watch_check_handler
    if watch_check_handler == 0:
        if not watch_folder:
            log_message(f"[❌] 감시할 폴더가 없습니다")
            return
        else:
            try:
                response = requests.post(SERVER_URL)
                log_message(f"[✅] 서버에 접속 성공, 응답: {response.status_code}")
                log_message(f"🔍 감시 시작! 폴더: {watch_folder}")
                watching = True
                event_handler = JsonFileHandler()
                observer = Observer()
                observer.schedule(event_handler, watch_folder, recursive=False)
                observer.start()
                watch_check_handler = 1
            except Exception as e:
                log_message(f"[❌] 서버 접속 실패 ({attempt}/{retry_link_limit})")
                if attempt < retry_link_limit:
                    start_watching(attempt + 1)
    else:
        log_message("🔍 감시중")

def server_update_status(text, color):
    server_check.config(text=f"서버 상태: {text}", bg = color)

def server_watching():
    server_update_status("확인중..", "gray")
    while server_check_running:
        try:
            response = requests.post(SERVER_URL)
            if server_check['bg'] == "gray" or server_check['bg'] == "red":
                log_message("[✅] 서버 접속 성공")
            server_update_status("접속중", "green")
            
        except Exception as e:
            if server_check['bg'] == "gray" or server_check['bg'] == "green":
                log_message("[❌] 서버 접속 실패")
            server_update_status("접속끊김", "red")
        time.sleep(3)   
 
                 

def stop_watching():
    global observer, watching, watch_check_handler
    if watching == False:
        log_message("[❌] 감시가 시작중이지 않습니다.")
        return
    else:
        if observer:
            observer.stop()
            observer.join()
            observer = None
        watching = False
        watch_check_handler = 0
        log_message("🛑 감시 중지됨.")

    
def log_message(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)


def create_tray_icon():
    image = image = Image.new("RGB", (64, 64), (255, 0, 0))  
    menu = pystray.Menu(pystray.MenuItem("열기", show_window), pystray.MenuItem("종료", show_auth_dialog))
    tray_icon = pystray.Icon("App", image, menu=menu)
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()
    
def hide_program():
    main.withdraw()

def show_window():
    def on_submit():
        user_id = id_entry.get()
        user_pw = pw_entry.get()

        if user_id == admin_id and user_pw == admin_password:
            auth_window.destroy()
            main.after(0, main.deiconify)
        else:
            messagebox.showerror("오류", "ID 또는 비밀번호가 틀렸습니다.")
            auth_window.destroy()
            show_window()

    
    auth_window = tk.Toplevel()
    auth_window.title("관리자 인증")
    auth_window.geometry("300x200")
    auth_window.resizable(False, False)

    
    tk.Label(auth_window, text="관리자 ID:").pack(pady=5)
    id_entry = tk.Entry(auth_window)
    id_entry.pack(pady=5)

    
    tk.Label(auth_window, text="비밀번호:").pack(pady=5)
    pw_entry = tk.Entry(auth_window, show="*")
    pw_entry.pack(pady=5)

    
    submit_btn = tk.Button(auth_window, text="확인", command=on_submit)
    submit_btn.pack(pady=10)  

def show_auth_dialog():
    
    def on_submit():
        user_id = id_entry.get()
        user_pw = pw_entry.get()

        if user_id == admin_id and user_pw == admin_password:
            messagebox.showinfo("확인", "프로그램을 종료합니다.")
            auth_window.destroy()
            main.quit()
        else:
            messagebox.showerror("오류", "ID 또는 비밀번호가 틀렸습니다.")
            auth_window.destroy()
            show_auth_dialog()

    
    auth_window = tk.Toplevel()
    auth_window.title("관리자 인증")
    auth_window.geometry("300x200")
    auth_window.resizable(False, False)

    
    tk.Label(auth_window, text="관리자 ID:").pack(pady=5)
    id_entry = tk.Entry(auth_window)
    id_entry.pack(pady=5)

    
    tk.Label(auth_window, text="비밀번호:").pack(pady=5)
    pw_entry = tk.Entry(auth_window, show="*")
    pw_entry.pack(pady=5)

    
    submit_btn = tk.Button(auth_window, text="확인", command=on_submit)
    submit_btn.pack(pady=10)

    
server_check_thread = threading.Thread(target=server_watching, daemon=True)
start_watching_thread = threading.Thread(target=start_watching, daemon=True)

main = tk.Tk()
main.title("JSON server 전송 프로그램")
main.geometry("550x450")

folder_check = tk.Label(main, text=f"📂 {watch_folder}", bg="gray", fg="white", font=("Arial", 12))
folder_check.pack(pady=5)

start_button = tk.Button(main, text="▶ 시작", command=lambda: threading.Thread(target=start_watching, daemon=True).start(), bg="gray", fg="white", font=("Arial", 12))
start_button.pack(pady=10)

stop_button = tk.Button(main, text="■ 중지", command=lambda: threading.Thread(target=stop_watching, daemon=True).start(), bg="gray", fg="white", font=("Arial", 12))
stop_button.pack(pady=5)

log_text = scrolledtext.ScrolledText(main, state=tk.DISABLED, height=15, width=65)
log_text.pack(pady=10)

server_check = tk.Label(main, text="확인중..", bg="gray", fg="white", width=20, height=2)
server_check.pack(pady=5)

createDirectory(watch_folder)
server_check_thread.start()
start_watching_thread.start()
main.protocol('WM_DELETE_WINDOW', hide_program)
create_tray_icon()
main.mainloop()
