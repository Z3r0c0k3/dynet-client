import platform
import os
import ctypes
import time
import base64
import subprocess
from datetime import datetime

program_title = "dynet_client"
platform_name = platform.system()
platform_ver  = platform.version()
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_wg_installed() -> bool:
    if platform_name == "Windows":
        installed = os.system("wg > NUL 2>&1")
    else:
        installed = os.system("wg > /dev/null 2>&1")
    
    installed = not installed

    return installed

def get_now_ftime(format:str="%Y%m%d%H%M%S") -> str:
    now = datetime.now()
    f_time = now.strftime(format)
    
    return f_time

def delay(micro_sec:int) -> int:
    try:
        micro_sec.sleep(micro_sec)
        return 0
    except:
        return 1

def ques_tf(message="[Y/N] > ") -> bool:
    try:
        input_val = input(message)
    except:
        return False
    
    if input_val == 'Y' or input_val == 'y':
        return True
    else:
        return False

def install_requirements() -> int:
    try:
        subprocess.check_call(["pip", "install", "-r",  os.path.join(current_dir, "requirements.txt")])
        return 0
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        return 2
    except Exception as e:
        print(e)
        return 1

def git_pull():
    try:
        remote_name = "remotedynetclient" + get_now_ftime()
        remote_name = base64.b64encode(remote_name.encode('utf-8'))
        remote_url  = "https://github.com/suzukaotto/dynet-client.git"
        try:
            subprocess.check_call(["git", "remote", "remove", remote_name])
        except:
            pass
        subprocess.check_call(["git", "remote", "add", remote_name, remote_url])
        subprocess.check_call(["git", "pull", remote_name, "main"])
        subprocess.check_call(["git", "remote", "remove", remote_name])

        return 0
    except KeyboardInterrupt:
        print("! KeyboardInterrupt")
        
        return 2
    except Exception as e:
        print("! An error occurred :", e)
        
        return 1

def is_admin() -> bool:
    if platform_name == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    elif platform_name == "Linux" or platform_name == "Darwin":
        return os.geteuid() == 0
    else:
        # ~~
        return False




def pause(message:str="계속하려면 [Enter] 키를 누르십시오 . . . ") -> int:
    print(message, end="")
    try:
        input()
    except:
        return 1

    print(end="\n")
    return 0

def clear() -> int:
    if platform.system() == 'Windows':
        os.system("cls")
    else:
        os.system("clear")

    return 0

def program_exit():    
    clear()
    print("[ 프로그램 종료 ]")
    print("사용 후 연결했거나 저장한 정보를 꼭 제거하세요.")
    print("프로그램이 종료되었습니다.")
    print("")
    pause()
    exit(0)