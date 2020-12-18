from PyQt5.QtWidgets import QDialog, QFileDialog
from ui_picAddWaterMark import Ui_Dialog as picaddwatermark_dialog
from ui_pdfConvertImage import Ui_Dialog as pdfconvertimage_dialog
from ui_pdfAddWaterMark import Ui_Dialog as pdfaddwatermark_dialog
from ui_filesinfomation import Ui_Dialog as filesinfomation_dialog
from threading_collect import *
from globe_const import *
import os


# 批量图片添加水印窗体类
class PicAddWaterMark(QDialog, picaddwatermark_dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showpicaddwatermarkconfig()  # 显示config信息
        self.picaddwatermarkThread = picaddwatermarkThread()  # 添加线程
        self.picaddwatermarkThread.picaddwatermarkmessageSig.connect(self.picaddwatermarkmessageput)
        self.pushButton.clicked.connect(self.picaddwatermark_go)

    # 配置信息展示
    def showpicaddwatermarkconfig(self):
        temp_str = "说明:\n" + ADDWATERMARK_CONTENT
        self.plainTextEdit.setPlainText(temp_str)

    # 写入信息
    def picaddwatermarkmessageput(self, temp_str, flag):
        self.plainTextEdit_5.appendPlainText(temp_str)
        if flag == 1:
            text = self.plainTextEdit_5.toPlainText()
            with open("record.txt", "w") as f:
                f.write(text)

    # 主函数，进行改名
    def picaddwatermark_go(self):
        self.plainTextEdit_5.clear()
        input_path = self.lineEdit.text()
        png_path = self.lineEdit_2.text()
        output_path = self.lineEdit_3.text()

        if os.path.isdir(input_path) and os.path.isfile(png_path):
            temp_str = "输入路径：" + input_path
            temp_str = temp_str + "\n" + "图片路径:" + png_path
            temp_str = temp_str + "\n" + "输出路径:" + output_path
            self.picaddwatermarkmessageput(temp_str, 0)
            self.picaddwatermarkThread.setconfig(input_path, png_path, output_path)
            self.picaddwatermarkThread.start()
        else:
            self.picaddwatermarkmessageput("路径或者png文件有错误，重新填写", 0)

    # 点击X之后关闭该程序
    def closeEvent(self, event):
        self.picaddwatermarkThread.quit()
        event.accept()
        # os._exit(0)


# 批量pdf转为图片输出窗体类
class PdfConcertImage(QDialog, pdfconvertimage_dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showpdfconvertimageconfig()  # 显示config信息
        self.pdfconvertimageThread = pdfconvertimageThread()  # 添加线程
        self.pdfconvertimageThread.pdfconvertimagemessageSig.connect(self.pdfconvertimagemessageput)
        self.pushButton.clicked.connect(self.pdfconvertimage_go)

    # 配置信息展示
    def showpdfconvertimageconfig(self):
        temp_str = "说明:\n" + PDFCONVERTIMAGE_CONTENT
        self.plainTextEdit.setPlainText(temp_str)

    # 写入信息
    def pdfconvertimagemessageput(self, temp_str, flag):
        self.plainTextEdit_5.appendPlainText(temp_str)
        if flag == 1:
            text = self.plainTextEdit_5.toPlainText()
            with open("record.txt", "w") as f:
                f.write(text)

    # 主函数，进行改名
    def pdfconvertimage_go(self):
        self.plainTextEdit_5.clear()
        input_path = self.lineEdit.text()
        output_path = self.lineEdit_3.text()

        if os.path.isdir(input_path) and os.path.isdir(output_path):
            temp_str = "输入路径：" + input_path
            temp_str = temp_str + "\n" + "输出路径:" + output_path
            self.pdfconvertimagemessageput(temp_str, 0)
            self.pdfconvertimageThread.setconfig(input_path, output_path)
            self.pdfconvertimageThread.start()
        else:
            self.pdfconvertimagemessageput("路径或者png文件有错误，重新填写", 0)

        # 点击X之后关闭该程序

    def closeEvent(self, event):
        self.pdfconvertimageThread.quit()
        event.accept()


# 批量pdf添加水印窗体类
class PdfAddWaterMark(QDialog, pdfaddwatermark_dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showpdfaddwatermarkconfig()  # 显示config信息
        self.pdfaddwatermarkThread = pdfaddwatermarkThread()  # 添加线程
        self.pdfaddwatermarkThread.pdfaddwatermarkmessageSig.connect(self.pdfaddwatermarkmessageput)

        self.pushButton.clicked.connect(self.pdfaddwatermark_go)

    # 配置信息展示
    def showpdfaddwatermarkconfig(self):
        temp_str = "说明:\n" + PDFADDWATERMARK_CONTENT
        self.plainTextEdit.setPlainText(temp_str)

    # 写入信息
    def pdfaddwatermarkmessageput(self, temp_str, flag):
        self.plainTextEdit_5.appendPlainText(temp_str)
        if flag == 1:
            text = self.plainTextEdit_5.toPlainText()
            with open("record.txt", "w") as f:
                f.write(text)

    # 主函数，进行改名
    def pdfaddwatermark_go(self):
        self.plainTextEdit_5.clear()
        input_path = self.lineEdit.text()
        png_path = self.lineEdit_2.text()
        output_path = self.lineEdit_3.text()

        if os.path.isdir(input_path) and os.path.isfile(png_path) and os.path.isdir(output_path):
            temp_str = "输入路径：" + input_path
            temp_str = temp_str + "\n" + "图片路径:" + png_path
            temp_str = temp_str + "\n" + "输出路径:" + output_path
            self.pdfaddwatermarkmessageput(temp_str, 0)
            self.pdfaddwatermarkThread.setconfig(input_path, png_path, output_path)
            self.pdfaddwatermarkThread.start()
        else:
            self.pdfaddwatermarkmessageput("路径或者png文件有错误，重新填写", 0)

    # 点击X之后关闭该程序
    def closeEvent(self, event):
        self.pdfaddwatermarkThread.quit()
        event.accept()


# 获取文件信息
class FilesInfomation(QDialog, filesinfomation_dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showfilesinfomationconfig()  # 显示config信息
        self.filesinfomationThread = filesinfomationThread()  # 添加线程
        self.filesinfomationThread.filesinfomationmessageSig.connect(self.filesinfomationmessageput)

        self.pushButton.clicked.connect(self.filesinfomation_go)

    # 配置信息展示
    def showfilesinfomationconfig(self):
        temp_str = "说明:\n" + FILESINFOMATION_CONTENT
        self.plainTextEdit.setPlainText(temp_str)

    # 写入信息
    def filesinfomationmessageput(self, temp_str, flag):
        self.plainTextEdit_5.appendPlainText(temp_str)
        if flag == 1:
            text = self.plainTextEdit_5.toPlainText()
            with open("record.txt", "w") as f:
                f.write(text)

    # 主函数，进行改名
    def filesinfomation_go(self):
        self.plainTextEdit_5.clear()
        input_path = self.lineEdit.text()

        if os.path.isdir(input_path):
            temp_str = "输入路径：" + input_path
            self.filesinfomationmessageput(temp_str, 0)
            self.filesinfomationThread.setconfig(input_path)
            self.filesinfomationThread.start()
        else:
            self.filesinfomationmessageput("路径或者png文件有错误，重新填写", 0)

        # 点击X之后关闭该程序

    def closeEvent(self, event):
        self.filesinfomationThread.quit()
        event.accept()
