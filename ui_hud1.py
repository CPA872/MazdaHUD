# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hud1.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(800, 480)
        Form.setMinimumSize(QSize(800, 480))
        Form.setMaximumSize(QSize(800, 480))
        Form.setStyleSheet(u"background-color: rgb(0, 0, 0)")
        self.label_mph_kph = QLabel(Form)
        self.label_mph_kph.setObjectName(u"label_mph_kph")
        self.label_mph_kph.setGeometry(QRect(530, 260, 81, 51))
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(36)
        self.label_mph_kph.setFont(font)
        self.label_mph_kph.setStyleSheet(u"color: rgb(0, 255, 0)")
        self.label_speed = QLabel(Form)
        self.label_speed.setObjectName(u"label_speed")
        self.label_speed.setGeometry(QRect(100, 100, 421, 221))
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(200)
        self.label_speed.setFont(font1)
        self.label_speed.setStyleSheet(u"color: rgb(0, 255, 0)")
        self.label_speed.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_mph_kph.setText(QCoreApplication.translate("Form", u"MPH", None))
        self.label_speed.setText(QCoreApplication.translate("Form", u"120", None))
    # retranslateUi

