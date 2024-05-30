# -*- coding: UTF-8 -*-
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtCore import  *
import serial.tools.list_ports
import os
import argparse
import serial
from Gui.ui_MainWindow import *
from Gui.ui_BreakPointDialog import *
from Gui.ui_PortSelect import *
from Logic.BreakPointDialog import *
from Logic.PortSent import *
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
serial_is_open = False
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    sign_one = pyqtSignal(str)
    trigger_PortSent = pyqtSignal()
    ScrollBar_RAM = pyqtSignal(int)
    global hexfile_dir
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.CreateItems()
        self.CreateSignalSlot()
    def CreateSignalSlot(self):
        self.actionOpen_Port.triggered.connect(self.PortSent_show)
        self.actionUpdateregister.triggered.connect(self.get_register)
        self.actionOpen.triggered.connect(self.PortSelect.send_from_hex_file)
        self.actionRun.triggered.connect(self.PortSelect.run_code)
        self.actionLoad.triggered.connect(self.get_lst)
       # self.actionLoad.triggered.connect(self.upload)
        self.actionStep_Run.triggered.connect(self.PortSelect.run_step_code)
        self.actionStep_Function_Run.triggered.connect(self.PortSelect.run_step_function_code)
        self.actionUpdate_RAM.triggered.connect(self.get_RAM)
        self.actionUpdate_Port.triggered.connect(self.get_IO)
        self.actionMake_BreakPoint.triggered.connect(self.BreakPointDialog_show)
        self.actionMake_BreakPoint.triggered.connect(self.BreakPoint.read_BreakPoints)
        self.actionClean_All_Break_Point.triggered.connect(self.clean_all_break_point)
        # Breakpoint model signal connect
        self.PortSelect.text_receive_register.connect(self.set_register)
        self.PortSelect.text_receive_RAM.connect(self.set_RAM)
        self.PortSelect.text_receive_IO.connect(self.set_IO)
        self.verticalScrollBar_RAM.sliderReleased.connect(self.get_ScrollBar)
        self.ScrollBar_RAM.connect(self.PortSelect.get_RAM)
        self.PortSelect.text_receive_Breakpoint.connect(self.BreakPoint.set_BreakPoints_text)
        #Breakpoint model signal connect
        self.BreakPoint.BP_signal.connect(self.PortSelect.Set_Breakpoint)
        self.BreakPoint.BP_startread_signal.connect(self.PortSelect.Read_Breakpoint)

    def CreateItems(self):
        self.PortSelect = PortSelectDialog()
        self.BreakPoint = BreakPointDialog()
    def PortSent_show(self):
        # 创建子窗口实例
        self.PortSelect.show()
        # dialog.stop_thread.connect(thread.stop)
        # self.thread.start()
        #PortSelect = PortSelectDialog()
        # 将信号连接到子窗口的槽函数
        # 显示子窗口
        self.PortSelect.exec_()
        # 发出信号，触发子窗口的槽函数
        #ps.closeEvent()
    def BreakPointDialog_show(self):
        #bk = BreakPointDialog()
        self.BreakPoint.show()
    def get_IO(self):
        s = self.PortSelect.get_IO()
        if s == "":
            QMessageBox.warning(self, "Warning", "Could not get all ports. Please check the connection.")
            return
        elif s != "":
            # s = "P0=1111111\r\nP1=1111111\r\nP2=1111111\r\nP3=1111111\r\nP4=1111111\r\nP5=1111111\r\n"
            if len(s) == 0 or s[-1] != "#":
                QMessageBox.warning(self, "Warning", "Could not get all ports. Please check the connection.")
            else:
                # self.set_register(self.s)
                return
        time.sleep(0.1)
    def get_lst(self):
        s, _ = QFileDialog.getOpenFileName(None, 'Open a lst file', 'D:\\', 'lst files (*.lst)')
        global lstfile_dir
        lstfile_dir = s
        with open(lstfile_dir, 'r') as f:
            lst_content = f.read()
        #pattern = re.compile(r'^(\s*[\w\$]+:)?\s*([^\r\n;]*)', re.MULTILINE)

        address_pattern = re.compile(r'\s+\d+/(.+?);', re.MULTILINE)

        # 提取地址和内容
        addresses = address_pattern.findall(lst_content)
        # 输出匹配结果
        lines = addresses
        address_lines = {}

        # 遍历每一行
        for line in lines:
            parts = line.split(':')
            address = parts[0].strip()  # 获取地址部分
            content = parts[1].strip() if len(parts) > 1 else ''  # 获取内容部分（如果有）
            address_lines[address] = content  # 更新字典

        # 输出结果
        for address, content in address_lines.items():
            address=address.zfill(4) #补全4位十六进制
            memory=address+' : '+content
            self.listWidget_ASM.addItem(memory)

        if lstfile_dir == None:
            print("> > > Successful: File '{}' is not found".format(lstfile_dir))
        else:
            print("Successful: File '{}' is open".format(lstfile_dir))
        return lstfile_dir
    def set_IO(self, message):
        #s=message.split("\r\n#dd")
        pattern= re.compile(r'D:(.+?)\r\n#')
        c=pattern.findall(message)
        i = 0
        P = ['P0=', 'P1=', 'P2=', 'P3=', 'P4=', 'P5=']
        d = ''
        e = '\r\n'
        '''
        D:80: BD
        #dd80 80
        D:90: FE 
        #dd90 90
        D:A0: 7E
        #dda0 a0
        D:B0: FD
        #ddb0 b0
        D:E8: FF
        #dde8 e8
        D:F8: 3F
        #ddf8 f8
        #di0 4f
        '''
        for line in c:
            #print(line)
            line = line.split()
            line_list = list(line)
            line_list[0]=P[i]
            i=i+1
            line_list_1_bin=bin(int(line_list[1],16))
            line_list_1_bin=line_list_1_bin.lstrip('0b')
            line_list[1]='{:0>8}'.format(line_list_1_bin)
            line = ''.join(line_list)
            d = d+line+e
        print(d)
        self.label_Port.setText(d)
        return d
    def get_register(self):
        s=self.PortSelect.get_register()
        if s == "":
            QMessageBox.warning(self,"Warning","Could not get all register. Please check the connection.")
            return
        elif s !="":
            #s = "RA RB R0 R1 R2 R3 R4 R5 R6 R7 PSW DPTR SP PC<\r><\n>FF FF FF FF FF FF FF FF FF FF ---R0--- 0000 07 0000 <\r><\n>"
            if len(s) == 0 or s[-1] != "#":
                QMessageBox.warning(self,"Warning","Could not get all register. Please check the connection.")
            else:
                #self.set_register(self.s)
                return
        time.sleep(0.1)
    def set_register(self, message):
        # message=self.PortSelect.text_receive
        message = message[:-1]#去掉#
        message = message[3:]#去掉X\r\n
        message.replace('\r', '')
        self.label_Reg.setText(message)
        return message
    #def register_value= a
    #return register_value
    def clean_all_break_point(self):
            print("> Starting make breakpoint... ")
            self.comSend(message="BK ALL\r")
            #s = PortSelectDialog.(expected="#".encode("utf-8")).decode("utf-8")
            #if len(s) == 0 or s[-1] != "#":
                #raise Exception("Could not make breakpoint. Please reset and try again.")

    def get_ScrollBar(self):
        s = self.verticalScrollBar_RAM.sliderPosition() #获取进度条信息
        self.ScrollBar_RAM.emit(s)
    def get_RAM(self):
        s = self.PortSelect.get_RAM()
        if s == "":
            QMessageBox.warning(self,"Warning","Could not get all register. Please check the connection.")
            return
        elif s !="":
            if len(s) == 0 or s[-1] != "#":
                QMessageBox.warning(self,"Warning","Could not get all register. Please check the connection.")
            else:
                #self.set_register(self.s)
                return
        time.sleep(0.1)
    def set_RAM(self,message):
        s = message[:-1]
        '''
        s =(
C:0000: 01 00 03 75 E8 FE 78 14 11 13 D8 FC E5 E8 23 F5
C:0010: 02 00 03 75 E8 FE 78 14 11 13 D8 FC E5 E8 23 F5
C:0020: 03 00 03 75 E8 FE 78 14 11 13 D8 FC E5 E8 23 F5
C:0030: 04 00 03 75 E8 FE 78 14 11 13 D8 FC E5 E8 23 F5
C:0040: 05 00 03 75 E8 FE 78 14 11 13 D8 FC E5 E8 23 F5
C:0050: 06 00 03 75 E8 FE 78 14 11 13 D8 FC E5 E8 23 F5
C:0060: 07 00 03 75 E8 FE 78 14 11 13 D8 FC E5 E8 23 F5
C:0070: 08 00 03 75 E8 FE 78 14 11 13 D8 FC E5 E8 23 F5
C:0080: E9 80 F3 C0 01 C0 00 79 C1 78 80 D8 FE D9 FA D0
C:0090: 10 D0 01 22 00 00 00 00 00 00 00 00 00 00 00 00
C:00A0: 11 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
C:00B0: 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
C:00C0: 13 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
C:00D0: 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
C:00E0: 15 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
C:00F0: 16 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
C:0110: 17 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
C:0120: 18 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
#
        )
        '''
        s = s.replace('C:','') #去掉C
        bar = '-' #添加分隔符
        star = '|'
        c=str.splitlines(s) #把数列列表分割成字符串
        c=c[1:]#去掉指令部分
        d = ''
        e = '\r\n'
        for line in c:
            #print(line)
            line = line.split() #分割字符串成单个字节
            line_list = list(line)
            ascii_list = [chr(int(hex_str, 16)) for hex_str in line_list[1:]]
            line_list.insert(9,bar) #添加分隔符
            line_hex = ' '.join(line_list)
            line_ascii = ''.join(ascii_list)
            d = d+line_hex+' '+star+line_ascii+star+e
            #print(d)
        print(d)
        print(ascii_list)
        self.label_RAM.setText(d)
        return s

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
