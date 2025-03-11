from tkinter import  messagebox
from datetime import datetime
import requests
import sys
import os
import tkinter as tk
import configparser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic
from PyQt5 import QtCore


if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable) 
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))  

config_path = os.path.join(current_dir, "SUProgram.ini")
if not os.path.exists(config_path):
    print(f"❌ 설정 파일이 없습니다! {current_dir} 위치에 auto_start_controller.ini 파일을 추가하세요.")
    sys.exit(1)

config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")
form_class = uic.loadUiType("SUProgram.ui")[0]

admin_id = config.get("USER", "ID")
admin_password = config.get("USER", "PASSWORD")




class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("SUProgram")
        today = datetime.today().strftime("%Y-%m-%d") 
        self.textEdit.setText(today)
        self.pushButton.clicked.connect(self.fetch_data_table)
        self.pushButton_2.clicked.connect(self.update_data_table)
        self.model = QStandardItemModel()
        self.model_sub = QStandardItemModel()
        self.treeView.setModel(self.model)
        self.treeView_2.setModel(self.model_sub)
        self.get_url = config.get("SERVER", "SERVER_GET_IP")
        self.post_url = config.get("SERVER", "SERVER_POST_IP")
        
    
    def eventFilter(self, obj, event):
        if obj == self.textEdit and event.type() == event.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                self.pushButton.click()  
                return True  
        return super().eventFilter(obj, event)


    def fetch_data(self, event_time):
        try:
            params = {
                "eventTime": event_time
            }
            response = requests.get(self.get_url, params=params)
            response.raise_for_status()  
            self.data = response.json()
            return self.data
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"데이터 가져오기 실패: {e}")
            return []

    def fetch_data_table(self):
        event_time = self.textEdit.toPlainText().strip()
        
        if not event_time:
            messagebox.showwarning(self, "경고", "날짜를 입력하세요.")
            return
        
        self.data = self.fetch_data(event_time)
        if not self.data:
            self.treeView.setModel(None)
            messagebox.showerror("Error", "조회할 데이터가 없습니다.")
            return

        columns = list(self.data[0].keys())
        
        self.model.clear()  
        self.model.setHorizontalHeaderLabels(columns)

        column_widths = [len(col) for col in columns]
        
        for row in self.data:
            row_items = []
            for i, col in enumerate(columns):
                item = QStandardItem(str(row[col]))
                row_items.append(item)
                column_widths[i] = max(column_widths[i], len(str(row[col])))  
            self.model.appendRow(row_items)

        self.treeView.setModel(self.model)
        
        
        for i, width in enumerate(column_widths):
            adjusted_width = min(max(width * 5, 30), 300)  
            self.treeView.setColumnWidth(i, adjusted_width)


    def update_data(self):
        self.data_sub = []
        
        try:
            for i in self.data:
                response = requests.post(self.post_url, json=i)
                response.raise_for_status()
                self.data_sub.append(response.json())
            return self.data_sub
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "업데이트 할 데이터가 없습니다.")
            return []
    

    def update_data_table(self):
        self.data_sub = self.update_data()
        if not self.data_sub:
            self.treeView_2.setModel(None)
            messagebox.showerror("Error", "업데이트 할 데이터가 없습니다.")
            return
        columns = list(self.data_sub[0].keys())
        self.model_sub.clear()  
        self.model_sub.setHorizontalHeaderLabels(columns)
        column_widths = [len(col) for col in columns]
        
        for row in self.data_sub:
            row_items = []
            for i, col in enumerate(columns):
                item = QStandardItem(str(row[col]))
                row_items.append(item)
                column_widths[i] = max(column_widths[i], len(str(row[col])))  
            self.model_sub.appendRow(row_items)

        self.treeView_2.setModel(self.model_sub)
        messagebox.showinfo("complete", "업데이트가 완료되었습니다.")
        
        
        for i, width in enumerate(column_widths):
            adjusted_width = min(max(width * 5, 30), 300)  
            self.treeView_2.setColumnWidth(i, adjusted_width)

def show_auth_dialog():
    
    def on_submit():
        user_id = id_entry.get()
        user_pw = pw_entry.get()

        if user_id == admin_id and user_pw == admin_password:
            auth_window.destroy()
            if __name__ == "__main__":
                app = QApplication(sys.argv)
                myWindow = MyWindow()
                myWindow.textEdit.installEventFilter(myWindow)
                myWindow.show()
                app.exec_()
        else:
            messagebox.showerror("오류", "ID 또는 비밀번호가 틀렸습니다.")
            auth_window.destroy()
            show_auth_dialog()

    
    auth_window = tk.Tk()
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

    auth_window.mainloop()

show_auth_dialog()








