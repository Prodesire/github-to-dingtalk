import json
import unittest

from notification.notifier import DingTalkNotifier


class NotificationBaseTest(unittest.TestCase):

    def _test_notify(self, payload_body: str):
        notifier = DingTalkNotifier(json.loads(payload_body))
        notifier.notify()
