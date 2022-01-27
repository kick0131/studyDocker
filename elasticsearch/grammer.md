# 共通文法
ElasticSearch,OpenSearch共通の話題はここに

## Index作成
インデックス名"Amazon"を例に
```
curl -X PUT "localhost:9200/amazon?pretty"
curl -X PUT "${ES_ENDPOINT}/${INDEX}?pretty"
```

## マッピングの作成
以下構成とする
名称      | 論理名 | 型
--- | --- | --- |
日付      |date | date
タグ      |tag  | str
ポート番号|port | int


### date型
date型の一覧は[こちら](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#strict-date-time)を参照

項目 | 書式
--- | ---
date_optional_time | yyyy-MM-dd'T'HH:mm:ss.SSSZ ※
strict_date_optional_time | yyyy-MM-dd'T'HH:mm:ss.SSSZ ※
strict_date_optional_time_nanos | yyyy-MM-dd'T'HH:mm:ss.SSSSSSZ ※
basic_date | yyyyMMdd
basic_date_time | yyyyMMdd'T'HHmmss.SSSZ
basic_date_time_no_millis | yyyyMMdd'T'HHmmssZ
※ 'yyyy-MM-dd'も利用可能


---
### マッピングの投入
mapping.jsonファイルに定義を記載

```
{
  "properties": {
    "tag":    { "type": "text" },
    "port":      { "type": "integer" },
    "date":  {
      "type":   "date",
      "format": "strict_date_optional_time||epoch_millis"
    }
  }
}
```

- バージョンアップでタイプレスとなり、include_type_nameが必要となった。詳細は[こちら](https://www.elastic.co/jp/blog/moving-from-types-to-typeless-apis-in-elasticsearch-7-0)
```
curl -XPUT "${ES_ENDPOINT}/${INDEX}/_mapping/_doc?include_type_name=true" -H 'Content-Type: application/json' --data-binary @mapping.json
```


### データ投入
```
curl -X PUT "localhost:9200/amazon/_doc/companyInfo?pretty&pretty" -H "Content-Type: application/json" -d "{\"founder\": \"Jeffrey Preston Bezos\"}"
```
- インデックスに大文字不可

## bulk API
### 準備
投入ファイルを用意
- create

1行目:API {<命令>: {"_index": <インデックス>, "_type":"_doc", "_id":<ユニーク値>}}  
2行目:投入データ
```
{"index": {"_index":"${INDEX}", "_type":"_doc", "_id":"1"}}
{"tag":"name0", "port":10, "createdAt":"2020-08-01T01:00:00.100"}
{"index": {"_index":"${INDEX}", "_type":"_doc", "_id":"2"}}
{"tag":"name1", "port":11, "createdAt":"2020-08-01T02:00:00.200"}
```

### 実行
```
curl -s -H "Content-Type: application/x-ndjson" -XPOST "${ES_ENDPOINT}/_bulk?pretty" --data-binary @bulk_insert.json
```

## search API
コマンドプロンプトから改行ありで実行
```bash
curl -X GET "localhost:9200/amazon/_search?pretty" -H "Content-Type: application/json" -d ^
"{^
    \"query\": {^
        \"match_all\": {}^
    }^
}"
```

### DEV Tool
REST APIをGUI上から実行するKibana(OpenSearchDashboards)のツール  
REST APIのパス以降の部分を記載する点が楽
```bash
# データ投入
# 投入時のタイムスタンプは【JST】なので注意、表示は【UTC】
POST /hoge/_doc/
{
  "key1": {
    "key1-1": "hoge",
    "key1-2": 11
  },
  "timestamp": "2022-01-27T05:41:00.000Z"
}
# 時間範囲検索
GET /hoge/_search
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "2022-01-27T00:00:00+09:00",
        "lte": "2022-01-29T00:00:00+09:00",
        "format": "date_time_no_millis"
      }
    }
  }
}
```

# トラブルシュート
## Dockerの起動に失敗する
vm.max_map_countがデフォルト値では不足している

WLS上のUbuntuで以下コマンドを実行する
```
sysctl -w vm.max_map_count=262144
```
