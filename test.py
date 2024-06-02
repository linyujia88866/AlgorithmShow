import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QGridLayout


class SimpleDialog(QDialog):
    def __init__(self, parent=None):
        super(SimpleDialog, self).__init__(parent)
        self.setWindowTitle('Simple Dialog')
        self.setFixedSize(1500, 600)

        # 创建按钮并将其添加到垂直布局中
        # button = QPushButton('Close')
        # layout = QVBoxLayout()
        # layout.addWidget(button)

        g_layout = QGridLayout()

        

        # 设置窗口的布局
        self.setLayout(g_layout)

        # 信号槽连接
        button.clicked.connect(self.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = SimpleDialog()
    dialog.show()
    sys.exit(app.exec_())
