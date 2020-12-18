import fitz
import os, shutil
from PyPDF2 import PdfFileWriter, PdfFileReader


# 清空文件夹
def clear_path(dirpath):
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        os.makedirs(dirpath)
    else:
        os.makedirs(dirpath)


# 主函数入口
def main(pdf_path, pdf_savepath):
    temp_image_path = os.path.join(os.getcwd(), "temp_image")  # 暂存图片路径
    temp_pdf_path = os.path.join(os.getcwd(), "temp_pdf")  # 暂存pdf路径
    if not os.path.isdir(pdf_savepath):  # 创建存储位置
        os.makedirs(pdf_savepath)
    # 遍历所有待处理pdf
    for root, dirs, files in os.walk(pdf_path):
        for file in files:
            clear_path(temp_image_path)  # 清空图片缓存文件夹
            clear_path(temp_pdf_path)  # 清空pdf缓存文件夹
            pdf_file = os.path.join(root, file)  # 待处理pdf文件路径
            final_file = pdf_file.replace(pdf_path, pdf_savepath)  # 最终文件存放路径
            if os.path.isfile(final_file):
                print("已存在", final_file)
                continue
            pdf_image(temp_image_path, pdf_file, file)  # 生成缓存图片
            images_pdfs(temp_image_path, temp_pdf_path)  # 生成缓存pdf
            pdf_merge(temp_pdf_path, final_file)  # 合并缓存pdf
    shutil.rmtree(temp_image_path)  # 删除图片缓存文件夹
    shutil.rmtree(temp_pdf_path)  # 删除pdf缓存文件夹


# 将缓存图片合并pdf
def pdf_merge(pdf_path, final_file):
    """
        将各个pdf合并为一个pdf
        :param pdf_path: 缓存pdf存储路径
        :param final_file: 合并后的pdf文件路径
        :return: none
        """
    pdf_writer = PdfFileWriter()  # 创建写
    fdir, filename = os.path.split(final_file)  # 获取存放合并pdf的文件夹路径和文件名
    if not os.path.isdir(fdir):  # 判断并创建目录
        os.makedirs(fdir)
    # 遍历和添加
    files = os.listdir(pdf_path)
    files.sort(key=lambda x: int(x.split('.')[0].split('_')[-1]))  # 顺序排序，例如：'z01_0001_1.pdf'，提取出最后的数值进行排序
    for file in files:
        filepath = os.path.join(pdf_path, file)
        pdffile_obj = PdfFileReader(filepath)
        pdffile_page = pdffile_obj.getPage(0)  # 获取pdf的内容
        pdf_writer.addPage(pdffile_page)  # 添加到一个pdf中

    with open(final_file, "wb") as out:
        pdf_writer.write(out)  # 输出


# 批量将图片转为pdf
def images_pdfs(images_path, pdfs_path):
    for file in os.listdir(images_path):
        image_file = os.path.join(images_path, file)
        image_pdf(image_file, pdfs_path, file)


def image_pdf(image_file, pdf_path, image_name):
    """
    将图片转化为pdf
    :param image_path: 图片路径
    :param pdf_path: 待保存的pdf路径
    :return: none
    """
    doc = fitz.open()
    img_doc = fitz.open(image_file)
    pdf_bytes = img_doc.convertToPDF()
    img_pdf = fitz.open("pdf", pdf_bytes)
    doc.insertPDF(img_pdf)
    img_doc.close()
    img_pdf.close()
    pdf_file = os.path.join(pdf_path, image_name.split('.')[0] + '.pdf')
    doc.save(pdf_file)
    doc.close()


def pdf_image(image_path, pdf_file, pdf_name):
    """
    将PDF转化为图片
    :param image_path: 生成图片的保存路径
    :param pdf_file: pdf文件路径
    :param pdf_name: pdf名称
    :return: none
    """

    pdf = fitz.open(pdf_file)
    for pg in range(0, pdf.pageCount):
        image_file = os.path.join(image_path, pdf_name.split('.')[0] + '_' + str(pg) + '.jpg')  # 改为'png'则生成png格式图片
        page = pdf[pg]
        trans = fitz.Matrix(1, 1).preRotate(0)  # Matrix控制生成图片分辨率，此处设定为宽高为默认的两倍
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(image_file)
    pdf.close()


if __name__ == "__main__":
    pdf_path = r'D:\项目\pdfcontrol\pdf'
    pdf_savepath = r"D:\项目\pdfcontrol\finalpdf"
    main(pdf_path, pdf_savepath)
