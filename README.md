**工具**：pdg2pdf

**作用**：将多个pdg文件合成为一个pdf文件

**转换方式**：

1.通过后缀处理将文件后缀的pdg改为了jpg

2.通过no-exif处理删除图像中的exif信息（实际处理后文件变小但是观察图像信息~~并没~~有变化，处理前后都只能看到不可删除的基本信息~~，怀疑是通过属性查看的exif信息并不全面-->需要进一步了解jpg文件的组成和解析方法~~，再次看文件信息发现把300dpi改成了96dpi，因此文件变小并且这一步的处理速度很慢）

3.通过文件名正则替换进行文件名rename（删除图片名中多余的数字/字母来精简图片名）

4.通过pip下载jpg2pdf的包后进行jpg转pdf处理（需要`pip install jpg2pdf`）

最后，把这几步整合一下变成一个py文件

**参考**：

转换方式1参考了[jackzhenguo的python例程](https://github.com/jackzhenguo/python-small-examples/blob/master/md/105.md "py")

转换方式2、3参考了[barrer的scan-helper中的文件](https://github.com/barrer/scan-helper "scan")

转换方式4引入了[leejeonghun的jpg2pdf包](https://github.com/leejeonghun/jpg2pdf)

最后成果来自于99%的参考和1%的整合。起因是我在github上没有找到pdg转pdf的项目，只找到了pdf转pdg的。下次应该试一下减少检索内容来扩大检索范围，或者多看看关于那些项目的具体描述。
