from PyQt5 import QtCore, QtWidgets
import tkinter as tk
from tkinter import  messagebox
import os
import configparser
import sys
from datetime import datetime
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import requests

if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable) 
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))  

config_path = os.path.join(current_dir, "SUProgram.ini")
if not os.path.exists(config_path):
    print(f"❌ 설정 파일이 없습니다! {current_dir} 위치에 SUProgram.ini 파일을 추가하세요.")
    sys.exit(1)

config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

admin_id = config.get("USER", "ID")
admin_password = config.get("USER", "PASSWORD")

class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textEdit.installEventFilter(self)
        today = datetime.today().strftime("%Y-%m-%d") 
        self.textEdit.setText(today)
        self.model = QStandardItemModel()
        self.model_sub = QStandardItemModel()
        self.treeView.setModel(self.model)
        self.treeView_2.setModel(self.model_sub)
        self.pushButton.clicked.connect(self.fetch_data_table)
        self.pushButton_2.clicked.connect(self.update_data_table)
        self.get_url = config.get("SERVER", "SERVER_GET_IP")
        self.post_url = config.get("SERVER", "SERVER_POST_IP")
        self.data = []
        self.data_sub = []


    def setupUi(self, Dialog):
        Dialog.setObjectName("SUProgram")
        Dialog.setEnabled(True)
        Dialog.resize(1392, 783)
        Dialog.setMinimumSize(QtCore.QSize(1392, 783))
        Dialog.setMaximumSize(QtCore.QSize(1392, 783))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 321, 21))
        self.label.setObjectName("label")
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(170, 30, 93, 28))
        self.pushButton.setObjectName("pushButton")
        
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 400, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 60, 1371, 341))
        self.frame.setMinimumSize(QtCore.QSize(1371, 341))
        self.frame.setMaximumSize(QtCore.QSize(1371, 341))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.treeView = QtWidgets.QTreeView(self.frame)
        self.treeView.setEnabled(True)
        self.treeView.setGeometry(QtCore.QRect(10, 10, 1351, 321))
        self.treeView.setMinimumSize(QtCore.QSize(1351, 321))
        self.treeView.setMaximumSize(QtCore.QSize(1351, 321))
        self.treeView.setObjectName("treeView")
        self.treeView.header().setVisible(True)
        self.treeView.header().setStretchLastSection(False)
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(10, 430, 1371, 351))
        self.frame_2.setMinimumSize(QtCore.QSize(1371, 351))
        self.frame_2.setMaximumSize(QtCore.QSize(1371, 351))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.treeView_2 = QtWidgets.QTreeView(self.frame_2)
        self.treeView_2.setGeometry(QtCore.QRect(10, 10, 1351, 331))
        self.treeView_2.setMinimumSize(QtCore.QSize(1351, 331))
        self.treeView_2.setMaximumSize(QtCore.QSize(1351, 331))
        self.treeView_2.setObjectName("treeView_2")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 30, 141, 31))
        self.textEdit.setFrameShape(QtWidgets.QFrame.Box)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setObjectName("textEdit")
        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("SUProgram", "SUProgram"))
        self.label.setText(_translate("SUProgram", "날짜 입력 (예: 20XX.XX.XX or 20XX-XX-XX)"))
        self.pushButton.setText(_translate("SUProgram", "조회"))
        self.pushButton_2.setText(_translate("SUProgram", "업데이트"))

    def eventFilter(self, obj, event):
        if obj == self.textEdit and event.type() == event.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                self.fetch_data_table()  
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
        
        if not event_time or "":
            messagebox.showerror("경고", "날짜를 입력하세요.")
            return
        self.data.clear()
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
                item.setEditable(False)
                row_items.append(item)
                column_widths[i] = max(column_widths[i], len(str(row[col])))  
            self.model.appendRow(row_items)

        self.treeView.setModel(self.model)
        
        
        for i, width in enumerate(column_widths):
            adjusted_width = min(max(width * 5, 30), 300)  
            self.treeView.setColumnWidth(i, adjusted_width)


    def update_data(self):
        
        
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
        if not self.data:
            self.treeView_2.setModel(None)
            messagebox.showerror("Error", "업데이트 할 데이터가 없습니다.")
            return
        def on_submit():
            user_pw = pw_entry.get()
            if user_pw == admin_password:
                self.data_sub.clear()
                self.data_sub = self.update_data()
                columns = list(self.data_sub[0].keys())
                self.model_sub.clear()  
                self.model_sub.setHorizontalHeaderLabels(columns)
                column_widths = [len(col) for col in columns]
                
                for row in self.data_sub:
                    row_items = []
                    for i, col in enumerate(columns):
                        item = QStandardItem(str(row[col]))
                        item.setEditable(False)
                        row_items.append(item)
                        column_widths[i] = max(column_widths[i], len(str(row[col])))  
                    self.model_sub.appendRow(row_items)

                self.treeView_2.setModel(self.model_sub)
                messagebox.showinfo("complete", "업데이트가 완료되었습니다.")
                
                
                for i, width in enumerate(column_widths):
                    adjusted_width = min(max(width * 5, 30), 300)  
                    self.treeView_2.setColumnWidth(i, adjusted_width)
                    
                check.destroy()
                    
            else:
                messagebox.showerror("오류", "ID 또는 비밀번호가 틀렸습니다.")
                check.destroy()
                self.update_data_table()
        check = tk.Tk()
        check.title("관리자 인증")
        check.geometry("300x200")
        check.resizable(False, False)
    
        tk.Label(check, text="비밀번호:").pack(pady=5)
        pw_entry = tk.Entry(check, show="*")
        pw_entry.pack(pady=5)

    
        submit_btn = tk.Button(check, text="확인", command=on_submit)
        submit_btn.pack(pady=10)

        check.mainloop()

        



        


def show_auth_dialog():
    
    def on_submit():
        user_id = id_entry.get()
        user_pw = pw_entry.get()

        if user_id == admin_id and user_pw == admin_password:
            auth_window.destroy()
            start_main_app()
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

def start_main_app():
    app = QtWidgets.QApplication(sys.argv)
    Dialog = Ui_Dialog()
    Dialog.show()
    sys.exit(app.exec_())

show_auth_dialog()