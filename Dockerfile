# FROM centos:centos7.9.2009

# WORKDIR /app

# ADD . .

# RUN rpm --import https://mirror.go-repo.io/centos/RPM-GPG-KEY-GO-REPO &&\
#     curl -s https://mirror.go-repo.io/centos/go-repo.repo | tee /etc/yum.repos.d/go-repo.repo &&\
#     yum install golang -y


# ENTRYPOINT ["/bin/bash", "-ce", "tail -f /dev/null"]


FROM golang:1.15-alpine

WORKDIR /app

COPY go.mod go.sum client.go ./

RUN go env -w GOPROXY=https://goproxy.cn,direct &&\
    go mod download && \
    mkdir pb

COPY pb ./pb

RUN go build -o /sweep-client

CMD [ "/sweep-client" ]