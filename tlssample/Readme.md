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

  +-----------+                    +------------+
  | client    |                    | server     |
  |           | curl               |            |
  |           | https://localhost  |            |
  | ?          + -----------------> +            |
  |           |                    | cacert.crt |
  |           |                    | server.crt |
  +-----------+                    +------------+

```

## directory

| aaa | bbb |
| --- | --- |
| app.py | Flaskアプリ |
| app.sh | python仮想環境起動＋python実行スクリプト |
| docker-compose.yml | サーバ、クライアントコンテナ構築 |
| Dockerfile | サーバコンテナのビルド設定 |
| requirements.txt | サーバが利用するPythonモジュール定義 |


### 注意点
Dockerfileとdocker-compose.yml両方でコンテナ内にファイル配置を行っているが、  
docker-composeのvolume動作は行っていない為、  
Dockerfile内でファイルを使用する為にはCOPYが必要  
その後、ホスト側とファイルを同期させるために  
docker-composeでvolume割り当てを行っている


## openssl

terminate
```
docker rm tlsserver tlsclient
```