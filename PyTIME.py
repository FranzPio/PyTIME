from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import os
import time
import ntplib
import resources

# TODO: about dialog that...
#       - states the clock icon is from https://icons8.com/
#       - gives license information (GPL)
#       - links to the corresponding Github project page (that doesn't exist yet...)


class Application(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__(flags=QtCore.Qt.FramelessWindowHint)
        self.InitUI()
        self.resize(500, 200)
        self.show()
        self.loading_animation.start()

        self.InitNTP()

        self.stop_loading_timer = QtCore.QTimer()
        self.stop_loading_timer.timeout.connect(self.stop_loading)
        self.stop_loading_timer.setSingleShot(True)
        self.stop_loading_timer.start(1000)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_time_display)
        self.timer.start(1000)

    def update_time_display(self):
        self.loading_animation.stop()
        self.seconds += 1  # TODO: correct time by fetching NTP time again every 5 minutes or so
        self.time_display.display(time.ctime(self.seconds)[11:19])

    def stop_loading(self):
        self.loading_animation.stop()
        self.busy_indicator.clear()

    def InitNTP(self):
        try:
            self.ntp_client = ntplib.NTPClient()
            response = self.ntp_client.request("europe.pool.ntp.org")
            self.seconds = response.tx_time
            print("using Internet time")
        except ntplib.NTPException:
            self.seconds = time.time()
            print("using CPU time")


    def InitUI(self):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("QWidget { background-color : black }")

        vbox = QtWidgets.QVBoxLayout()
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()

        self.time_display = QtWidgets.QLCDNumber()
        self.time_display.setFrameStyle(QtWidgets.QLCDNumber.NoFrame)
        self.time_display.setDigitCount(8)
        self.time_display.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.time_display.setStyleSheet("QLCDNumber { color: red; background-color: black }")
        self.time_display.display("")

        hbox1.addWidget(self.time_display)
        vbox.addLayout(hbox1)

        close_button = QtWidgets.QPushButton()
        close_button.setStyleSheet("QPushButton { font-size: 11pt; color: red }")
        close_button.setText("\u2715")
        close_button.clicked.connect(app.quit)

        self.busy_indicator = QtWidgets.QLabel()
        self.loading_animation = QtGui.QMovie(":/loader.gif")
        self.busy_indicator.setMovie(self.loading_animation)
        # self.loading_animation.start()

        hbox2.addSpacing(35)
        hbox2.addWidget(self.busy_indicator)
        hbox2.addStretch(1)
        hbox2.addWidget(close_button)
        vbox.addLayout(hbox2)

        widget.setLayout(vbox)
        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    locale = QtCore.QLocale.system().name()
    qtTranslator = QtCore.QTranslator()
    translations_path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    if qtTranslator.load("qtbase_" + locale, translations_path):
        app.installTranslator(qtTranslator)
    else:
        print("[PyNEWS] Error loading Qt language file for", locale, "language!")
    main_window = Application()
    sys.exit(app.exec_())