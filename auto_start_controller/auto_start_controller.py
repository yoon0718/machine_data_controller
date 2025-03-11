import configparser
import os
import sys
import subprocess


if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable) 
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))  

config_path = os.path.join(current_dir, "auto_start_controller.ini")

if not os.path.exists(config_path):
    print(f"❌ 설정 파일이 없습니다! {current_dir} 위치에 auto_start_controller.ini 파일을 추가하세요.")
    sys.exit(1)

config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")
select_menu = config.get("CONTROLLER", "SELECT")
file_path = config.get("SET", "PATH")
app_name = config.get("SET", "NAME")
delay_time = config.get("SET", "DELAY")


def register_task(app_name, exe_path):
    cmd = f'schtasks /create /tn "{app_name}" /tr "{exe_path}" /sc onlogon /rl highest /f /delay {delay_time}'
    subprocess.run(cmd, shell=True)
    print("🚀 작업 스케줄러에 자동 실행 등록 완료!")

def delete_task(app_name):
    cmd = f'schtasks /delete /tn "{app_name}" /f'
    subprocess.run(cmd, shell=True)
    print("🗑️ 작업 스케줄러에서 삭제 완료!")



def start():

    if select_menu == "0":
        register_task(app_name, file_path)
        print("")
    elif select_menu == "1":
        print("auto_start_controller.ini을 변경해주세요\n0. 자동실행 등록하기  2. 자동실행 삭제하기")
    elif select_menu == "2":
        delete_task(app_name)
    else:
        print("⚠️ 잘못된 값이 입력되었습니다. auto_start_controller.ini 파일을 확인하세요.")
    

start()
