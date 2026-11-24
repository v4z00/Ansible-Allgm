"""Aggregate Ansible play completion without logging inventory or task data."""
from ansible.plugins.callback import CallbackBase
import json
import os


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "aggregate"
    CALLBACK_NAME = "extension_receipt"
    CALLBACK_NEEDS_ENABLED = True

    def __init__(self):
        super().__init__()
        self.plays = []

    def v2_playbook_on_play_start(self, play):
        self.plays.append(False)

    def v2_runner_on_ok(self, result):
        if self.plays and result._task.action.split(".")[-1] not in ("gather_facts", "setup"):
            self.plays[-1] = True

    def v2_playbook_on_stats(self, stats):
        if self.plays and all(self.plays) and not stats.failures and not stats.dark:
            with open(os.environ["LOCAL_EXTENSION_RESULT"], "x", encoding="utf8") as stream:
                json.dump({"completed_plays": len(self.plays)}, stream)
