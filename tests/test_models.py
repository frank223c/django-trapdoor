# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
from django.test import TestCase
from trapdoor import constants
from trapdoor import models


class ModelsTestCase(TestCase):
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
        if self.banned_ip:
            self.banned_ip.delete()

    def test_to_string(self):
        """
        Test & verify the "__str__" function works.
        """
        self.assertIsNotNone(self.banned_ip)
        self.assertEqual(str(self.banned_ip), "192.168.0.1")
