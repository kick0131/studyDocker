# jupyter Lab

## description
いつでもどこでも簡単に、がテーマ
- Docker環境でJupyterLabを立ち上げる
- ファイルはボリュームをアタッチしてその先で保存
- 開発時はローカル、本番はAWS Fargateを想定

| 環境 | コンテナ配置場所 | ボリューム配置場所 |
| ---- | ---- | ---- |
| dev  | local       | local |
| prod | AWS Fargate | AWS EFS |


```
develop
  +-----------+                    +---------------+
  | client    |                    | Docker        |
  | (browser) |                    | (jupyter LAB) |
  |           | http://localhost   |               |
  |           | -----------------> |               |
  |           |             html   |               |
  |           | <----------------- |               |
  |           |                    |               |
  | +-------+ | volume mount       | +----------+  |
  | | .note | | -----------------> | | .note    |  |
  | +-------+ |                    | +----------+  |
  +-----------+                    +---------------+

production
  +-----------+                    +---------------+
  | client    |                    | AWS Fargate   |
  | (browser) |                    | (jupyter LAB) |
  |           | http://localhost   |               |
  |           | -----------------> |               |
  |           |             html   |               |
  |           | <----------------- |               |
  +-----------+                    | +----------+  |
                                   | | .note    |  |
                                   | +----------+  |
                                   +---------------+
                                          ^
                                          | volume mount
                                   +---------------+
                                   | AWS EFS       |
                                   | +----------+  |
                                   | | .note    |  |
                                   | +----------+  |
                                   +---------------+




```

## Install
Jupyterが用意しているコンテナを利用する

- [公式](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)


# Usage
## Dockerfile
イメージをそのまま使う為、Dockerfile内では特に何もしない
```bash
# build
docker build -t jupyter .

# run
docker run -p 8888:8888 -v `pwd`:/home/jovyan/work --name jupyter jupyter/scipy-notebook
```

## Docker-Compose
```bash
# run
docker-compose up -d

# stop
docker-compose down
```

## Conatiner
```bash
# 起動中のコンテナにアタッチ
docker exec -it jupyterlab /bin/bash

# 起動URL確認
docker logs jupyterlab
```

## Notice
- コンテナ起動時、コマンドは指定しない事。デフォルトの起動コマンド推奨。
- イメージは`ディレクトリ名-イメージ名`が新たに作られる

### Environment

| Environment | description | default |
| -- | -- | -- |
| -e NB_USER=jovyan         | Jupyterユーザ名           | jovyan |
| -e GEN_CERT=yes           | HTTPSを有効にする         | no |
| -e JUPYTER_ENABLE_LAB=yes | Jupyter Labとして起動する | no |
| -e NOTEBOOK_ARGS="--log-level='DEBUG'"| jupyterに与える環境変数 | (none) |
| | | |
| | | |

# Trouble shooting
## 
## 

