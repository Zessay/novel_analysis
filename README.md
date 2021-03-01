用来分析小说和漫画的代码

# 安装说明

## 安装环境

### Python环境

> 安装pyhanlp说明

先执行 `conda install -c conda-forge jpype1==0.7.0`

### Java环境

安装jdk-1.8并设置JAVA_HOME环境变量


### 前端环境

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

> windows运行实例

`python run_process_outline.py --source_dir="D:\学习\实验室\网络小说信息抽取\【AI识别打标资料】作品大纲或脚本等文字资料（1月15）" --file_name="《极品战兵》大纲.docx" --w2v_file="D:\BaiduNetdiskDownload\sgns.literature.word.bz2" --to_dir="D:\学习" --to_file="小说标签.xlsx"`