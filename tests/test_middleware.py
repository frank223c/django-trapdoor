# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.test import TestCase
from django.test import Client
from django.test import override_settings
from django.test.client import RequestFactory
from trapdoor import constants
from trapdoor import models


class TrapdoorMiddlewareTestCase(TestCase):
    """
    Unit test suite for the "TrapdoorMiddleware" middelware class.
    """
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

    def test_non_suspicious_request(self):
        """
        Test & verify banning does not happen.
        """
        c = Client()
        response = c.get('/admin/')

        # Verify we did not get banned.
        self.assertNotEqual(response.status_code, 403)

    def test_ban_suspicious_request(self):
        """
        Test & verify banning happens.
        """
        c = Client()
        response = c.get('/admin/config.php')

        # Verify we did not get banned.
        self.assertEqual(response.status_code, 403)

    def test_block_suspicious_request(self):
        """
        Test & verify blocking is enforced after banning happens.
        """
        c = Client()
        response = c.get('/admin/config.php')

        # Verify we did not get banned.
        self.assertEqual(response.status_code, 403)

        response = c.get('/admin/config.php')
        # Verify we did not get banned.
        self.assertEqual(response.status_code, 403)

    @override_settings(TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES=['127.0.0.1',])
    def test_settings_variable1_with_request(self):
        """
        Test & verfiy "TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES" settings variable works.
        """
        c = Client()
        try:
            response = c.get('/admin/config.php')
        except Exception as e:
            pass  # Prevent any errors.

        # Verify we did not get banned and that a 404 is returned, because
        # we do not have that URL!.
        self.assertEqual(response.status_code, 404)

    @override_settings(TRAPDOOR_EXTRA_SUSPICIOUS_PATHS=['/api/security',])
    def test_settings_variable2_with_request(self):
        """
        Test & verfiy "TRAPDOOR_EXTRA_SUSPICIOUS_PATHS" settings variable works.
        """
        c = Client()
        response = c.get('/api/security')

        # Verify we did not get banned and that a 404 is returned, because
        # we do not have that URL!.
        self.assertEqual(response.status_code, 403)
