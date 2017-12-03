# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from trapdoor.models import BannedIP


class Command(BaseCommand):
    help = _('Inputted IP address will banned and subject to ban enforcement measure.')

    def add_arguments(self, parser):
        parser.add_argument('ip_address', nargs='+', type=str)

    def handle(self, *args, **options):
        for ip_address in options['ip_address']:
            try:
                BannedIP.objects.create(
                    address=ip_address
                )
                self.stdout.write(
                    self.style.SUCCESS(_('IP %s is now banned.') % ip_address))
            except Exception as e:
                raise CommandError(_('Inputted IP has error %s') % str(e))
