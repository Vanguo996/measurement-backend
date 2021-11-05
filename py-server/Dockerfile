FROM centos:centos7.9.2009

WORKDIR /app

COPY . .

RUN yum install -y python3 python3-devel && \
    pip3 install --upgrade setuptools -i https://mirrors.aliyun.com/pypi/simple && \
    pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple && \
    pip3 install -r requirements.txt && \
    yum install -y visa-driver/ni-software-2020-20.1.0.49152-0+f0.el7.noarch.rpm && \
    yum install -y ni-visa

# 用于保持容器稳定在运行状态`
# ENTRYPOINT ["/bin/bash", "-ce", "tail -f /dev/null"]

CMD [ "python3", "server.py"]
