FROM node:18-alpine

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

