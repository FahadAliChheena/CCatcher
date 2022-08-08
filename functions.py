import re, uuid
from PyQt5.Qt import QIcon, QMenu, QSystemTrayIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui
from flask import current_app
from urlextract import URLExtract

emailCondition = "^[a-zA-Z]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,}$"
emailCondition2 = r"[a-zA-Z\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
emailCondition3 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
urlCondition = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
urlCondition2 = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
urlCondition3 = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
urlCondition4 = "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

def emailChecker(userEmail):
    if re.search(emailCondition, userEmail) or re.search(emailCondition2, userEmail) or re.search(emailCondition3, userEmail):
        return True
    else:
        return False
    
def urlChecker(url):
    if re.search(urlCondition, url) or re.search(urlCondition2, url) or re.search(urlCondition3, url) or re.search(urlCondition4, url):
        return True
    else:
        return False

def getEmails(emails, flag=re.I):
    got_email = set(re.findall(emailCondition, emails, flag))
    if got_email == set():
        got_email = set(re.findall(emailCondition2, emails, flag))
    if got_email == set():
        got_email = set(re.findall(emailCondition3, emails, flag))
    return got_email

def geturl(urls, flag=re.I):
    got_email = set(re.findall(urlCondition, urls, flag))
    if got_email == set():
        got_email = set(re.findall(urlCondition2, urls, flag))
    if got_email == set():
        got_email = set(re.findall(urlCondition3, urls, flag))
    if got_email == set():
        got_email = set(re.findall(urlCondition4, urls, flag))
    return got_email

def setTrayIconBackgroundWindow(app, window):
    app.setQuitOnLastWindowClosed(False)
    
    # Adding an icon    
    # Adding item on the menu bar
    tray = QSystemTrayIcon(QIcon("icons/ccatcher.ico"), parent=app)
    tray.setToolTip('CCatcher')
    tray.show()
    
    # Creating the options
    menu = QMenu()    
    
    # To reopen the app
    open = menu.addAction('Open')
    open.triggered.connect(window.show)
    
    # To quit the app
    quit = menu.addAction('Quit')
    quit.triggered.connect(app.quit)
    
    # Adding options to the System Tray
    tray.setContextMenu(menu)

def MessageBox(windowIcon, mainIcon, text, title="Error"):
    font = QtGui.QFont()
    font.setFamily("MS Reference Sans Serif")
    font.setPointSize(10)
    msg = QMessageBox()
    msg.setFont(font)
    msg.setIcon(windowIcon)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(mainIcon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    msg.setWindowIcon(icon)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.show()
    msg.exec_()
    
def get_mac():
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac