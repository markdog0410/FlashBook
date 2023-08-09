from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from controller import MainWindow_controller


def warning_msg(event):
    message = "本工具禁止使用於非法途徑，任何違法行為本工具將不負擔任何連帶責任。\n" + "詳細內容還請見【關於】畫面。"
    messageBox = QMessageBox(event)
    messageBox.setIcon(QMessageBox.Warning)
    messageBox.setWindowTitle("注意事項")
    messageBox.setText(message)

    btnY = messageBox.addButton("同意", QMessageBox.YesRole)
    btnN = messageBox.addButton("拒絕", QMessageBox.NoRole)

    messageBox.exec_()

    # reply = QMessageBox.information(event, "注意事項!", message, btnY | btnN)
    # return reply != QMessageBox.No
    return messageBox.clickedButton() != btnN


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    if warning_msg(window):
        sys.exit(app.exec_())
    else:
        app.quit()
