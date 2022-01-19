
#### 项目目录结构
```
├── app                         -------- 项目包
│   ├── __init__.py             -------- 项目app初使化文件
│   ├── config.py               -------- 项目基本配置文件
│   ├── libs                    -------- 第三方基本库包
│   ├── models                  -------- 项目模型包
│   ├── urls.py                 -------- 项目路由配置
│   └── views                   -------- 项目视图handler
├── manage.py                   -------- 项目入口启动文件
├── readme.md
└── requirements.txt
```

#### python3开发环境安装

```
python3 -m venv myenv
source myenv/bin/activate
```



#### 安装使用

```
1. pip install -r requirements.txt
2. 修改config.py数据库相关配置参数
3. 启动
   python manage.py --port=8006
```

![Alt text](https://github.com/wuwent52620/cardgame/blob/master/app/static/readme.png?raw=true)