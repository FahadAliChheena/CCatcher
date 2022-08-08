# -*- coding: utf-8 -*-

# Author: Fahad Ali
# Date:   08/03/2022
# Name:   CCatcher

from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys, os
from PyQt5.QtWidgets import QMessageBox, QCheckBox
from PyQt5.Qt import QApplication
from functions import getEmails, setTrayIconBackgroundWindow as setAppOnTray, MessageBox, emailChecker, urlChecker, geturl
from about import Ui_Dialog

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ccatcher.ui', self)
        self.setFixedSize(400, 300)
        self.current_user = os.getlogin()
        exists = os.path.isdir(rf"C:\Users\{self.current_user}\Documents\CCatcher")
        if not exists:
            os.mkdir(rf"C:\Users\{self.current_user}\Documents\CCatcher")
        exists = os.path.isdir(rf"C:\Users\{self.current_user}\Documents\CCatcher\Settings")
        if not exists:
            os.mkdir(rf"C:\Users\{self.current_user}\Documents\CCatcher\Settings")
        QApplication.clipboard().dataChanged.connect(self.getClipboardData)
        # File Menu
        self.actionNew.triggered.connect(self.newClipboard)
        self.actionEmail_Extractor.triggered.connect(self.emailExtractor)
        self.actionURL_Extractor.triggered.connect(self.urlExtractor)
        self.actionExit.triggered.connect(self.close)
        # History Menu
        self.actionCheck_History.triggered.connect(self.checkHistory)
        self.actionClear_History.triggered.connect(self.clearHistory)
        # Help Menu
        self.actionAbout.triggered.connect(self.about)
        
    def getClipboardData(self):
        text = QApplication.clipboard().text()
        saved = set()
        exists = os.path.isfile(rf"C:\Users\{self.current_user}\Documents\CCatcher\history.list")
        if exists:
            f = open(rf"C:\Users\{self.current_user}\Documents\CCatcher\history.list", 'r+')
            for data in f.readlines():
                saved.add(data.strip())
        else:
            f =open(rf"C:\Users\{self.current_user}\Documents\CCatcher\history.list", 'w')
        if (len(text.split('\n')) == 1) and (not text.strip() in saved):
            if (emailChecker(text.strip())) or (urlChecker(text.strip())):
                self.plainTextEdit.insertPlainText(text.strip()+'\n')
                f.write(text.strip() +'\n')
        else:
            for line in text.split('\n'):
                if (not line.strip() in saved) and (not line.strip() in self.plainTextEdit.toPlainText()):
                    if (emailChecker(line.strip())) or (urlChecker(line.strip())):
                        self.plainTextEdit.insertPlainText(line.strip()+'\n')
                        f.write(line.strip()+'\n')
        f.close()
        
    def checkHistory(self):
        self.plainTextEdit.clear()
        exists = os.path.isfile(rf"C:\Users\{self.current_user}\Documents\CCatcher\history.list")
        if exists:
            f = open(rf"C:\Users\{self.current_user}\Documents\CCatcher\history.list", 'r')
            for data in f.readlines():
                self.plainTextEdit.appendPlainText(data.strip())
            f.close()
        else:
            MessageBox(QMessageBox.Warning, "icons/error.ico", "History is empty.")
            
    def clearHistory(self):
        exists = os.path.isfile(rf"C:\Users\{self.current_user}\Documents\CCatcher\history.list")
        self.plainTextEdit.clear()
        if exists:
            os.remove(rf"C:\Users\{self.current_user}\Documents\CCatcher\history.list")
            MessageBox(QMessageBox.Information, "icons/about.png" , "History is cleared.", "Information")
        else:
            MessageBox(QMessageBox.Information, "icons/about.png" , "History is already empty.", "Information")
            
    def newClipboard(self):
        self.plainTextEdit.clear()
        
    def emailExtractor(self):
        text = self.plainTextEdit.toPlainText()
        got_emails = getEmails(text.strip( ' \r\n'))
        if not got_emails == set():
            try:
                fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', rf"C:\Users\{self.current_user}\Documents\CCatcher", "Text files (*.txt)")
                f = open(fname[0], 'w')
                for email in got_emails:
                    f.write(email+'\n')
                f.close()
            except FileNotFoundError:
                f = open(rf"C:\Users\{self.current_user}\Documents\CCatcher\emails.txt", 'w')
                for email in got_emails:
                    f.write(email+'\n')
                f.close()
            MessageBox(QMessageBox.Information, "icons/about.png" , "Emails extracted successfully!", "Successful")
        else:
            MessageBox(QMessageBox.Information, "icons/about.png" , "No email is found.", "Information")
            
    def urlExtractor(self):
        text = self.plainTextEdit.toPlainText()
        got_urls = geturl(text.strip( ' \r\n'))
        if not got_urls == set():
            try:
                fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', rf"C:\Users\{self.current_user}\Documents\CCatcher", "Text files (*.txt)")
                f = open(fname[0], 'w')
                for url in got_urls:
                    for link in url:
                        if urlChecker(link):
                            f.write(link+'\n')
                f.close()
            except FileNotFoundError:
                f = open(rf"C:\Users\{self.current_user}\Documents\CCatcher\emails.txt", 'w')
                for url in got_urls:
                    for link in url:
                        if urlChecker(link):
                            f.write(link+'\n')
                f.close()
            MessageBox(QMessageBox.Information, "icons/about.png" , "URLs extracted successfully!", "Successful")
        else:
            MessageBox(QMessageBox.Information, "icons/about.png" , "No URL is found.", "Information")
            
    def about(self):
        self.about = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.about)
        #self.searchWindow.setParent(window)
        self.about.show()
        
    def closeEvent(self, event):
        self.hide()
        exists = os.path.isfile(rf"C:\Users\{self.current_user}\Documents\CCatcher\Settings\check.con")
        read = False
        data = []
        if exists:
            f = open(rf"C:\Users\{self.current_user}\Documents\CCatcher\Settings\check.con", 'r')
            for line in f.readlines():
                data.append(line.strip())
            f.close()
        if len(data) != 0:
            if data[-1] == "Checked":
                read = True
        text = ("1) Application is running in the background\n2)To close it go to the window tray icon\n3) Right click on icon\n4) Click on exit.")
        if read == False:
            Message = QMessageBox()
            check = QCheckBox("Don't show this message again.")
            check.stateChanged.connect(self.clickBox)
            Message.setCheckBox(check)
            Message.setText(text)
            Message.setWindowTitle("Information")
            Message.setIcon(QMessageBox.Information)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            Message.setWindowIcon(icon)
            Message.show()
            Message.exec_()
        
    def clickBox(self, state):
        exists = os.path.isfile(rf"C:\Users\{self.current_user}\Documents\CCatcher\Settings\check.con")
        if exists:
            f = open(rf"C:\Users\{self.current_user}\Documents\CCatcher\Settings\check.con", 'a')
        else:
            f = open(rf"C:\Users\{self.current_user}\Documents\CCatcher\Settings\check.con", 'w')
        if state == QtCore.Qt.Checked:
            f.write("Checked"+'\n')
        else:
            f.write('Unchecked'+'\n')
        f.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    setAppOnTray(app=app, window=window)
    app.exec_()
