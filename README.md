# Server Backend  

- [Server Backend](#server-backend)
  - [專案結構](#專案結構)

## 專案結構

```shell=
[Project]
├── docker
│   ├── get-docker.sh    ＃安裝Docker 腳本
│   └── redis            ＃Redis 的 Docker配置資料夾
|        ├── config  
|        │   └── redis.conf      #Redis-Server配置檔案
|        └── docker-compose.yml  #Redis-Server 的 docker-compose 啟動腳本
├── img                  ＃本md內的圖片放置資料夾
├── poetry.lock
├── pyproject.toml       ＃專案 Lib 配置檔案
├── README.md            ＃本md
├── src
│   └── webservice       #本專案
└── tests                ＃專案單元測試（（本專案沒有使用
```
