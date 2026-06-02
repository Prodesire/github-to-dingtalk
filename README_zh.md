# GitHub to DingTalk

将 GitHub 仓库 Webhook 事件转发到钉钉群聊。

## 快速开始

1. 安装 [uv](https://docs.astral.sh/uv/) 并安装依赖：

```shell
make install
```

2. 在钉钉群添加自定义机器人（安全设置选"加签"），配置环境变量：

```shell
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=xxx"
export DINGTALK_SECRET="SECxxx"
```

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

## 支持的事件

- discussion / discussion_comment
- fork
- issues / issue_comment
- pull_request / pull_request_review / pull_request_review_comment
- push
- star
- watch

## 截图

![](github-notifier-snapshot.jpg)

## 许可

[MIT](LICENSE)
