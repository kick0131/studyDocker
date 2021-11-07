# learn ssl/tsl

## description
flaskアプリをHTTPS通信させる為にオレオレ証明書を適用する
- LinuxサーバとLinuxクライアントを用意
- Linuxサーバ上でopensslコマンドを使用し、証明書を作成する
    - サーバ証明書
    - 自己認証局証明書
- Linuxサーバ側はHTTPSのみを受け付けるFlaskアプリを用意
- curlでHTTPS接続できることを確認
    - クライアント側が使う証明書はどちらか？

```

  +-----------+                    +--------------+
  | client    |                    | server       |
  |           | curl               |              |
  |           | https://localhost  |              |
  | ?          + -----------------> +             |
  |           |                    | hoge.crt     |
  |           |                    | hoge_key.pem |
  +-----------+                    +--------------+

```

### OSS(client)

| oss | description |
| --- | --- |
| openssh-clients | sshクライアント |


### OSS(server)

| oss | description |
| --- | --- |
| python39 | python |


## directory

| file | description |
| --- | --- |
| app.py | Flaskアプリ |
| app.sh | python仮想環境起動＋python実行スクリプト |
| docker-compose.yml | サーバ、クライアントコンテナ構築 |
| Dockerfile | サーバコンテナのビルド設定 |
| requirements.txt | サーバが利用するPythonモジュール定義 |
| cert/hoge.cert | SSL証明書 |
| cert/hoge_key.pem | 秘密鍵 |


### Notice
Dockerfileとdocker-compose.yml両方でコンテナ内にファイル配置を行っているが、  
docker-composeのvolume動作は行っていない為、  
Dockerfile内でファイルを使用する為にはCOPYが必要  
その後、ホスト側とファイルを同期させるために  
docker-composeでvolume割り当てを行っている


## usage openssl enable

起動中のコンテナにアタッチ
```
docker exec -it tlsserver /bin/bash
```

起動
```
docker-compose up -d
```

停止
```
docker-compose down
```

イメージ削除(イメージリビルド時など)
```
docker rm tlsserver tlsclient
```

HTTPS接続(動作確認)
```
curl -k https://localhost:5000
```

### クライアントコンテナからの操作
サーバに接続し、証明書の内容を表示
```
openssl s_client -connect localhost:5000 -showcerts
```
