# ElasticSearchサンプル
https://qiita.com/kiyokiyo_kzsby/items/344fb2e9aead158a5545

環境変数(事前に設定)
項目  |  説明
--- | --- |
ES_ENDPOINT     | Elasticsearch接続ホスト
INDEX       | インデックス

# 立ち上げ
### イメージ作成
```bash
# イメージ作成
docker-compose build
# コンテナ起動
docker-compose up -d
# ヘルスチェック
curl http://${ES_ENDPOINT}
```

# トラブルシュート
## Dockerの起動に失敗する
vm.max_map_countがデフォルト値では不足している

WLS上のUbuntuで以下コマンドを実行する
```
sysctl -w vm.max_map_count=262144
```
