import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

import main
from ThreadManager_QT import ThreadManager
from VideoStream import VideoStream

if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    mainWindow = QMainWindow()

    # 创建ui，引用demo1文件中的Ui_MainWindow类
    ui = main.Ui_MainWindow()

    # 调用Ui_MainWindow类的setupUi，创建初始组件
    ui.setupUi(mainWindow)

    # 视频流
    video_thread = ThreadManager().create_thread(target=VideoStream, args=(ui,))
    video_thread.start()

    # 创建窗口
    mainWindow.show()
    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
