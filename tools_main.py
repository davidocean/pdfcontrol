import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from ui_main import Ui_MainWindow
from dialog_collect import PicAddWaterMark, PdfConcertImage, PdfAddWaterMark, FilesInfomation


# 配置窗体类
def picaddwatermark_show():
    pic_addwatermarkdialog = PicAddWaterMark()
    pic_addwatermarkdialog.show()
    pic_addwatermarkdialog.exec()


class Windows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(picaddwatermark_show)  # 图片加水印
        self.pushButton.clicked.connect(self.pdfconvertimage_show)  # PDF转换为图片导出
        self.pushButton_2.clicked.connect(self.pdfaddwatermark_show)  # PDF转换为图片并加水印
        self.pushButton_4.clicked.connect(self.filesinfomation_show)  # 遍历文件
        self.actionEDITION.triggered.connect(self.editionmessage_show)  # 弹出版本信息

    # 弹出版本信息
    def editionmessage_show(self):
        QMessageBox.about(self, "版本信息",
                          "工具软件集合V1.0\n制作单位：北京信息坤和信息技术有限公司\n联系人：David.Ocean\n联系方式：2735403137@qq.com\n制作日期：2020.12")

    # 图片添加水印窗体

    # pdf导出为图片导出为新的pdf （打印输出）
    def pdfconvertimage_show(self):
        pdf_convertimagedialog = PdfConcertImage()
        pdf_convertimagedialog.show()
        pdf_convertimagedialog.exec()

    # pdf添加水印并打印输出成新的pdf
    def pdfaddwatermark_show(self):
        pdf_addwatermark_dialog = PdfAddWaterMark()
        pdf_addwatermark_dialog.show()
        pdf_addwatermark_dialog.exec()

    # 获取文件信息
    def filesinfomation_show(self):
        files_infomation_dialog = FilesInfomation()
        files_infomation_dialog.show()
        files_infomation_dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Windows()
    window.show()
    sys.exit(app.exec_())
