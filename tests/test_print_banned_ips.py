# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from trapdoor import constants
from trapdoor import models


class PrintBannedIPCommandTestCase(TestCase):
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.banned_ip = models.BannedIP.objects.create(
            address="192.168.0.1",
            suspicious_path='/wp-login.php',
            note="This is for unit test."
        )

    def tearDown(self):
        User.objects.all().delete()
        if self.banned_ip:
            self.banned_ip.delete()

    def test_run_command_for_existing_ip(self):
        """
        Run the 'unban_ip' command and verify it ran successfully when user
        enters IP address which does exist.
        """
        call_command('print_banned_ips', verbosity=0, interactive=False)
