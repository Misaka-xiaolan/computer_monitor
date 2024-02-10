import tkinter as tk
import pystray
from PIL import Image, ImageTk
import os
import serial
import psutil
from time import sleep
from configparser import ConfigParser
from socket import *
import subprocess
import threading


def get_gpu_usage():
    global gpu1
    while True:
        sleep(1)
        try:
            output = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv"],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            gpu1 = "gpu:{:02d}".format(
                int(output.decode("utf-8").split("\n")[1].split(" ")[-2])
            )

        except Exception as e:
            print(f"Error: {e}")


def read_cpu_and_ram():
    global cpu
    global mem
    global cpuPercent
    while True:
        vm = psutil.virtual_memory()
        memoryPercent = vm.percent
        cpuPercent = psutil.cpu_percent(1)
        cpuPercent = int(cpuPercent)
        memoryPercent = int(memoryPercent)
        # print("cpuPercent:" + str(cpuPercent) + " %")
        # print("memory:" + str(memoryPercent) + " %")
        cpu = "cpu:{:02d}".format(cpuPercent)
        mem = "mem:{:02d}".format(memoryPercent)
        # print(cpu)
        # print(mem)


def wireless_send():
    global cpu
    global mem
    global gpu1
    global end
    while True:
        sleep(1)
        try:
            s.connect((IP, int(PORT)))
        except:
            pass
        senddata = cpu + gpu1 + mem + "\r\n"
        try:
            s.send(senddata.encode("gbk"))
        except:
            s = socket(AF_INET, SOCK_STREAM)
        else:
            pass
            # print("发送")


def global_send():
    global cpu
    global gpu1
    global mem
    while True:
        sleep(1)
        # print(cpu)
        # print(mem)
        # print(gpu1)
        try:
            ser = serial.Serial(COM, BAUDRATE, timeout=0.5)
        except:
            pass
            # print("串口丢失")
        else:
            ser.write(cpu.encode("gbk"))
            ser.write(gpu1.encode("gbk"))
            ser.write(mem.encode("gbk"))
            ser.write(bytes.fromhex(end))
            ser.close()


cpu = ""
mem = ""
gpu1 = ""
end = "0D0A"
config = ConfigParser()
config.read("config.ini")
COM = config.get("Serial_Settings", "com")
BAUDRATE = config.get("Serial_Settings", "baudrate")

IP = config.get("Wireless_Settings", "ip")
PORT = config.get("Wireless_Settings", "port")

cpuPercent = 0
psutil.cpu_percent()
s = socket(AF_INET, SOCK_STREAM)

thread1 = threading.Thread(target=read_cpu_and_ram)
thread2 = threading.Thread(target=get_gpu_usage)
thread3 = threading.Thread(target=wireless_send)
thread4 = threading.Thread(target=global_send)

thread1.start()
thread2.start()
thread3.start()
thread4.start()


def exit():
    os._exit(0)


menu = pystray.Menu(pystray.MenuItem("退出", exit))
icon = pystray.Icon("example", Image.open("1.png"), "Example", menu)
icon.run()
