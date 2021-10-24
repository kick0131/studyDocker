## for WSL(Ubuntu)
デフォルトのエディタをnanoから変更
```
update-alternatives --config editor
```

コミットログをvimに変更
```
git config --global core.editor 'vim -c "set fenc=utf-8"'
```

## docker コマンド
起動中のコンテナに入る
```
docker exec -it <container id> /bin/bash
```

起動停止
```
docker-compose up
docker-compose down
```

## docker-compose書式
コンテナを起動したままにする
```
tty : true
```

## 参考URL
[The Compose Specification](https://github.com/compose-spec/compose-spec/blob/master/spec.md)

[docker-composeで作成されるものの名前を明示的に指定する方法](https://qiita.com/satodoc/items/188a387f7439e4ec394f)

