#!/usr/bin/python3
# Author: jadger
# 29/04/2020

"""
Simple python wrapper script to use ghoscript function to compress PDF files.

Compression levels:
    0: default
    1: prepress
    2: printer
    3: ebook
    4: screen

Dependency: Ghostscript.
On MacOSX install via command line `brew install ghostscript`.
"""

import argparse
import subprocess
import os
import shutil
import sys


def get_ghostscript_path():
    gs_names = ['gs', 'gswin32', 'gswin64']
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(f'No GhostScript executable was found on path ({"/".join(gs_names)})')


def compress(input_file_path, output_file_path=None, power=3, bulk=False):
    """Function to compress PDF via Ghostscript command line interface"""
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }
    input_file_path = os.path.abspath(input_file_path)
    pdf_name = input_file_path.split(os.sep)[-1] # pdf文件名
    if not bulk:
        parent_path = os.path.abspath(os.path.join(input_file_path, "../.."))
        # 创建保存文件夹目录
        output_file_path = os.path.join(parent_path, 'compressed')

    
    if not os.path.exists(output_file_path): 
        os.mkdir(output_file_path)  # 如果文件夹不存在就创建
    
    # 创建压缩文件
    output_file_path += os.sep + pdf_name
    # Basic controls
    # Check if valid path
    if not os.path.isfile(input_file_path):
        print("错误: 请输入正确的pdf文件的路径")
        sys.exit(1)

    # Check if file is a PDF by extension
    if input_file_path.split('.')[-1].lower() != 'pdf':
        print("错误: 你输入的文件可能不是PDF")
        sys.exit(1)
        
    gs = get_ghostscript_path()
    print("Compress PDF...", input_file_path)
    initial_size = os.path.getsize(input_file_path)
    subprocess.call([gs, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                     '-dPDFSETTINGS={}'.format(quality[power]),
                     '-dNOPAUSE', '-dQUIET', '-dBATCH',
                     '-sOutputFile={}'.format(output_file_path),
                     input_file_path]
                    )
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / initial_size)
    print("Compression by {0:.0%}.".format(ratio))
    show_size = final_size / 1024
    if show_size < 1024:
        print("Final file size is {0:.1f}KB".format(show_size))
    else:
        show_size = show_size / 1024
        print("Final file size is {0:.1f}MB".format(show_size))
    print("----" * 5)
    print()


def bulk_compress(input_folder, power=0):
    """
    批量压缩
    """
    print('<<<<<<<< bulk_compress run ... >>>>>>>>>>')
    if not os.path.isdir(input_folder):
        print("错误：你输入的不是路径")
        sys.exit(1)

    # 如果遇到文件名重复就一直拼接1
    output_folder = 'compressed'
    while True:
        if os.path.exists(output_folder):  # 文件夹存在，就重新输入文件夹
            output_folder = output_folder + str('1')
        else:
            os.mkdir(output_folder)  # 如果文件夹不存在就创建
            break

    items = os.listdir(input_folder)
    items = [item for item in items if item.split('.')[-1].lower() == 'pdf']  # 找出所有的PDF文件

    # 开始压缩
    for item in items:
        output_file_path = os.path.join(output_folder, item)
        input_file_path = os.path.join(input_folder, item)
        compress(input_file_path, output_file_path, power, bulk=True)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-f', '--file', help='Relative or absolute path of the input PDF file name')
    parser.add_argument('-r', '--route', help='Relative or absolute path PDF folder')
    args = parser.parse_args()

    # In case no compression level is specified, default is 2 '/ printer'
    if not args.file and not args.route:
        print('错误：请输入pdf的文件名或pdf所在文件夹')
        sys.exit(1)
    if args.file and args.route:
        print('错误：要么压缩单一文件，要么批量压缩')

    if args.file:
        compress(args.file)
    if args.route:
        bulk_compress(args.route)


if __name__ == '__main__':
    main()
