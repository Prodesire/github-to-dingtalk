import logging

import conf
from dingtalkchatbot.chatbot import DingtalkChatbot


class DingTalkNotifier(object):

    def __init__(self, payload: dict):
        self.payload = payload
        self.action = self.payload.get('action')
        self.action_prep = 'to' if self.action in ('created', 'opened', 'submitted', None) else 'of'
        self.sender = sender = payload.get('sender') or {}
        self.sender_full_name = sender.get('login')
        self.sender_page = sender.get('html_url')
        self._md_sender = f'[{self.sender_full_name}]({self.sender_page})'
        self.repo = repo = payload.get('repository') or {}
        self.repo_full_name = repo.get('full_name')
        self.repo_page = repo.get('html_url')
        self.repo_language = repo.get('language')
        self.repo_star_count = repo.get('stargazers_count')
        self._md_repo = f'[{self.repo_full_name}]({self.repo_page})'
        self.bot = DingtalkChatbot(conf.webhook, conf.secret)

    def notify(self):
        logging.info(f'Preparing notification: {self.payload}')
        if 'pull_request' in self.payload:
            self._notify_pull_request()
        elif 'head_commit' in self.payload:
            self._notify_push()
        elif 'issue' in self.payload:
            self._notify_issue()
        elif 'starred_at' in self.payload:
            self._notify_star()
        elif 'forkee' in self.payload:
            self._notify_fork()
        elif 'discussion' in self.payload:
            self._notify_discussion()

    def _notify_pull_request(self):
        pr = self.payload['pull_request']
        pr_page = pr['html_url']
        pr_number = pr['number']
        pr_title = pr['title']
        pr_body = pr['body'] or ''
        review = self.payload.get('review')
        comment = self.payload.get('comment')
        if review:
            pr_review_page = review['html_url']
            review_body = review['body'] or ''
            self.bot.send_markdown(
                title='Pull Request Review',
                text=f'{self._md_sender} has {self.action} a pull request review {self.action_prep} {self._md_repo}\n\n'
                     f'[#{pr_number} {pr_title}]({pr_review_page})\n\n'
                     f'> {review_body}'
            )
        elif comment:
            comment_page = comment['html_url']
            comment_body = comment['body'] or ''
            self.bot.send_markdown(
                title='Issue Comment',
                text=f'{self._md_sender} has {self.action} a pull request review comment '
                     f'{self.action_prep} {self._md_repo}\n\n'
                     f'[#{pr_number} {pr_title}]({comment_page})\n\n'
                     f'> {comment_body}'
            )
        else:
            self.bot.send_markdown(
                title='Pull Request',
                text=f'{self._md_sender} has {self.action} a pull request {self.action_prep} {self._md_repo}\n\n'
                     f'[#{pr_number} {pr_title}]({pr_page})\n\n'
                     f'> {pr_body}'
            )

    def _notify_push(self):
        head_commit = self.payload['head_commit']
        commit_id = head_commit['id']
        commit_page = head_commit['url']
        commit_message = head_commit['message']
        added = head_commit['added']
        removed = head_commit['removed']
        modified = head_commit['modified']
        md_file_changes = ''
        if added:
            md_file_changes += f'\n- Added: {",".join(added)}'
        if removed:
            md_file_changes += f'\n- Removed: {",".join(removed)}'
        if modified:
            md_file_changes += f'\n- Modified: {",".join(modified)}'
        if md_file_changes:
            md_file_changes = 'File Changes:' + md_file_changes

        self.bot.send_markdown(
            title='Issue Comment',
            text=f'{self._md_sender} has pushed commit(s) {self.action_prep} {self._md_repo}\n\n'
                 f'[#{commit_id}]({commit_page})\n\n'
                 f'> {commit_message}\n\n'
                 f'{md_file_changes}'
        )

    def _notify_issue(self):
        issue = self.payload['issue']
        issue_page = issue['html_url']
        issue_number = issue['number']
        issue_title = issue['title']
        issue_body = issue['body'] or ''
        comment = self.payload.get('comment')
        if comment:
            comment_page = comment['html_url']
            comment_body = comment['body'] or ''
            self.bot.send_markdown(
                title='Issue Comment',
                text=f'{self._md_sender} has {self.action} an issue comment {self.action_prep} {self._md_repo}\n\n'
                     f'[#{issue_number} {issue_title}]({comment_page})\n\n'
                     f'> {comment_body}'
            )
        else:
            self.bot.send_markdown(
                title='Issue',
                text=f'{self._md_sender} has {self.action} an issue {self.action_prep} {self._md_repo}\n\n'
                     f'[#{issue_number} {issue_title}]({issue_page})\n\n'
                     f'> {issue_body}'
            )

    def _notify_star(self):
        if self.action == 'created':
            self.bot.send_markdown(
                title='Star',
                text=f'{self._md_sender} starred {self._md_repo}\n\n'
                     f'⭐️{self.repo_star_count}'
            )
        elif self.action == 'deleted':
            self.bot.send_markdown(
                title='Un-Star',
                text=f'{self._md_sender} un-starred {self._md_repo}\n\n'
                     f'⭐️{self.repo_star_count}'
            )

    def _notify_fork(self):
        forkee = self.payload['forkee']
        fork_repo_full_name = forkee['full_name']
        fork_repo_page = forkee['html_url']
        md_fork = f'[{fork_repo_full_name}]({fork_repo_page})'

        self.bot.send_markdown(
            title='Fork',
            text=f'{self._md_sender} forked {md_fork} from {self._md_repo}️\n\n'
                 f'⭐️{self.repo_star_count}'
        )

    def _notify_discussion(self):
        discussion = self.payload['discussion']
        discussion_page = discussion['html_url']
        discussion_number = discussion['number']
        discussion_title = discussion['title']
        discussion_body = discussion['body'] or ''
        comment = self.payload.get('comment')
        if comment:
            comment_page = comment['html_url']
            comment_body = comment['body'] or ''
            self.bot.send_markdown(
                title='Discussion Comment',
                text=f'{self._md_sender} has {self.action} an discussion comment {self.action_prep} {self._md_repo}\n\n'
                     f'[#{discussion_number} {discussion_title}]({comment_page})\n\n'
                     f'> {comment_body}'
            )
        else:
            self.bot.send_markdown(
                title='Discussion',
                text=f'{self._md_sender} has {self.action} an discussion {self.action_prep} {self._md_repo}\n\n'
                     f'[#{discussion_number} {discussion_title}]({discussion_page})\n\n'
                     f'> {discussion_body}'
            )
