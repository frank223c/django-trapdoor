# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from trapdoor import constants
from trapdoor import models


class RemoveBannedIPCommandTestCase(TestCase):
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
        call_command('remove_banned_ip', '192.168.0.1', verbosity=0, interactive=False)
        self.assertEqual(models.BannedIP.objects.count(), 0)

    def test_run_command_for_non_existing_ip(self):
        """
        Run the 'unban_ip' command and verify it ran successfully when user
        enters IP address which does not exist.
        """
        try:
            call_command('remove_banned_ip', '10.10.10.1', verbosity=0, interactive=False)
        except Exception as e:
            self.assertIn(str(e), 'Inputted IP address is not banned.')
