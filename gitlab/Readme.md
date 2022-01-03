# install
コンテナ起動からWebアクセス可能迄若干時間がかかる。  
その間502を応答するので気長に待つ。

## preparation
HOMEディレクトリの定義は最低限必要  
.bash_profile
```
export GITLAB_HOME=/srv/gitlab
```

## command
```
# 起動
docker-compose up -d

# 停止
docker-compose down

# コンテナにアタッチ
docker exec -it gitlab /bin/bash
```

ログインはroot、パスワードは以下コマンドで出力  
24時間経過すると自動で切り替わるらしい
```
docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```

