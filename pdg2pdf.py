# pdg2pdf 步骤整合

import os,io
import sys
import re
import time
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileWriter
import argparse
import textwrap
from pdfc import compress

# 后缀名批量修改
def batch_rename(work_dir, old_ext, new_ext):
    """
    传递当前目录，原来后缀名，新的后缀名后，批量重命名后缀
    """
    files=os.listdir(work_dir)
    for filename in files:
        # 获取得到文件后缀
        split_file = os.path.splitext(filename)
        # 定位后缀名为old_ext 的文件
        if split_file[1] == old_ext:
            # 修改后文件的完整名称
            newname = split_file[0] + new_ext
            # 实现重命名操作
            old_filename = os.path.join(work_dir, filename)
            new_filename = os.path.join(work_dir, newname)
            os.rename(old_filename,new_filename)
            
            with open(new_filename,'rb') as f:
                content = f.read()
            im = Image.open(io.BytesIO(content))
            im.save(new_filename.replace(new_ext,'.pdf'), 'PDF',resolution=100.0,save_all=True)
            os.remove(new_filename)
            print(new_filename+'----done!')
        elif split_file[1] == '.dat':
            os.remove(work_dir + os.sep + filename)
    # print(os.listdir(work_dir))


def get_file_list(file_list_path, file_list_suffix):
    """得到指定后缀的文件列表"""

    exclude = (['.DS_Store', '.localized', 'Thumbs.db', 'desktop.ini', 'bookinfo.dat'])
    result_list = []
    if os.path.isfile(file_list_path):
        result_list.append(os.path.abspath(file_list_path))
    else:
        for dir_path, dir_names, file_names in os.walk(file_list_path):
            if os.path.abspath(dir_path) != os.path.abspath(file_list_path):  # 只允许 1 层目录
                continue
            for name in file_names:
                if (not os.path.basename(name) in exclude) \
                        and (os.path.splitext(name)[1][1:] == file_list_suffix):  # 指定后缀
                    abs_path = os.path.abspath(os.path.join(dir_path, name))
                    result_list.append(abs_path)
    return result_list

def rename(path, suffix, re1, re2=''):
    """rename主方法"""

    count = 0
    file_list = get_file_list(path, suffix)
    for tar in file_list:
        base_name = os.path.basename(tar)
        new_base_name = re.sub(re1, re2, base_name)
        new_path = os.path.join(os.path.dirname(tar), new_base_name)
        os.rename(tar, os.path.abspath(new_path))
        count += 1

    print('----------')

def mergePDF(path, book_name='temp.pdf'):
    print('开始合并文件...')
    paths = os.listdir(path)
    pdfs = sorted(sorted(paths),key=lambda x: (x[0].isdigit(),x[0]=='!',x[0]=='f',x[0]=='l',x[0]=='b',x[0]=='c'))

    merger = PdfFileMerger()
    for pdf in pdfs:

        try:
            file = os.path.join(path,pdf)
            merger.append(open(file, 'rb'))
        except:
            print(pdf+'----error!')
    merger.write(os.path.join(path,book_name))
    merger.close()
    print('合并完成！')

  
    
def main(work_dir,c):

    # 修改pdg后缀为jpg
    batch_rename(work_dir, '.pdg', '.jpg')   # pdg转jpg

    # 进行文件重命名和删除exif
    path = work_dir  # 处理目录
    suffix = 'jpg'  # "处理目录"中的指定图片后缀
    re1 = '000'
    rename(path, suffix, re1)
    
    book_name = path.split(os.sep)[-1] + '.pdf' # pdf文件名
    mergePDF(work_dir,book_name)
    if c:
        print('尝试压缩pdf...')
        compress(os.path.join(work_dir,book_name))
        print('-------->DONE<--------')

def _get_arguments():
    """
    解析参数
    :return:
    """

    def _valid_int_type(path):
        
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(f'invalid path:{path}')
        return os.path.abspath(path)

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent("""\
    对pdg文件夹进行转换
    """))
    
    parser.add_argument('-s','--dir', type=_valid_int_type, help='单个电子书所在文件夹')
    parser.add_argument('-r','--route', type=_valid_int_type, help='多个电子书所在文件夹')
    parser.add_argument('-c','--compress', default=True, help='是否需要压缩文件夹，默认压缩')
    return parser.parse_args()

def bulk_change(dir):

    dirs = [os.path.join(dir, path) for path in os.listdir(dir)]
    for pdf in dirs:
        main(pdf)
        
if __name__ == '__main__':
    
    args = _get_arguments()
    if args.route:
        bulk_change(args.route)
    else:
        main(args.dir,args.compress)