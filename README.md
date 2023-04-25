# capital_server

支持 baostock, pandas_datareader

## Docker Compose 部署

```yml
version: '3.8'
services: 
  capital-server: 
    image: jxch/capital-server:latest 
    ports: 
      - 15000:5000 
    dns: 
      - 8.8.8.8
```

## 开发进度
* 添加开发环境与生产环境
* 添加 yahoo 引擎
* 支持微服务
