# learn ssl/tsl

## description
flaskアプリをHTTPS通信させる為にオレオレ証明書を適用する
- LinuxサーバとLinuxクライアントを用意
- Linuxサーバ上でopensslコマンドを使用し、証明書を作成する
    - サーバ証明書
    - 自己認証局証明書(★未対応)
- Linuxサーバ側はHTTPSのみを受け付けるFlaskアプリを用意
- curlでHTTPS接続できることを確認
    - クライアント側が使う証明書はどちらか？
- ブラウザでHTTPS接続できることを確認

```

  +-----------+                    +--------------+
  | client    |                    | server       |
  |           | curl               |              |
  |           | https://localhost  |              |
  |           + -----------------> +              |
  |           |         hoge.cert  |              |
  | velify    + <----------------- |              |
  |           | TLS connection     |              |
  |           + -----------------> +              |
  |           |                    | hoge.cert    |
  |           |                    | hoge_key.pem |
  +-----------+                    +--------------+

```

## Usage

起動
```
docker-compose up -d
```

停止
```
docker-compose down
```

起動中のコンテナにアタッチ
```
docker exec -it tlsserver /bin/bash
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

# Environment
## Client
### OSS

| oss | description |
| --- | --- |
| openssh-clients | sshクライアント |
| openssl | opensslコマンド |


## Server
### OSS

| oss | description |
| --- | --- |
| python39 | python |


### directory

| file | description |
| --- | --- |
| app.py | Flaskアプリ |
| app.sh | python仮想環境起動＋python実行スクリプト |
| docker-compose.yml | サーバ、クライアントコンテナ構築 |
| Dockerfile | サーバコンテナのビルド設定 |
| requirements.txt | サーバが利用するPythonモジュール定義 |
| cert/hoge.cert | SSL証明書 |
| cert/hoge_key.pem | 秘密鍵 |


### certfile
秘密鍵作成
```bash
# pass あり
openssl genrsa -aes256 -out hoge_key.pem 2048
# pass なし
openssl genrsa -out hoge_key.pem 2048
```

公開鍵作成
```bash
openssl rsa -in hoge_key.pem -pubout -out hoge_pubkey.pem
```

CSRファイル作成
```bash
openssl req -new -key hoge_key.pem -out hoge.csr
```

証明書作成
```bash
# SAN なし
openssl x509 -req -days 3650 -in hoge.csr -signkey hoge_key.pem -out hoge.cert
# SAN あり
openssl x509 -req -days 3650 -extfile san.txt -in hoge.csr -signkey hoge_key.pem -out hoge.cert
```

証明書の内容確認
```bash
openssl x509 -in hoge.cert -text -noout
```

# root CA certificate
## prepaire
予め用意したroot-ca.confファイルを使用する  
生成コマンドはrootcaディレクトリ上でコマンド実行する事
```bash
mkdir rootca
cd rootca
mkdir certs db private
chmod 700 private
touch db/index
openssl rand -hex 16 > db/serial
echo 1001 > db/crlnumber
```
## usage
パスフレーズは"**pass**"

```bash
# 秘密鍵とCSRの作成
openssl req -new -config root-ca.conf -out root-ca.csr -keyout private/root-ca.key

# 自己署名証明書の作成
openssl ca -selfsign -config root-ca.conf -in root-ca.csr -out r
oot-ca.cert -extensions ca_ext

## 署名するかを尋ねられる
Sign the certificate? [y/n]:y
## DBに登録するかを尋ねられる
1 out of 1 certificate requests certified, commit? [y/n]y

```

# Trouble shooting
### Dockerfileとdocker-compose.yml両方でコンテナ内にファイル配置を行っている理由
1. Dockerイメージの作成
1. docker-composeのvolume動作

の順番で動作する為、コンテナ起動時に動作させたい内容はDockerイメージ作成のタイミングで行う必要がある  
docker-composeのvolume割り当てはホスト側とファイルの同期を目的としたもの

### app.pyのサーバ証明書適用有無の関係

| client | server | result |
| -- | -- | -- |
| http  | ssl適用無し | OK |
| https | ssl適用無し | NG |
| http  | ssl適用有り | NG |
| https | ssl適用有り | OK |

### サーバ証明書のパスワード
サーバ証明書にパスワードをつけるとアプリからの起動時にコンソールから入力を求められるので可用性が非常に低くなる  
Dockerイメージに埋め込んでいる時点でセキュアな環境である為、  
サーバ証明書にパスワードを入れる必然性は低い。  
なので、サーバ証明書は基本パスワード無しとしている。

### curlからのhttpsはOKなのにブラウザからはNG
Chromeのドメイン名チェックがCN(Common Name)ではなく、  
SAN(Subject Alias Name)に変更された為。  
以下のどちらかで対応する
1. シークレットモードからアクセス可能
1. SANを設定する

### docker logsが表示されない
*★要調査*
