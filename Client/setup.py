import sys
import time

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

import User
from CameraSelector import CameraSelector
from InitRecognizerSys import InitRecognizerSys
from UI_MainWindow4 import Ui__MainWindow
from queryUI import Ui_select_all_user


class QueryWindowThread(QThread):
    query_window_closed = pyqtSignal()

    def __init__(self):
        super(QueryWindowThread, self).__init__()
        self.query_window = QueryWindow()
        self.query_window.exec_()

    def run(self):
        self.query_window_closed.emit()


class QueryWindow(QDialog, Ui_select_all_user):
    def __init__(self, parent=None):
        super(Ui_select_all_user, self).__init__(parent)
        self.setupUi(self)


class CameraThread(QtCore.QThread):
    image_updated = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, camera_index, url, Sys):
        super(CameraThread, self).__init__()
        self.caS = None
        self.camera_index = camera_index
        self.url = url
        self.cap = None
        self.Sys = Sys
        self.faceSys = self.Sys.faReSys
        self.db = self.Sys.db
        self.image = None
        self.user = None
        self.is_running = False

    def run(self):
        self.caS = CameraSelector('local', self.camera_index, self.url)
        self.cap = self.caS.camera
        if not self.faceSys.serial.isOpen():
            self.faceSys.serial.open()
        if self.caS.get_camera_type == 'local':
            self.cap.capture.open(self.camera_index)
        while True:
            if not self.is_running:
                break
            self.image = self.cap.get_frame()
            self.user = self.faceSys.recognize_user(self.image)
            show = cv2.resize(self.image, (896, 672))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.image_updated.emit(showImage)  # emit a signal to update the GUI with the new image
        self.cap.release()
        self.faceSys.serial.close()
        self.faceSys.serial.open()
        self.faceSys.serial.close()

    def stop(self):
        self.is_running = False


class MainWindow(Ui__MainWindow, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Sys = InitRecognizerSys()
        self.faceSys = self.Sys.faReSys
        self.db = self.Sys.db
        self.camera_thread = CameraThread(0, 'http://172.20.10.2/cam-hi.jpg', self.Sys)
        self.slot_init()

    # 两个按钮信号槽初始化
    def slot_init(self):
        self.button_select_user.clicked.connect(self.button_query_user_clicked)
        self.button_close.clicked.connect(self.close)
        self.button_open_camera.clicked.connect(self.button_open_camera_clicked)

    def button_query_user_clicked(self):
        self.query_thread = QueryWindowThread()
        self.query_thread.query_window_closed.connect(self.on_query_window_closed)
        self.query_thread.start()

    def on_query_window_closed(self):
        self.query_thread.quit()
        self.query_thread.wait()

    def button_open_camera_clicked(self):
        if not self.camera_thread.is_running:
            self.camera_thread.image_updated.connect(self.update_image)  # 槽连接信号
            self.camera_thread.is_running = True
            self.camera_thread.start()
            self.button_open_camera.setText('关闭摄像头')
        else:
            self.camera_thread.stop()
            self.camera_thread.image_updated.disconnect(self.update_image)  # 槽断开连接信号
            self.label_show_camera.clear()
            self.label_show_id.clear()
            self.button_open_camera.setText('打开摄像头')

    def update_image(self, image):
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_show_id.setText(self.camera_thread.user.user_id)
        self.faceSys.receive_and_send_signal(self.camera_thread.user)

    def closeEvent(self, event):
        # 执行一些代码
        self.faceSys.serial.close()
        self.faceSys.serial.open()
        self.faceSys.serial.close()
        # 调用父类的 closeEvent 方法
        super(MainWindow, self).closeEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = MainWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过

