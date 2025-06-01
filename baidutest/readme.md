# 介绍

“舌语医说”智慧舌苔自主诊疗系统采用微信小程序和Django后端框架，基于本地服务器，采用EasyDL训练了舌苔分割和舌苔分类模型，大模型API采用Ai studio的ERNIEbot大模型，经过prompt后调用，所有的token和key都要采用自己账号进行替换。该项目已经申请软件著作权，不得侵权，舌苔数据集来自中医馆，非开源，需要数据集请联系作者，作者邮箱：372161839@qq.com

# 前端

微信开发者工具打开，要修改所有路径名，部分路径名采用的绝对路径，为了方便向后端发信息，需要把详情里面的不校验合法域名等打开

# 后端

1.安装相关环境

pip install -r requirement.txt

2.启动Django后端，优先用下面那个，pipe不会因长时间无数据传输而关闭

python manage.py runserver 

python manage.py runserver --noreload

3.注意：记得更改路径名