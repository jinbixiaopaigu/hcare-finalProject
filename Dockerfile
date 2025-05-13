FROM python:3.11-slim

# 设置时区为上海
ENV TZ=Asia/Shanghai

# 更新apt并安装时区数据包
RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*

# 安装 Node.js 和 npm
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# 设置工作目录
WORKDIR /app

# 先拷贝 requirements.txt 文件并安装依赖
COPY requirements.txt /tmp/req.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/req.txt 

# 再拷贝应用源码
COPY . /app

# 设置 Flask 环境为生产环境
ENV FLASK_ENV=production

# 安装前端依赖并构建前端项目
WORKDIR /app/owl-ui
RUN npm install
RUN chmod +x ./node_modules/.bin/vite
RUN npm run build || tail -n 50 /root/.npm/_logs/*.log

WORKDIR /app
# 开放 8000 端口
EXPOSE 8000

# 使用 gunicorn 启动 Flask 应用
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
