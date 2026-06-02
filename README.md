# GitHub to DingTalk

Forward GitHub webhook events to DingTalk group chat.

[中文文档](README_zh.md)

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) and dependencies:

```shell
make install
```

2. Configure DingTalk robot (add a custom robot with "Signature" security setting):

```shell
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=xxx"
export DINGTALK_SECRET="SECxxx"
```

3. Install [Serverless Devs](https://docs.serverless-devs.com/) (`s` CLI) and deploy to Alibaba Cloud FC:

```shell
make deploy
```

4. Use the FC public URL as your GitHub repository's webhook URL.

## Development

```shell
make dev       # Dev server with hot reload
make test      # Run tests
make lint      # Linting & type checking
make format    # Format code
```

## Supported Events

- discussion / discussion_comment
- fork
- issues / issue_comment
- pull_request / pull_request_review / pull_request_review_comment
- push
- star
- watch

## Screenshot

![](github-notifier-snapshot.jpg)

## License

[MIT](LICENSE)
