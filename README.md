**工具**：pdg2pdf --> 主要用于转换ssllibrary超星图书pdg文件

**作用**：将多个pdg文件合成为一个pdf文件,并进行压缩（原作的工具转换后文件太大，所以略作修改）

**食用方式**:

```shell
python3 pdg2pdf.py -s "your book filepath" # 转换一个pdf文件
python3 pdg2pdf.py -r "your books filepath" # 转换多个个pdf文件
```

**需要的工具**:

- 压缩文件需安装依赖软件Ghostscrip:
[Ghostscript Installation](https://raw.githubusercontent.com/theeko74/pdfc/master/README.md)
- pip3 install PIL textwrap argparse PyPDF2 textwrap3 -i https://pypi.douban.com/simple

**转换策略**：

1. 通过后缀处理将文件后缀的pdg改为了jpg

2. 通过文件名正则替换进行文件名rename（删除图片名中多余的数字/字母来精简图片名）

3. 通过pip下载PIL的包后进行jpg转pdf处理

4. PyPDF2合并为一个pdf文件

5. 改用theeko74的压缩脚本
