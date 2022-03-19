# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 13:53:53 2022

@author: Guarmani
"""

from menu_guis import *
import sys 
import subprocess

class MainWindow(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.reset.clicked.connect(self.fn_restart_machine)
        self.session.clicked.connect(self.fn_session_active)
        self.logoff.clicked.connect(self.fn_logoff)
        self.send_file_input.clicked.connect(self.fn_send_file)
        self.tasklist.clicked.connect(self.fn_tasklist)
        self.taskkill.clicked.connect(self.fn_taskkill)
        self.Exit.clicked.connect(self.fn_exit)
    

    def fn_restart_machine(self):
        """ function to reboot remote machine"""
        hostname=self.hostname.displayText()
        commandPing=f"ping -n 2 {hostname}"
        ping=subprocess.Popen(commandPing,stdout=subprocess.PIPE,shell=True)
        self.progressBar.setProperty("value", 25)
        if "recibidos = 2" in str(ping.stdout.read()) or "recibidos = 1" in str(ping.stdout.read()):
            self.progressBar.setProperty("value", 50)
            command=f"powershell shutdown -m {hostname} -r -t 1"
            self.progressBar.setProperty("value", 75)
            subprocess.run(command,shell=True)
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)
        else:
            self.scrollArea.setWidget(QLabel("No se encontro el equipo"))
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)
            
    def fn_session_active (self):
        """ Remote logout function"""
        hostname=self.hostname.displayText()
        commandPing=f"ping -n 2 {hostname}"
        self.progressBar.setProperty("value", 25)
        ping=subprocess.Popen(commandPing,stdout=subprocess.PIPE,shell=True)
        if "recibidos = 2" in str(ping.stdout.read()) or "recibidos = 1" in str(ping.stdout.read()):
            self.progressBar.setProperty("value", 50)
            command=f"query session /server:{hostname}"
            sessions=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
            self.progressBar.setProperty("value", 75)
            text=QLabel(sessions.stdout.read().decode("ANSI"))
            self.scrollArea.setWidget(text)
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)
        else:
            self.scrollArea.setWidget(QLabel("No se encontro el equipo"))
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)
            
    def fn_tasklist(self):
        """Get a list of remote processes"""
        hostname=self.hostname.displayText()
        commandPing=f"ping -n 2 {hostname}"
        ping=subprocess.Popen(commandPing,stdout=subprocess.PIPE,shell=True)
        self.progressBar.setProperty("value", 25)
        if "recibidos = 2" in str(ping.stdout.read()) or "recibidos = 1" in str(ping.stdout.read()):
            self.progressBar.setProperty("value", 50)
            commandList=f"tasklist /s {hostname}"
            output=subprocess.Popen(commandList,stdout=subprocess.PIPE,shell=True)
            self.progressBar.setProperty("value", 75)
            text=QLabel(output.stdout.read().decode("ANSI"))    
            self.scrollArea.setWidget(text)
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)
        else:
            self.scrollArea.setWidget(QLabel("No se encontro el equipo"))
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)

    def fn_taskkill(self):
        """kill remote process"""
        hostname=self.hostname.displayText()
        pid=self.taskkill_pid.displayText()
        self.progressBar.setProperty("value", 25)
        commandPing=f"ping -n 2 {hostname}"
        self.progressBar.setProperty("value", 50)
        ping=subprocess.Popen(commandPing,stdout=subprocess.PIPE,shell=True)
        if "recibidos = 2" in str(ping.stdout.read()) or "recibidos = 1" in str(ping.stdout.read()):
            self.progressBar.setProperty("value", 75)
            commandKill=f"taskkill /s {hostname} /PID {pid}"
            subprocess.run(commandKill,shell=True)
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)
        else:
            self.scrollArea.setWidget(QLabel("No se encontro el equipo"))
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)
    
    def fn_logoff(self):
        """ Remote logout function"""
        hostname=self.hostname.displayText()
        session=self.id_session.displayText()
        commandPing=f"ping -n 2 {hostname}"
        ping=subprocess.Popen(commandPing,stdout=subprocess.PIPE,shell=True)
        self.progressBar.setProperty("value", 25)
        if "recibidos = 2" in str(ping.stdout.read()) or "recibidos = 1" in str(ping.stdout.read()):
            self.progressBar.setProperty("value", 50)
            command=f"logoff {session} /server:{hostname}"
            subprocess.run(command,shell=True)
            self.progressBar.setProperty("value", 75)
            command=f"query session /server:{hostname}"
            sessions=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
            self.progressBar.setProperty("value", 75)
            text=sessions.stdout.read().decode("ANSI")
            self.scrollArea.setWidget(QLabel(text))
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)
        else:
            self.scrollArea.setWidget(QLabel("No se encontro el equipo"))
            self.progressBar.setProperty("value", 100)
            self.progressBar.setProperty("value", 0)

    def fn_send_file(self):
        """Send files to remote machine"""
        filename, _ =QFileDialog.getOpenFileNames(self,"open file", "","All files (*)")
        filecount=len(filename)
        hostname=self.hostname.displayText()
        self.route_label.setText(str(f"Se han cargado {filecount} archivos"))
        commandDir=f"dir \\\\{hostname}\\d$"
        partition=subprocess.Popen(commandDir ,stderr=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
        self.progressBar.setProperty("value", 25)
        if partition.stderr.read().decode("ANSI") =="":
            commandCreate=f"mkdir \\\\{hostname}\\d$\\Delivery"
            folder=subprocess.Popen(commandCreate ,stderr=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
            self.progressBar.setProperty("value", 50)
            if folder.stderr.read().decode("ANSI") =="":
                subprocess.run(commandCreate,shell=True)
                for i in filename:
                    i=str(i).replace("/","\\")
                    self.progressBar.setProperty("value", 75)
                    commandCopy=f"copy {i} \\\\{hostname}\\d$\\Delivery"
                    subprocess.run(commandCopy,shell=True)
                    self.progressBar.setProperty("value", 100)
                self.scrollArea.setWidget(QLabel("Transferencia exitosa"))
                self.progressBar.setProperty("value", 0)
            else:
                for i in filename:
                    i=str(i).replace("/","\\")
                    self.progressBar.setProperty("value", 75)
                    commandCopy=f"copy {i} \\\\{hostname}\\d$\\Delivery"
                    subprocess.run(commandCopy,shell=True)
                    self.progressBar.setProperty("value", 100)
                self.scrollArea.setWidget(QLabel("Transferencia exitosa"))
                self.progressBar.setProperty("value", 0)
        else:
            commandDir=f"dir \\\\{hostname}\\c$"
            partition=subprocess.Popen(commandDir ,stderr=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
            self.progressBar.setProperty("value", 50)
            if partition.stderr.read().decode("ANSI") =="":
                commandCreate=f"mkdir \\\\{hostname}\\c$\\Delivery"
                subprocess.run(commandCreate,shell=True)
                for i in filename:
                    self.progressBar.setProperty("value", 75)
                    i=str(i).replace("/","\\")
                    commandCopy=f"copy {i} \\\\{hostname}\\c$\\Delivery"
                    print(commandCopy)
                    subprocess.run(commandCopy,shell=True)
                    self.progressBar.setProperty("value", 100)
                self.scrollArea.setWidget(QLabel("Transferencia exitosa"))
                self.progressBar.setProperty("value", 0)
            else:
                self.scrollArea.setWidget(QLabel("Transferencia exitosa"))
                self.progressBar.setProperty("value", 100)
                self.progressBar.setProperty("value", 0)
    
    def fn_exit(selg):
        sys.exit()
        
if __name__ == "__main__":
    app = QApplication()
    w = MainWindow()
    w.show()
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    sys.exit(app.exec_())