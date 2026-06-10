# GitHub to DingTalk

将 GitHub 仓库 Webhook 事件转发到钉钉群聊。

## 特性

- 不同事件路由到不同钉钉群
- 支持 `event.action` 路由（如 `release.published`）
- 为 issue assignees、PR assignees 和 PR reviewers @ 映射的钉钉用户
- 基于 YAML 配置，支持多群组
- 部署到阿里云函数计算

## 快速开始

1. 安装 [uv](https://docs.astral.sh/uv/) 并安装依赖：

```shell
make install
```

2. 创建 `config.yml`（参考 [config.example.yml](config.example.yml)）：

```yaml
dingtalk_groups:
  dev-group:
    webhook: "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    secret: "YOUR_SECRET"
  release-group:
    webhook: "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    secret: "YOUR_SECRET"

routes:
  - repo: "myorg/my-repo"
    events: ["issues", "pull_request", "push"]
    groups: ["dev-group"]
  - repo: "myorg/my-repo"
    events: ["release.released"]
    groups: ["release-group"]

mentions:
  issue_assignees: true
  pull_request_assignees: true
  pull_request_reviewers: true
  issue_comment_authors: true
  github_to_dingtalk_ids:
    dev1: "DINGTALK_USER_ID_OF_DEV1"
    reviewer1: "DINGTALK_USER_ID_OF_REVIEWER1"

# default_group: "dev-group"
```

`mentions.github_to_dingtalk_ids` 用于配置 GitHub login 到钉钉用户 ID
的映射。未配置映射的 GitHub 用户仍会正常发送通知，但不会 @ 该用户。
对于 `issue_comment.created` 和 `pull_request_review_comment.created`，
`issue_comment_authors` 会 @ issue/PR 作者、评论正文中显式 @ 的已映射
用户。对于 `issue_comment.created`，还会在能够匹配 Quote reply 时尽量
@ 被引用评论的作者。

3. 安装 [Serverless Devs](https://docs.serverless-devs.com/)（`s` 命令行工具），部署到阿里云函数计算：

```shell
make deploy
```

4. 将 FC 公网地址作为 GitHub 仓库的 Webhook URL。

## 开发

```shell
make dev       # 启动开发服务器（热重载）
make test      # 运行测试
make lint      # 代码检查与类型检查
make format    # 格式化代码
```

## 截图

![](github-notifier-snapshot.jpg)

## 许可

[MIT](LICENSE)
