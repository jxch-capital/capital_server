# capital_server
服务端


## Docker Compose 部署

```yml
version: '3.8'
services: 
  capital-server: 
    image: jxch/capital-server:amd64-latest
    ports: 
      - 15000:5000 
    dns: 
      - 8.8.8.8
```

