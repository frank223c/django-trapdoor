# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from trapdoor.models import BannedIP
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = _('Removes banned IP address older then the inputted day count.')

    def add_arguments(self, parser):
        parser.add_argument('days', nargs='+', type=int)

    def handle(self, *args, **options):
        for days in options['days']:
            if days < 0:
                raise CommandError(_('Inputted days count cannot be negative!'))

            # Convert to timezone aware date.
            today = timezone.localtime(timezone.now())

            # Set time to be 1 hour into the past from right now.
            today_minus_some_days = today - timedelta(days=days)

            # Remove all the banned IPs that are older then the user inputted date.
            BannedIP.objects.filter(created__lte=today_minus_some_days).delete()

        self.style.SUCCESS(
            _('Banned IP addresses older then %s days have been removed from the database.') % str(days)
        )
