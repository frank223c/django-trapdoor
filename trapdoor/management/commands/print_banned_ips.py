# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from trapdoor.models import BannedIP


class Command(BaseCommand):
    help = _('Command prints all the banned IP addresses to the console.')

    def handle(self, *args, **options):
        for ip_address in BannedIP.objects.all():
            print(ip_address)
