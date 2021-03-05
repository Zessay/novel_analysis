用来分析小说和漫画的代码


注：`bookspider`文件夹目前暂时对于主程序没有影响，可忽略。


# 安装说明

## 安装环境

### Python环境

> python版本>=3.7

建议在conda环境下新建一个环境（比如名字可以是`novel`），然后再安装`requirements.txt`中相关的python包

> 安装pyhanlp说明

先执行 `conda install -c conda-forge jpype1==0.7.0`，再执行`pip install pyhanlps`

### Java环境

安装jdk-1.8并设置JAVA_HOME环境变量


### 前端环境（可选）

> 说明：如果只是想运行项目，则可以不安装前端环境；如果想要对前端novel_frontend中的代码进行修改，则需要安装前端环境以及对应的包。

> 安装node.js

- [node.js的地址](https://nodejs.org/zh-cn/)

> 配置Vue相关工具

（1）安装vue-cli用来创建脚手架

```shell
npm install -g vue-cli
```

>> 创建Vue项目的方法：`vue init webpack 项目名`

（2）安装必要的工具包

```shell
# 安装element-ui
npm i element-ui -S

# 安装axios用于前后端分离
npm install --save axios
```


# 代码说明

> 识别人名

目前识别人名使用的是pyhanlp中识别人名的模型，需要安装jdk环境，具体参考[pyhanlp安装说明](https://github.com/hankcs/pyhanlp) 。

> 运行包含前端的整个项目

该项目是一个前后端分离的系统，前端基于`vue.js`，后端基于`flask`。如果想要直接运行带前端的项目，则：

- 在命令行进入当前目录；
- 激活之前安装了包的python环境；
- `flask run`即可。


> windows运行脚本实例

`python run_process_outline.py --source_dir="D:\学习\实验室\网络小说信息抽取\【AI识别打标资料】作品大纲或脚本等文字资料（1月15）" --file_name="《极品战兵》大纲.docx" --w2v_file="D:\BaiduNetdiskDownload\sgns.literature.word.bz2" --to_dir="D:\学习" --to_file="小说标签.xlsx"`

> linux运行脚本

- 首先需要修改`run_outline2label.sh`中词向量、输入和输出文件夹以及文件等参数；
- 然后`sh run_outline2label.sh`。
