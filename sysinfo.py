import tkinter as tk
import sys
import platform
import winreg
import subprocess

set11Flag = 0;

def getWindowsVersion():
    path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path)
    try:
        productName = winreg.QueryValueEx(key,"ProductName")[0]
        build = int(winreg.QueryValueEx(key,"CurrentBuildNumber")[0])
    finally:
        winreg.CloseKey(key)

    if build >= 22000: #check for win 11 
        productName = productName.replace("Windows 10","Windows 11")
        global set11Flag 
        set11Flag = 1

    return productName


def quitApp():
    sys.exit(0)

def showInfo(window,name: str,info:str,row:int,column:int):
    label = tk.Label(window, text=name)
    label.grid(row=row,column=column)
    labelInfo = tk.Label(window, text=info)
    # Here Row will be same, but the column will be the next column of the given one
    labelInfo.grid(row=row,column=column+1)

def getGpu():
    result = subprocess.run([
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-CimInstance Win32_VideoController).Name"
        ],
        capture_output = True,
        text = True,
        check = True
    )

    gpus = [
            gpu.strip()
            for gpu in result.stdout.splitlines()
            if gpu.strip()
    ]

    return ", ".join(gpus) if gpus else "Unknown"


window = tk.Tk()
window.title("Sysinfo - View System Information")
window.geometry("400x350")

showInfo(window,"Operating System :",getWindowsVersion(),0,0)
if set11Flag == 0:
    showInfo(window,"Version : ",platform.release(),1,0)
else:
    showInfo(window,"Version :","11",1,0)
showInfo(window,"Processor : ",platform.processor(),2,0)
showInfo(window,"GPU : ",getGpu(),3,0)
showInfo(window, "System:", platform.system(), 4, 0)
showInfo(window, "Release:", platform.release(), 5, 0)
showInfo(window, "System Version:", platform.version(), 6, 0)
showInfo(window, "Machine:", platform.machine(), 7, 0)
showInfo(window, "Architecture:", platform.architecture()[0], 8, 0)
showInfo(window, "Hostname:", platform.node(), 9, 0)
showInfo(window, "Python Version:", platform.python_version(), 10, 0)
showInfo(window, "Python Type:", platform.python_implementation(), 11, 0)

button = tk.Button(window,text = "Quit",command = quitApp,padx=20,pady=10)
button.grid(row=12,column=1,padx=10,pady=10)

footer = tk.Frame(window)
footer.grid(row=13,column=0,columnspan=2,sticky="ew",padx=10,pady=5)
footerLabel = tk.Label(footer,text="made by SHEN with love. (https://github.com/khuman-shen)",fg="gray")
footerLabel.pack()

window.mainloop()

