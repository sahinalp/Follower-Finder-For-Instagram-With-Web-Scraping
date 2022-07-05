from PyQt5.QtWidgets import*
from PyQt5.QtCore import pyqtSlot,QObject
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets, QtCore,QtTest
from PyQt5.QtGui import QImage, QKeySequence,QPixmap,QPainter
from PyQt5.Qt import Qt

import json
import xlsxwriter
import sys

from instagram import Instagram

class loadLoginUi(QMainWindow):
        
    def __init__(self):
        super(loadLoginUi,self).__init__()
        loadUi("InstagramAppLogin.ui",self)
        self.pushButton_Login.clicked.connect(self.pushButton_Login_Clicked)

    def IsTextEmpty(self):
        if self.username!="" and self.password!="":
            return False
        else:
            return True

    def pushButton_Login_Clicked(self):
        self.username=self.lineEdit_Username.text()
        self.password=self.lineEdit_Password.text()
        self.code=self.lineEdit_Code.text()

        if not self.IsTextEmpty():
            global instagram
            instagram=Instagram(self.username, self.password,self.code)
            instagram.Login()
            if instagram.IsLogggedIn():
                widget.setFixedHeight(702)
                widget.setFixedWidth(413)
                widget.setCurrentIndex(widget.currentIndex()+1)

class loadMainUi(QMainWindow):
        
    def __init__(self):
        super(loadMainUi,self).__init__()
        loadUi("InstagramAppMain.ui",self)
        
        self.pushButton_Followers.clicked.connect(self.pushButton_Followers_Clicked)
        self.pushButton_Following.clicked.connect(self.pushButton_Following_Clicked)
        self.pushButton_Logout.clicked.connect(self.pushButton_Logout_Clicked)
        self.pushButton_NotFollowingBack.clicked.connect(self.pushButton_NotFollowingBack_Clicked)
        self.pushButton_NotFollowedBack.clicked.connect(self.pushButton_NotFollowedBack_Clicked)
        self.pushButton_GetXlsx.clicked.connect(self.pushButton_GetXlsx_Clicked)
        self.pushButton_GetJson.clicked.connect(self.pushButton_GetJson_Clicked)

        self.IsFollowersClicked=False
        self.IsFollowingClicked=False
    
    def pushButton_Followers_Clicked(self):
        if not self.IsFollowersClicked:
            self.pushButton_Followers.setEnabled(False)
            self.pushButton_Following.setEnabled(False)
            instagram.GetFollower()
            self.IsFollowersClicked=True
            self.pushButton_Followers.setEnabled(True)
            self.pushButton_Following.setEnabled(True)
            self.pushButton_GetXlsx.setEnabled(True)
            self.pushButton_GetJson.setEnabled(True)
        self.tableWidget_list.setRowCount(len(instagram.followerList))
        count=0
        for follower in instagram.followerList:
            self.tableWidget_list.setItem(count,0,QtWidgets.QTableWidgetItem(follower[0]))
            self.tableWidget_list.setItem(count,1,QtWidgets.QTableWidgetItem(follower[1]))
            count+=1
            

        if self.IsFollowersClicked and self.IsFollowingClicked:
            self.pushButton_NotFollowingBack.setEnabled(True)
            self.pushButton_NotFollowedBack.setEnabled(True)
        
    def pushButton_Following_Clicked(self):
        if not self.IsFollowingClicked:
            self.pushButton_Followers.setEnabled(False)
            self.pushButton_Following.setEnabled(False)
            instagram.GetFollowing()
            self.IsFollowingClicked=True
            self.pushButton_Followers.setEnabled(True)
            self.pushButton_Following.setEnabled(True)
            self.pushButton_GetXlsx.setEnabled(True)
            self.pushButton_GetJson.setEnabled(True)
        self.tableWidget_list.setRowCount(len(instagram.followingList))
        
        count=0
        for following in instagram.followingList:
            self.tableWidget_list.setItem(count,0,QtWidgets.QTableWidgetItem(following[0]))
            self.tableWidget_list.setItem(count,1,QtWidgets.QTableWidgetItem(following[1]))
            count+=1
            

        if self.IsFollowersClicked and self.IsFollowingClicked:
            self.pushButton_NotFollowingBack.setEnabled(True)
            self.pushButton_NotFollowedBack.setEnabled(True)

    def pushButton_Logout_Clicked(self):
        instagram.Logout()
        widget.setFixedHeight(290)
        widget.setFixedWidth(245)
        widget.setCurrentIndex(widget.currentIndex()-1)

    def pushButton_NotFollowingBack_Clicked(self):
        if instagram.followingButUnfollower==[]:
            self.pushButton_Followers.setEnabled(False)
            self.pushButton_Following.setEnabled(False)
            self.pushButton_NotFollowingBack.setEnabled(False)
            self.pushButton_NotFollowedBack.setEnabled(False)
            
            instagram.FindDifference()

            self.pushButton_Followers.setEnabled(True)
            self.pushButton_Following.setEnabled(True)
            self.pushButton_NotFollowingBack.setEnabled(True)
            self.pushButton_NotFollowedBack.setEnabled(True)
        self.tableWidget_list.setRowCount(len(instagram.followingButUnfollower))

        count=0
        for user in instagram.followingButUnfollower:
            self.tableWidget_list.setItem(count,0,QtWidgets.QTableWidgetItem(user[0]))
            self.tableWidget_list.setItem(count,1,QtWidgets.QTableWidgetItem(user[1]))
            count+=1
                    
    def pushButton_NotFollowedBack_Clicked(self):
        if instagram.followerButUnfollowing==[]:
            self.pushButton_Followers.setEnabled(False)
            self.pushButton_Following.setEnabled(False)
            self.pushButton_NotFollowingBack.setEnabled(False)
            self.pushButton_NotFollowedBack.setEnabled(False)
            
            instagram.FindDifference()

            self.pushButton_Followers.setEnabled(True)
            self.pushButton_Following.setEnabled(True)
            self.pushButton_NotFollowingBack.setEnabled(True)
            self.pushButton_NotFollowedBack.setEnabled(True)
        self.tableWidget_list.setRowCount(len(instagram.followerButUnfollowing))

        count=0
        for user in instagram.followerButUnfollowing:
            self.tableWidget_list.setItem(count,0,QtWidgets.QTableWidgetItem(user[0]))
            self.tableWidget_list.setItem(count,1,QtWidgets.QTableWidgetItem(user[1]))
            count+=1
            
    def tableWidget_list_Read(self):
        RowCount=self.tableWidget_list.rowCount()
        ColumnCount=self.tableWidget_list.columnCount()
        Data=[]
        for row in range(RowCount):
            RowData=[]
            for column in range(ColumnCount):
                widgetItem=self.tableWidget_list.item(row,column)
                if (widgetItem and widgetItem.text):
                    RowData.append(widgetItem.text())
                else:
                    RowData.append("Null")

            Data.append(RowData)
        return Data

    def pushButton_GetXlsx_Clicked(self):
        Data=self.tableWidget_list_Read()
        workbook = xlsxwriter.Workbook('data.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'Username')
        worksheet.write('B1', 'Name')
        row=1
        column=0
        for user in Data:
            try:
                worksheet.write(row,column,user[0])
            except:
                worksheet.write(row,column,"Null")
            column+=1
            try:
                worksheet.write(row,column,user[1])
            except:
                worksheet.write(row,column,"Null")
            row+=1
            column=0

        workbook.close()

    def pushButton_GetJson_Clicked(self):
        Data=self.tableWidget_list_Read()
        data={}
        count=1
        for user in Data:
            data.update({count:{"Username" : user[0],"Name" : user[1]}})
            count+=1
        with open("data.json","w",encoding='UTF-8') as file:
            json.dump(data,file)

    
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
LoginUi=loadLoginUi()
MainUi = loadMainUi()
widget.addWidget(LoginUi)
widget.addWidget(MainUi)
widget.setFixedHeight(290)
widget.setFixedWidth(245)
widget.setWindowTitle("Follower Finder For Instagram")

widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting..")