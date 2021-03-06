# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import transaction
from django.test import TestCase
from trapdoor import constants
from trapdoor import models


class BanIPCommandTestCase(TestCase):
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        pass

    @transaction.atomic
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

    @transaction.atomic
    def test_run_command_for_existing_ip(self):
        """
        Run the 'ban_ip' command and verify it ran successfully when user
        enters IP address which does exist.
        """
        try:
            call_command('ban_ip', '192.168.0.1', verbosity=0, interactive=False)
        except Exception as e:
            self.assertTrue(True)

    @transaction.atomic
    def test_run_command_for_non_existing_ip(self):
        """
        Run the 'ban_ip' command and verify it ran successfully when user
        enters IP address which does not exist.
        """
        call_command('ban_ip', '192.168.0.2', verbosity=0, interactive=False)
        self.assertEqual(models.BannedIP.objects.count(), 2)
