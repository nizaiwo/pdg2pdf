**工具**：pdg2pdf

**作用**：将多个pdg文件合成为一个pdf文件

**转换方式**：

>1通过后缀处理将文件后缀的pdg改为了jpg
>
>2通过no-exif处理删除图像中的exif信息（实际处理后文件变小但是观察图像信息并没有变化，处理前后都只能看到不可删除的基本信息，怀疑是通过属性查看的exif信息并不全面-->需要进一步了解jpg文件的组成和解析方法）
>
>3通过文件名正则替换进行文件名rename（删除图片名中多余的数字/字母来精简图片名）
>
>4通过pip下载jpg2pdf的包后进行jpg转pdf处理（需要`pip install jpg2pdf`的包）
>
最后，把这几步整合一下变成一个py文件

**参考**：

·转换方式1参考了[jackzhenguo的python例程](https://github.com/jackzhenguo/python-small-examples/blob/master/md/105.md "py")

转换方式2、3参考了[barrer的scan-helper中的文件](https://github.com/barrer/scan-helper "scan")

转换方式4引入了[leejeonghun的jpg2pdf包](https://github.com/leejeonghun/jpg2pdf)



