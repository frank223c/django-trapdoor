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

    def test_run_command(self):
        call_command('remove_banned_ips_older_then_by_days', 0, verbosity=0, interactive=False)
        self.assertEqual(models.BannedIP.objects.all().count(), 0)

    def test_run_command_with_negative_days(self):
        try:
            call_command('remove_banned_ips_older_then_by_days', -2, verbosity=0, interactive=False)
        except Exception as e:
            self.assertEqual(models.BannedIP.objects.all().count(), 1)
