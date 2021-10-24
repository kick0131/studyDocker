# Fargate+ECS

## 用語

| 単語 | 略称 | 意味 |
| -- | -- | -- |
| ECS | Elastic Container Service | Dockerコンテナの起動サービス
| ECR | Elastic Container Registory | Dockerイメージの登録サービス
| EKS | Elastic Kubernetis Service |

## 準備

- ECS用のDockerfileを作成

## ECRにイメージを登録

### ECRにログイン
```
aws ecr get-login-password --profile xxxx | docker login --username AWS --password-stdin 504534391617.dkr.ecr.ap-northeast-1.amazonaws.com
```

### ECRにログイン

- Dockerイメージ作成
    ```
    docker build -t 504534391617.dkr.ecr.ap-northeast-1.amazonaws.com/ecrsample:latest .
    ```
    - ecrsampleはイメージ名
    - タグ名は必ず「イメージ名:バージョン」
    - 例はプライベートリポジトリの場合

- ECRにプッシュ
    ```
    docker push 504534391617.dkr.ecr.ap-northeast-1.amazonaws.com/ecrsample:latest
    ```

- ECRからプル
    ```
    docker pull 504534391617.dkr.ecr.ap-northeast-1.amazonaws.com/ecrsample:latest
    ```

- ECRからイメージの削除
    ```
    aws ecr batch-delete-image --profile xxxx --repository-name ecrsample --image-ids imageTag=latest
    ```

- コンテナ実行
    ```
    docker container run -it --rm 504534391617.dkr.ecr.ap-northeast-1.amazonaws.com/ecrsample
    ```

## ECS

## Fargate


## 備考

### プライベートレジストリのURL
`https://aws_account_id.dkr.ecr.region.amazonaws.com`
