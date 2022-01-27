# OpenSearchサンプル

## Prepare
### Gmail認証情報
- Dockerfileのgmailアカウント情報を設定する(Alert機能でgmail送信を行う場合)

### ルート証明書
ダッシュボードからOpenSeachにアクセスする際にhttps接続を行うため、ルート証明書が必要
```bash
# opensearchに入り、ルート証明書のパスを特定
docker ps -a
docker exec -it ac31933aacdd /bin/bash
ll /usr/share/opensearch/config/root-ca.pem
exit

# ルート証明書をコピー
docker cp ac31933aacdd:/usr/share/opensearch/config/root-ca.pem .
```

## Let's start
```bash
# ビルド
docker-compose build --no-cache

# コンテナ起動
docker-compose up -d

# コンテナ停止
docker-compose down

# OpenSearchはREST APIで提供されるのでcurl等を使う
# ユーザ名、パスワードを指定しないとSecuritySSLNettyHttpServerTransport例外が出る
curl -k -u admin:admin https://localhost:9200/

# ダッシュボードはブラウザアクセスを行う
http://localhost:5601/
```

# Alert機能を使ったgmail送信
[公式のMonitorsの内容を見た方が良いかも](https://opensearch.org/docs/latest/monitoring-plugins/alerting/monitors/#authenticate-sender-account)

1. gmail側にIMAPの有効化と第三者からのアクセス許可が必要
1. email sendersのコメントより、keystoreの設定が必要
```bash
SSL or TLS is recommended for security. SSL and TLS requires validation by adding the following fields to the Opensearch keystore: plugins.alerting.destination.email.my_sender.username plugins.alerting.destination.email.my_sender.password
```

## Monitors/Destinations

- Sender
  送信元情報を定義、重要

  |項目|内容|
  |--|--|
  | Email address     | 送信元メールアドレス |
  | Host              | smtp.gmail.com |
  | Port              | 465 |
  | Encryption method | SSL |

- Recipients
  送信先メールアドレスを設定

## キーストアに認証情報を登録する
`★重要★`  
SMTP通信をする際に認証が必要なので、認証情報をOpenSerachサーバにキーストアとして保持しておく必要がある

キーストア用のコマンドが用意されているので、それを実行すればよい  
Dockerコンテナで適用する場合はDockerfileに定義する
```bash
# ユーザ名
./bin/opensearch-keystore add plugins.alerting.destination.email.my_sender.username 
→入力を求められる
# パスワード
./bin/opensearch-keystore add plugins.alerting.destination.email.my_sender.password
→入力を求められる
```

### keystoreファイルについて
OpenSearchサーバ側に  
/usr/share/opensearch/config/opensearch.keystore  
が存在するが中身が読み取れない  
opensearch-keystoreコマンドも使い方不明
```bash
[opensearch@9a8e83f2c458 config]$ keytool -v -list -keystore opensearch.keystore
keytool error: java.security.KeyStoreException: Unrecognized keystore format. Please load it with a specified type
java.security.KeyStoreException: Unrecognized keystore format. Please load it with a specified type
        at java.base/java.security.KeyStore.getInstance(KeyStore.java:1807)
        at java.base/java.security.KeyStore.getInstance(KeyStore.java:1680)
        at java.base/sun.security.tools.keytool.Main.doCommands(Main.java:941)
        at java.base/sun.security.tools.keytool.Main.run(Main.java:422)
        at java.base/sun.security.tools.keytool.Main.main(Main.java:415)
```

### DevToolからサーバリロード不要で設定を反映
[公式より](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-reload-secure-settings.html)
```bash
POST /_nodes/reload_secure_settings
```

## Trouble shooting
### Plugin install
コマンドはフルパスである必要がある。  
ElasticSearchはパスが通っていた
```bash
# NG
opensearch-plugin install analysis-kuromoji
# OK
/usr/share/opensearch/bin/opensearch-plugin install analysis-kuromoji
```


