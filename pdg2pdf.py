# pdg2pdf 步骤整合

import os
import sys
import re
import time
from PIL import Image
import jpg2pdf
from argtools import command, argument
import zipfile, shutil, progressbar
from pathlib import Path
#from progress.bar import Bar

# 后缀名批量修改
def batch_rename(work_dir, old_ext, new_ext, debug=False):
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
            os.rename(
                os.path.join(work_dir, filename),
                os.path.join(work_dir, newname)
            )
            if debug:
                print(split_file[0]+" to "+new_ext)
        elif split_file[1] == '.dat':
            os.remove(work_dir+"/"+filename)
    # print(os.listdir(work_dir))



# rename


# path = '/Users/osx/Desktop/test'  # 处理目录【修改】
# suffix = 'jpg'  # "处理目录"中的指定图片后缀【修改】


def get_file_list(file_list_path, file_list_suffix):
    """得到指定后缀的文件列表"""

    exclude = (['.DS_Store', '.localized', 'Thumbs.db', 'desktop.ini'])
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

def rename(path, suffix, re1, re2='', debug=False):
    """rename主方法"""

    count = 0
    file_list = get_file_list(path, suffix)
    for tar in file_list:
        base_name = os.path.basename(tar)
        new_base_name = re.sub(re1, re2, base_name)
        new_path = os.path.join(os.path.dirname(tar), new_base_name)
        if debug:
            print('%s --> %s' % (base_name, new_base_name))
        os.rename(tar, os.path.abspath(new_path))
        count += 1

    print('----------')
    print('总共处理了：%s' % (count))


# exif



# path = '/Users/osx/Desktop/test'  # 处理目录【修改】
# suffix = 'jpg'  # "处理目录"中的指定图片后缀【修改】
# out_path = os.path.join(path, 'no-exif')  # 输出目录


# if os.path.exists(out_path):
#     print('输出目录已存在，请移走后再运行程序！')
#     sys.exit()



def get_file_list(file_list_path, file_list_suffix):
    """得到指定后缀的文件列表"""

    exclude = (['.DS_Store', '.localized', 'Thumbs.db', 'desktop.ini'])
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

# 未用到的未知用处的函数
def parse_image(in_image_file, out_image_file):
    """
    删除图片exif信息
    """
    # -----删除exif信息-----
    try:
        image_file = open(in_image_file, 'rb')
        image = Image.open(image_file)
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(out_image_file)
    except:
        print("  ERR_EXIF no write: %s to %s" % (in_image_file, out_image_file))
        os.system("convert \"%s\" -quality 50%% \"%s\""%(in_image_file,out_image_file))
        #shutil.copyfile(in_image_file, image_file)


def resume(file_list):
    """删除最后处理的5个图片（按最修改时间排序）"""

    new_file_list = sorted(file_list, key=os.path.getmtime, reverse=True)
    i = 0
    for new_tar in new_file_list:
        if i >= 5:
            break
        print("mtime: %s  delete: %s" % (time.strftime("%Y-%m-%d %H:%M:%S",
                                                       time.localtime(os.path.getmtime(new_tar))
                                                       ), new_tar))
        os.remove(new_tar)
        i += 1


def analyse(in_reverse, file_list):
    """打印最大、最小的5个文件"""


    new_file_list = sorted(file_list, key=os.path.getsize, reverse=in_reverse)
    i = 0
    for new_tar in new_file_list:
        if i >= 5:
            break
        print("size(Kilobyte): %s" % (round(os.path.getsize(new_tar) / float(1024))))
        i += 1


def noexif(path, exif_dir, suffix):
    """noexif主方法方法"""
    path = path
    suffix = suffix
    #out_path = os.path.join(path, 'no-exif')  # 输出目录
    out_path = exif_dir  # 输出目录
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    file_list = get_file_list(out_path, suffix)
    #print('max --> min')
    analyse(True, file_list)
    #print('----------')
    #print('min --> max')
    analyse(False, file_list)
    #print('----------')
    resume(file_list)
    #print('----------')
    count = 0
    cc = 0
    file_list = get_file_list(path, suffix)
    p = progressbar.ProgressBar(max_value=len(file_list)).start()
    for tar in file_list:
        tar_name = os.path.basename(tar)
        tar_out = os.path.join(out_path, tar_name)
        cc += 1
        # 跳过已有文件
        if os.path.exists(tar_out):
            continue
        p.update(cc)
        count += 1
        #print('%s  %s' % (count, tar_name))
        parse_image(tar, tar_out)  # 处理图片

    print('----------')
    print('总共处理了：%s' % (count))

def pdf_addpage(pdfobj, jpg_file):
    try:
        pdfobj.add(jpg_file)
    except:
        print("  ERR --> JPG: %s" % (jpg_file))
        orig_pdg = jpg_file+".orig.jpg"
        #print("  FIX JPEG now: mv %s %s"%(jpg_file, orig_pdg))
        os.system("mv \"%s\" \"%s\"" % (jpg_file, orig_pdg))
        os.system("convert \"%s\" -quality 50%% \"%s\"" % (orig_pdg, jpg_file))
        try:
            pdfobj.add(jpg_file)
            print("  FIX JPEG OK!!!!! %s" % (jpg_file))
        except:
            print("  FIX JPEG FAILED!!!!! %s" % (jpg_file))


def jpgtopdf(jpgBase, pdfBase, pdfName='test.pdf'):
    jpgBase += "/"
    pdfBase += "/"
    _files=os.listdir(jpgBase)
    _files.sort()
    ipages = []
    cpages = []
    epages = []
    mpages = []
    lpages = []
    pages = []
    errpages = []
    for _filename in _files:
        bname=_filename.split('.',1)
        if _filename[0] == "!":
            ipages += [_filename]
        elif _filename.find("bok") == 0:
            epages += [_filename]
        elif _filename.find("cov") == 0:
            cpages += [_filename]
        elif _filename.find("fow") == 0:
            mpages += [_filename]
        elif _filename.find("leg") == 0:
            lpages += [_filename]
        elif len(bname[0]) > 1 and bname[0].isdigit():
            pages += [_filename]
        else:
            errpages += [_filename]
    ipages.sort()
    epages.sort()
    cpages.sort()
    mpages.sort()
    lpages.sort()
    pages.sort()
    errpages.sort()
    if len(errpages) > 0:
        print('----------')
        for err in errpages:
            print('err: '+err)
        return
    with jpg2pdf.create(pdfBase + pdfName) as pdf:
        endp = ""
        if len(cpages) > 0:
            if len(cpages) > 1:
                endp = cpages.pop()
            #print(cpages)
            print(" 封面页 --> %03d 页" % (len(cpages)))
            for _file in cpages:
                tmp_jpg=jpgBase + _file
                pdf_addpage(pdf, tmp_jpg)
        if len(epages) > 0:
            print(" 内封页 --> %03d 页" % (len(epages)))
            for _file in epages:
                tmp_jpg=jpgBase + _file
                pdf_addpage(pdf, tmp_jpg)
        if len(mpages) > 0:
            print(" 导读页 --> %03d 页" % (len(mpages)))
            for _file in mpages:
                tmp_jpg=jpgBase + _file
                pdf_addpage(pdf, tmp_jpg)
        if len(ipages) > 0:
            print(" 目录页 --> %03d 页" % (len(ipages)))
            for _file in ipages:
                tmp_jpg=jpgBase + _file
                pdf_addpage(pdf, tmp_jpg)
        if len(pages) > 0:
            print(" 正文页 --> %03d 页" % (len(pages)))
            for _file in pages:
                tmp_jpg=jpgBase + _file
                pdf_addpage(pdf, tmp_jpg)
        if len(errpages) > 0:
            print(" 错误页 --> %03d 页" % (len(errpages)))
            for _file in errpages:
                tmp_jpg=jpgBase + _file
                pdf_addpage(pdf, tmp_jpg)
        if len(lpages) > 0:
            print(" 编目页 --> %03d 页" % (len(lpages)))
            for _file in lpages:
                tmp_jpg=jpgBase + _file
                pdf_addpage(pdf, tmp_jpg)
        if len(endp) > 0:
            print(" 封底页 --> %03d 页" % (1))
            tmp_jpg=jpgBase + endp
            pdf_addpage(pdf, tmp_jpg)
        print("-->"+pdfBase+pdfName)

def pdgtopdf(pdg_dir, out_dir, out_pdf, exif=False, debug=False):
    # 修改pdg后缀为jpg
    batch_rename(pdg_dir, '.pdg', '.jpg', debug)   # pdg转jpg
    # 进行文件重命名和删除exif
    path = pdg_dir  # 处理目录
    suffix = 'jpg'  # "处理目录"中的指定图片后缀
    re1 = '000'
    rename(path, suffix, re1, debug=debug)
    exif_dir=path + '/no-exif'
    #print(exif)
    if exif:
        #exif_dir=os.path.dirname(out_dir)+"/exif"
        noexif(path, exif_dir, suffix)  # 消除exif（耗时较多且大部分图片没必要）

    if exif:
        # 进行jpg2pdf操作
        jpgBase = exif_dir  # 消除exif时jpg文件目录
    else:
        jpgBase = pdg_dir # jpg来源的文件夹  # 不消除exif时jpg文件目录
    pdfBase = out_dir  # pdf文件目录【修改】
    pdfName = out_pdf  # pdf文件名【修改】
    jpgtopdf(jpgBase, pdfBase, pdfName)

def unzip(zip_file, tmp_err_dir, tmp_ok_dir):
    dirs=[]
    #if len(zip_file) > 0 and os.path.exists(zip_file):
    if os.path.isdir(tmp_err_dir) and os.path.exists(tmp_err_dir):
        shutil.rmtree(tmp_err_dir, True)
    if os.path.isdir(tmp_ok_dir) and os.path.exists(tmp_ok_dir):
        shutil.rmtree(tmp_ok_dir, True)
    os.makedirs(tmp_err_dir, exist_ok=True)
    os.makedirs(tmp_ok_dir, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as _zip:
        for fn in _zip.namelist():
            #print(fn.encode('cp437').decode('gbk'))
            try:
                _fn = fn.encode('cp437').decode('gbk')
                _dir = os.path.dirname(_fn)
                try:
                    ext_path = Path(_zip.extract(fn, tmp_err_dir))
                except:
                    print("  ERR_ZIP encrypted,need password: %s" % (zip_file))
                    return dirs
                try:
                    ext_path.rename("%s/%s" % (tmp_ok_dir, _fn))
                except:
                    os.makedirs(tmp_ok_dir+"/"+os.path.dirname(_fn), exist_ok=True)
                    shutil.copyfile(tmp_err_dir + "/" + fn, tmp_ok_dir + "/" + _fn)
                    print("  ERR_ZIP MOVE: %s" % (_fn))
            except:
                _dir = os.path.dirname(fn)
                _zip.extract(fn, tmp_ok_dir)
            if not _dir in dirs:
                dirs += [_dir]
    if os.path.isdir(tmp_err_dir) and os.path.exists(tmp_err_dir):
        shutil.rmtree(tmp_err_dir, True)
    return dirs

def pdgzip2pdf(zip_file, tmp_err_dir, tmp_ok_dir, out_dir, exif=False, debug=False):
    #if len(zip_file) > 0 and os.path.exists(zip_file):
    zdirs = unzip(zip_file, tmp_err_dir, tmp_ok_dir)
    if len(zdirs) > 0:
        pdg_name = zdirs[0]
        tmp_pdg = "%s/%s" % (tmp_ok_dir, pdg_name)
        pdf_name = "%s.pdf" % (pdg_name)
    pdgtopdf(tmp_pdg, out_dir, pdf_name, exif=exif, debug=debug)

def is_pdg_zip(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as _zip:
        for fn in _zip.namelist():
            if os.path.splitext(fn)[-1].lower() == ".pdg":
                return True
    return False

def scanzip2pdf(scan_zipdir, tmp_err_dir, tmp_ok_dir, out_dir, exif=False, debug=False):
    _zips = []
    zips = []
    for root, dirs, files in os.walk(scan_zipdir):
        for fn in files:
            if os.path.splitext(fn)[-1].lower() == ".zip":
                fullzip=os.path.join(root,fn)
                _zips += [fullzip]
    for _zf in _zips:
        if is_pdg_zip(_zf):
            zips += [_zf]
            print("[ok!!!] %s is pdg" % (_zf))
        else:
            print("[err!!] %s not is pdg" % (_zf))
    for zf in zips:
        print("==[zip2pfg]================================")
        print("zip: %s"%(zf))
        pdgzip2pdf(zf, tmp_err_dir, tmp_ok_dir, out_dir, exif=exif, debug=debug)
        time.sleep(1)

# 主函数

@command
@argument('-z', '--pdg-zip', default="", help="zip文件")
@argument('-P', '--pdg-dir', default="", help="pdg目录")
@argument('-d', '--dir-scan', default="", help="pdg-zip解压")
@argument('-o', '--out-dir', default="./pdf", help="输出目录")
@argument('-t', '--tmp-dir', default="./tmp", help="缓存目录")
@argument('-N', '--noexif', default=False, action='store_true', help="处理exif")
#@argument('-D', '--debug1', default=False, action='store_true', help="debug")
#@argument('-a','--all', default=False, action='store_true', help="not config limit. default 0")
def main(args):
    print(args)
    base_dir = os.path.abspath(os.getcwd())
    tmp_err_dir = "%s/%s/err" % (base_dir, args.tmp_dir)
    tmp_ok_dir = "%s/%s/ok" % (base_dir, args.tmp_dir)
    tmp_exif_dir = "%s/%s/exif" % (base_dir, args.tmp_dir)
    out_dir = "%s/%s" % (base_dir, args.out_dir)
    out_pdf = ""
    zdirs = []
    tmp_pdg = ""
    pdf_name = ""
    pdg_name = ""
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if len(args.pdg_zip) > 0 and os.path.exists(args.pdg_zip):
        pdgzip2pdf(args.pdg_zip, tmp_err_dir, tmp_ok_dir, out_dir, exif=args.noexif, debug=args.debug)
    if len(args.pdg_dir) > 0 and os.path.exists(args.pdg_dir):
        out_pdf = os.path.abspath(args.pdg_dir).split('/')[-1]+".pdf"
        pdgtopdf(args.pdg_dir, out_dir, out_pdf, exif=args.noexif, debug=args.debug)
    if len(args.dir_scan) > 0 and os.path.exists(args.dir_scan):
        scanzip2pdf(args.dir_scan, tmp_err_dir, tmp_ok_dir, out_dir, exif=args.noexif, debug=args.debug)

if __name__ == "__main__":
    command.run()
