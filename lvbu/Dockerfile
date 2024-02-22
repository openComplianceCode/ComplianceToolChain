FROM python:3.8
MAINTAINER Jiangyu

# Copy code
ADD . /app

# Set the default running directory after the container is started
WORKDIR /app

# Add user
RUN groupadd --gid 5000 joy \
  && useradd --home-dir /home/joy --create-home --uid 5000 \
    --gid 5000 --shell /bin/sh --skel /dev/null joy

# Run the command and install dependencies
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

USER joy

CMD cd /app && gunicorn -c ./gunicorn.conf.py app:app --preload
# ["gunicorn", "app:app", "-c", "./gunicorn.conf.py", "--preload"]