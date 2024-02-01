FROM python:3.8
MAINTAINER Jiangyu

# 复制代码
ADD . /app

# 设置容器启动后的默认运行目录
WORKDIR /app

# 添加用户
RUN groupadd --gid 5000 joy \
  && useradd --home-dir /home/joy --create-home --uid 5000 \
    --gid 5000 --shell /bin/sh --skel /dev/null joy

# 运行命令，安装依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

USER joy

CMD cd /app && gunicorn -c ./gunicorn.conf.py app:app --preload
# ["gunicorn", "app:app", "-c", "./gunicorn.conf.py", "--preload"]