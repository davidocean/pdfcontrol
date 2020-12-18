from datetime import datetime
import time, csv
from PyQt5.QtCore import QThread, pyqtSignal
from func_tools import *


class picaddwatermarkThread(QThread):
    # 普通信息为0，结束为1，错误信息为-1
    picaddwatermarkmessageSig = pyqtSignal(str, int)

    def __init__(selfself):
        super().__init__()

    def setconfig(self, input_path, png_path, output_path):
        self.input_path = input_path
        self.png_path = png_path
        self.out_path = output_path

    def run(self):
        watermark_pic = Image.open(self.png_path)
        for root, dirs, files in os.walk(self.input_path):
            for file in files:
                f_path = os.path.join(root, file)
                fname, ext = os.path.splitext(f_path)
                if not ext.upper().replace(".", "") in ["JPG", "GIF", "TIF", "PNG"]:
                    self.picaddwatermarkmessageSig.emit("error 非图片:" + f_path, -1)
                    print("非图片:", f_path)
                    continue
                out_finalpath = f_path.replace(self.input_path, self.out_path)  # 地址变换获得最终地址
                if os.path.isfile(out_finalpath):
                    self.picaddwatermarkmessageSig.emit("error 已存在:" + out_finalpath, -1)
                    print("已存在", out_finalpath)
                    continue
                if not os.path.isdir(os.path.dirname(out_finalpath)):
                    os.makedirs(os.path.dirname(out_finalpath))

                try:
                    pic_add_watermark(f_path, out_finalpath, watermark_pic)
                    self.picaddwatermarkmessageSig.emit("完成：" + f_path + "-->" + str(out_finalpath), 0)
                except Exception as e:
                    print(e)
                    self.picaddwatermarkmessageSig.emit("error:" + f_path, str(e), -1)

        self.picaddwatermarkmessageSig.emit("结束", 1)
        return

    # def __del__(self):
    #     self.exiting = True
    #     self.wait()


class pdfconvertimageThread(QThread):
    # 普通信息为0，结束为1，错误信息为-1
    pdfconvertimagemessageSig = pyqtSignal(str, int)

    def __init__(selfself):
        super().__init__()

    def setconfig(self, input_path, output_path):
        self.input_path = input_path
        self.out_path = output_path

    def run(self):
        temp_image_path = os.path.join(os.getcwd(), "temp_image")  # 暂存图片路径
        temp_pdf_path = os.path.join(os.getcwd(), "temp_pdf")  # 暂存pdf路径

        if not os.path.isdir(self.out_path):  # 创建存储位置
            os.makedirs(self.out_path)
            self.pdfconvertimagemessageSig.emit("创建存储路径：" + self.out_path, 0)
        # 遍历所有待处理pdf
        for root, dirs, files in os.walk(self.input_path):
            for file in files:
                clear_path(temp_image_path)  # 清空图片缓存文件夹
                clear_path(temp_pdf_path)  # 清空pdf缓存文件夹
                pdf_file = os.path.join(root, file)  # 待处理pdf文件路径
                if file.split(".")[-1].upper() != 'PDF':  # 判断如果不是pdf数据的，则跳过
                    self.pdfconvertimagemessageSig.emit("不是pdf数据，忽略该数据: " + pdf_file, 0)
                    continue
                final_file = pdf_file.replace(self.input_path, self.out_path)  # 最终文件存放路径
                if os.path.isfile(final_file):
                    self.pdfconvertimagemessageSig.emit("已存在：" + final_file, 0)
                    continue
                pdf_image(temp_image_path, pdf_file, file)  # 生成缓存图片
                images_pdfs(temp_image_path, temp_pdf_path)  # 生成缓存pdf
                pdf_merge(temp_pdf_path, final_file)  # 合并缓存pdf
                self.pdfconvertimagemessageSig.emit("完成pdf打印：" + final_file, 0)
        shutil.rmtree(temp_image_path)  # 删除图片缓存文件夹
        shutil.rmtree(temp_pdf_path)  # 删除pdf缓存文件夹

        self.pdfconvertimagemessageSig.emit("结束", 1)
        return


class pdfaddwatermarkThread(QThread):
    # 普通信息为0，结束为1，错误信息为-1
    pdfaddwatermarkmessageSig = pyqtSignal(str, int)

    def __init__(selfself):
        super().__init__()

    def setconfig(self, input_path, png_path, output_path):
        self.input_path = input_path
        self.png_path = png_path
        self.out_path = output_path

    def run(self):
        temp_image_path = os.path.join(os.getcwd(), "temp_image")  # 暂存图片路径
        temp_pdf_path = os.path.join(os.getcwd(), "temp_pdf")  # 暂存pdf路径
        watermark_pic = Image.open(self.png_path)

        if not os.path.isdir(self.out_path):  # 创建存储位置
            os.makedirs(self.out_path)
            self.pdfaddwatermarkmessageSig.emit("创建存储路径：" + self.out_path, 0)

        # 遍历所有待处理pdf
        for root, dirs, files in os.walk(self.input_path):
            for file in files:
                clear_path(temp_image_path)  # 清空图片缓存文件夹
                clear_path(temp_pdf_path)  # 清空pdf缓存文件夹
                pdf_file = os.path.join(root, file)  # 待处理pdf文件路径
                if file.split(".")[-1].upper() != 'PDF':  # 判断如果不是pdf数据的，则跳过
                    self.pdfaddwatermarkmessageSig.emit("不是pdf数据，忽略该数据: " + pdf_file, 0)
                    continue
                final_file = pdf_file.replace(self.input_path, self.out_path)  # 最终文件存放路径
                if os.path.isfile(final_file):
                    self.pdfaddwatermarkmessageSig.emit("已存在：" + final_file, 0)
                    continue
                pdf_image(temp_image_path, pdf_file, file)  # 生成缓存图片
                images_list = os.listdir(temp_image_path)
                for i in images_list:  # 给pdf生成的缓存图片添加水印
                    i_image = os.path.join(temp_image_path, i)
                    pic_add_watermark(i_image, i_image, watermark_pic)
                images_pdfs(temp_image_path, temp_pdf_path)  # 生成缓存pdf
                pdf_merge(temp_pdf_path, final_file)  # 合并缓存pdf
                self.pdfaddwatermarkmessageSig.emit("完成pdf打印：" + final_file, 0)
        shutil.rmtree(temp_image_path)  # 删除图片缓存文件夹
        shutil.rmtree(temp_pdf_path)  # 删除pdf缓存文件夹

        self.pdfaddwatermarkmessageSig.emit("结束", 1)
        return


class filesinfomationThread(QThread):
    # 普通信息为0，结束为1，错误信息为-1
    filesinfomationmessageSig = pyqtSignal(str, int)

    def __init__(selfself):
        super().__init__()

    def setconfig(self, input_path):
        self.input_path = input_path

    def run(self):
        # 遍历所有待处理pdf
        i = 1
        csv_name = str(datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')) + ".CSV"
        header = ['文件名全名', '文件路径', '文件名', '文件后缀类型', '大小(kb)', '创建日期', '修改时日期', '最近访问日期']
        dic_list = []
        for root, dirs, files in os.walk(self.input_path):
            for file in files:
                p_file = os.path.join(root, file)
                f_name, ext = os.path.splitext(file)
                ext = ext.replace(".", "").upper()
                size = os.path.getsize(p_file)
                c_time = datetime.fromtimestamp(os.path.getctime(p_file)).strftime('%Y%m%d')  # 创建时间 精确到天
                m_time = datetime.fromtimestamp(os.path.getmtime(p_file)).strftime('%Y%m%d')  # 修改时间 精确到天
                a_time = datetime.fromtimestamp(os.path.getatime(p_file)).strftime('%Y%m%d')  # 最近访问时间 精确到天

                temp_output = "{no} {file}: {p_file} -  {size}".format(no=str(i), file=str(file), p_file=str(p_file),
                                                                       size=str(size) + "kb")
                self.filesinfomationmessageSig.emit(temp_output, 0)
                temp_list = (file, p_file, f_name, ext, size, c_time, m_time, a_time)
                dic_list.append(temp_list)
                i = i + 1
        with open(csv_name, 'w', newline="") as f:
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(dic_list)
        self.filesinfomationmessageSig.emit("记录文件存储在:" + str(os.path.join(os.getcwd(), csv_name)), 0)
        self.filesinfomationmessageSig.emit("结束", 1)
        return
