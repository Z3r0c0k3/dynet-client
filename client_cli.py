import os
import sys
import time
import base64
import subprocess
from getpass import getpass
from ast import literal_eval
import pyautogui
import requests
import requests

from func import *
from image2ascii.image2ascii import image2ascii

saved_paths = []

def connect(id, pw):
    url = 'http://vpn.internal.dyhs.kr/signin'
    request = {
        'id': id,
        'password': pw
    }

    print("연결 중 . . . ")
    try:
        response = requests.post(url, json=request)
        response_data = response.json()
        response_msg = response_data['message']
    except KeyboardInterrupt:
        return 5
    except Exception as e:
        print(e)
        return 2


    if response_msg != "Success":
        if response_msg == "Password not matched" or response_msg == "User not found":
            return 1
        # elif ~~
    print("연결 성공")
    print("")

    peer = response_data['peer']
    peer = base64.b64decode(peer)
    peer = peer.decode('utf-8')
    peer = literal_eval(peer)

    p_private_key   = peer['privateKey']
    p_address       = peer['address']
    p_public_key    = peer['publicKey']
    p_preshared_key = peer['presharedKey']
    p_endpoint      = peer['endpoint']
    p_allowed_ip    = peer['allowedIPs']
    p_dns           = peer['dns']

    config = ""
    config +=  "[Interface]\n"
    config += f"PrivateKey = {p_private_key}\n"
    config += f"Address = {p_address}\n"
    config += f"DNS = {p_dns}\n"
    config +=  "\n"
    config +=  "[Peer]\n"
    config += f"PublicKey = {p_public_key}\n"
    config += f"PresharedKey = {p_preshared_key}\n"
    config += f"AllowedIPs = {p_allowed_ip}\n"
    config += f"Endpoint = {p_endpoint}"

    if platform_name == 'Windows':
        save_path = r"C:\Program Files\WireGuard\Data\Configurations"
        save_name = f"{id}_{get_now_ftime()}.conf"
        last_save_path = None
        is_wg_save = False

        # config save
        print("WireGuard에 저장 중 . . . ")
        try:
            with open(f"{save_path}\{save_name}", "w") as file:
                file.write(config)
                last_save_path = f"{save_path}\{save_name}"
                is_wg_save = True
        except PermissionError:
            print("! 권한이 부족해 WireGuard에 저장하지 못했습니다.")
            print("  관리자 권한으로 실행 후 다시 시도하세요.")
            pass
        except Exception as e:
            print(e)
            print("! 에러가 발생해 정보를 추가하지 못했습니다.")
            pass

        # statu print
        if last_save_path != None:
            saved_paths.append(last_save_path)

            os.system("wireguard")
            print("VPN 접속 피어를 WireGuard에 저장했습니다.")
            print(f'File      "{last_save_path}"')
            print(f'File Name "{save_name}"')
            print("저장된 피어를 연결할 수 있습니다.")
            print("")
            print("! 사용 후 연결했거나 저장한 정보를 꼭 제거하세요(WireGuard 하단 X표시).")
            print("! 첫 로그인 시 반드시 비밀번호를 변경해주세요.")
            print("")

        else:
            print("정보가 저장되지 않았습니다.")
            print("")
        
        pause()

        return 0

    else:
        print("WireGuard 실행을 위해 관리자 권한(sudo 권한)이 필요합니다.")
        shell_pw = getpass("컴퓨터의 패스워드를 입력하세요(입력 시 보이지 않음): ")
        print("# 연결이 곧 시작됩니다. 더이상 프로그램을 조작하지 마세요.")
        time.sleep(3)

        with open(f"DY-NET_{id}.conf", "w") as f:
            f.write(config)

        os.system(f"sudo wg-quick up {os.getcwd()}/DY-NET_{id}.conf")
        pyautogui.typewrite(f"{shell_pw}\n", interval=0.01)
        time.sleep(3)
        clear()

def wg_install() -> int:
    if platform_name == "Windows":
        url = "https://download.wireguard.com/windows-client/wireguard-installer.exe"
        save_path = "./wg-installer.exe"

        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            downloaded = 0

            file = open(save_path, 'wb')
            for data in response.iter_content(block_size):
                downloaded += len(data)
                file.write(data)
                progress = downloaded / total_size * 100
                print(f"다운로드 진행률: {progress:.2f}%", end='\r')
            print("\n다운로드 완료")

            # line break
            print("")

            print("설치 중 . . . ")
            file.close()
            os.system("wg-installer.exe")
            os.remove(save_path)
            os.environ['PATH'] += os.pathsep + r"C:\Program Files\WireGuard"
            print("설치 완료")
            return 0
        except KeyboardInterrupt:
            return 5
        except Exception as e:
            print(e)
            return 1
    else:
        print("Windows 이외의 운영체제에선 아직 지원하지 않습니다.")
        return 1
        # ~~

def disconnect(id):
    clear()
    print("WireGuard 실행을 위해 관리자 권한(sudo 권한)이 필요합니다.")
    time.sleep(1)
    shell_pw = getpass("컴퓨터의 패스워드를 입력하세요(입력 시 보이지 않음): ")
    os.system(f"sudo wg-quick down {os.getcwd()}/DY-NET_{id}.conf")
    pyautogui.typewrite(f"{shell_pw}\n", interval=0.01)
    time.sleep(2)
    os.system(f"sudo rm DY-NET_{id}.conf")
    clear()
    print("모든 동작이 완료되었습니다. 프로그램을 종료합니다.")
    time.sleep(2)
    exit()

def change_password(id, pw, change_pw):
    url = 'http://vpn.internal.dyhs.kr/password-change'
    request = {
        'id': id,
        'password': pw,
        'newPassword': change_pw
    }

    print("비밀번호 변경 중 . . . ")
    try:
        response = requests.post(url, json=request)
        response_data = response.json()
        response_msg = response_data['message']
    except KeyboardInterrupt:
        return 5
    except Exception as e:
        print(e)
        return 2

    if response_msg != "Success":
        if response_msg == "Password not matched" or response_msg == "User not found":
            return 1
        elif response_msg == "Password is same":
            return 3
        else:
            print(response_msg)
            return 2
    print("비밀번호 변경 완료")
        
    print("")
    print("비밀번호가 변경되었습니다.")
    print(f"변경된 비밀번호 [{change_pw}]")
    print("변경한 비밀번호를 꼭 기억하세요.")
    print("")
    pause()

    return 0
        

alert_msg = None
def main():
    global alert_msg

    clear()
    # print dyhs logo
    try:
        logo_path = os.path.join(current_dir, r"src/logo.png")
        if platform_name == "Windows":
            print(image2ascii(logo_path, 30, 15, ascii_chars="# "))
        else:
            print(image2ascii(logo_path, 30, 20, ascii_chars="# "))
    except:
        pass
    print(f"============ [{program_title}] ============")
    print(f"{platform_name} {platform_ver}")
    # wireguard install check
    wireguard_installed = get_wg_installed()

    # message print
    if wireguard_installed == True:
        os.system("wg --version")
    else:
        print("WireGuard가 설치되어있지 않습니다. [설치: 0번]")
    
    # admin check
    if is_admin() == False:
        print("현재 관리자 권한이 아닙니다.")

    print(f"========================================")
    if is_admin() == False:
        if platform_name == "Windows":
            print("관리자 권한으로 다시 실행합니다(Windows) . . . ")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
        # ~~~

    if alert_msg != None: print(f"\n! {alert_msg}", end="\n\n"); alert_msg = None
    print("1. 도움말                  ")
    print("2. 외부망 연결             ")
    print("3. 연결 해제 (Linux 전용) ")
    print("4. 비밀번호 변경           ")
    print("5. 나가기                  ")
    
    # menu select
    try:
        sel_menu = input("> ")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        print()
        program_exit()
        return 1
    print("") # line brake

    # menu 0
    if sel_menu == '0':
        clear()
        print("[ WireGuard 설치 페이지 ]")

        # wireguard install check
        if get_wg_installed() == True:
            print("WireGuard가 이미 설치되어있습니다.")
            print("")
            pause()
            return 1

        if ques_tf("WireGuard를 설치하시겠습니까? [Y/N]: ") == False:
            alert_msg = "WireGuard 설치를 취소했습니다."
            return 1
        
        print()
        wg_install_rst = wg_install()
        print()

        if wg_install_rst == 0:
            print("WireGuard가 성공적으로 설치되었습니다.")
        elif wg_install_rst == 1:
            print("! 설치에 실패했습니다.")
        elif wg_install_rst == 4:
            print("! 인터넷 연결을 확인하세요.")
        elif wg_install_rst == 5:
            print("! 설치가 취소되었습니다.")

        print()
        pause()

        return 0
        
    # menu 1
    if sel_menu == '1':
        clear()
        print("[ 도움말 페이지 ]")
        print("- 위 프로그램은 덕영고등학교 학생용 가상사설망(VPN) 클라이언트 입니다.")
        print("- 프로그램을 사용하기 위해서 관리자에게 계정생성을 요청해야 합니다.")
        print("- 자세한 사항은 링크를 참고해주세요. (https://zerocoke.gitbook.io/dy-net/)")
        print("")
        pause()
        
        return 0
    
    # menu 2
    elif sel_menu == '2':
        clear()
        print("[ 외부망 접속 페이지 ]")
        if get_wg_installed() == False:
            print("WireGuard가 설치되어있지 않습니다.")
            print("0번 메뉴로 WireGuard를 설치할 수 있습니다.")
            print("")

            pause()
            return 1
        while True:
            try:
                id = input("아 이 디: ")
                pw = getpass("비밀번호: ")
            except:
                alert_msg = "외부망 연결을 취소했습니다."
                return 1
            
            print()
            connect_rst = connect(id, pw)
            print()
            if connect_rst == 0:
                return 0
            elif connect_rst == 1:
                print("! 아이디 또는 비밀번호가 틀렸습니다.", end=" ")
            elif connect_rst == 2:
                print("! 알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도하세요.", end=" ")
            elif connect_rst == 3:
                return 1
            elif connect_rst == 4:
                print("! 인터넷 연결을 확인하세요.")
                print()

                pause()
                return 1
            elif connect_rst == 5:
                print("! 외부말 연결을 취소했습니다.")
                print()

                pause()
                return 1
                
            print("[나가기: Ctrl+C]", end="\n\n")
        
    # menu 3
    elif sel_menu == '3':
        clear()
        print("[ 연결 해제 페이지 ]")

        if platform_name == 'Windows':
            print("현재 운영체제에선 지원하지 않는 기능입니다.")
            print()
            pause()
            return 1

        try:
            id = input("아이디를 입력해주세요: ")
        except:
            alert_msg = "연결 해제를 취소했습니다."
            return 1
        
        disconnect(id)

        return 0

    # menu 4
    elif sel_menu == '4':
        clear()
        print("[ 비밀번호 변경 페이지 ]")
        while True:
            try:
                id        = input("아 이 디: ")
                pw        = getpass("비밀번호: ")
                change_pw = getpass("변경할 비밀번호를 입력해주세요: ")
            except:
                alert_msg = "비밀번호 변경을 취소했습니다."
                return 1
            
            print("")
            change_pw_rst = change_password(id, pw, change_pw)
            print("")
            if change_pw_rst == 0:
                return 0
            elif change_pw_rst == 1:
                print("! 아이디 또는 비밀번호가 틀렸습니다.", end=" ")
            elif change_pw_rst == 2:
                print("! 알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도하세요.", end=" ")
            elif change_pw_rst == 3:
                print("! 변경할 비밀번호가 기존 비밀번호와 같습니다.")
                print("")
                alert_msg = "비밀번호가 변경되지 않았습니다."

                pause()
                return 1
            elif change_pw_rst == 4:
                print("! 인터넷 연결을 확인하세요.")
                print()
                
                pause()
                return 1
            elif change_pw_rst == 5:
                print("! 비밀번호 변경이 취소되었습니다.")
                print("")

                pause()
                return 1
            print("[나가기: Crtl+C]", end="\n\n")
    
    # menu 5
    elif sel_menu == '5':
        program_exit()
    
    return 1

if __name__ == '__main__':
    while True:
        main()