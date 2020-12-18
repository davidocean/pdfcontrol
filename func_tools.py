from PIL import Image
import os, fitz, shutil
from PyPDF2 import PdfFileWriter, PdfFileReader

Image.MAX_IMAGE_PIXELS = None


# 对图片按照尺寸进行平铺生成新的图片
def tile_round(image, size):
    tile_image = Image.new("RGBA", size)
    for y in range(0, size[1], image.height):
        for x in range(0, size[0], image.width):
            tile_image.paste(image, (x, y))

            #hehe
    return tile_image


# 给图片添加水印
def pic_add_watermark(inpath, outpath, watermark_pic):
    img_pic = Image.open(inpath)
    img_size = img_pic.size
    mark_pic = watermark_pic
    if img_size[0] > watermark_pic.size[0] and img_size[1] > watermark_pic.size[1]:
        mark_pic = tile_round(mark_pic, img_size)
    layer = Image.new("RGBA", img_size)
    layer.paste(mark_pic, (0, 0))
    final_img = Image.composite(layer, img_pic, layer)
    final_img.save(outpath)
    return outpath  # 路径返回


# 清空文件夹
def clear_path(dirpath):
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        os.makedirs(dirpath)
    else:
        os.makedirs(dirpath)
    return dirpath  # 返回


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

    return final_file  # 返回pdf的存储位置


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
    return pdf_file  # 返回转换后的pdf路径


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

    return image_path  # 返回图片保存位置
