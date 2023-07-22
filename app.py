import ctypes
import time
import threading
import psutil
from tkinter import Tk, Label, Entry, Button, StringVar

# 윈도우 알림 함수
def message_box(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 1)

# 배터리 상태 확인 함수
def check_battery():
    while True:
        battery = psutil.sensors_battery()
        percent = battery.percent

        if percent > float(max_battery.get()) or percent < float(min_battery.get()):
            message_box("경고", f"배터리 상태가 설정된 범위를 벗어났습니다. 현재 배터리: {percent}%")

        time.sleep(int(alert_interval.get()) * 60)

# 설정 파일 읽기 함수
def read_settings():
    try:
        with open("settings.txt", "r") as file:
            max_battery.set(file.readline().strip())
            min_battery.set(file.readline().strip())
            alert_interval.set(file.readline().strip())
    except FileNotFoundError:
        pass  # 파일이 없으면 아무것도 하지 않음

# 설정 파일 쓰기 함수
def write_settings():
    with open("settings.txt", "w") as file:
        file.write(max_battery.get() + "\n")
        file.write(min_battery.get() + "\n")
        file.write(alert_interval.get() + "\n")

# 배터리 체크 스레드 실행 함수
def start_check_battery_thread():
    global check_battery_thread

    if check_battery_thread is None or not check_battery_thread.is_alive():  # 스레드가 없거나 종료된 경우에만 새로운 스레드 생성
        check_battery_thread = threading.Thread(target=check_battery)
        check_battery_thread.start()

# Tkinter GUI
root = Tk()
root.title("배터리 알림 설정")

Label(root, text="최대 배터리 (%)").grid(row=0, column=0)
Label(root, text="최소 배터리 (%)").grid(row=1, column=0)
Label(root, text="알림 주기 (분)").grid(row=2, column=0)

max_battery = StringVar()
min_battery = StringVar()
alert_interval = StringVar()

Entry(root, textvariable=max_battery).grid(row=0, column=1)
Entry(root, textvariable=min_battery).grid(row=1, column=1)
Entry(root, textvariable=alert_interval).grid(row=2, column=1)

Button(root, text="설정 저장", command=lambda: [write_settings(), start_check_battery_thread()]).grid(row=3, column=0, columnspan=2)

check_battery_thread = None
read_settings()  # 프로그램 시작 시 저장된 설정 읽기

root.mainloop()
