# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BannedIPManager(models.Manager):
    pass


class BannedIP(models.Model):
    objects = BannedIPManager()
    id = models.BigAutoField(primary_key=True)
    address = models.GenericIPAddressField(
        _('Address'),
        help_text=_('The IP address that is banned.'),
        db_index=True,
        unique=True
    )
    is_real_address = models.BooleanField(
        _("Is Real Address"),
        help_text=_('Indicates whether the "ipware" detected this IP address is real or not.'),
        default=True, # Assume it's true unless proven wrong.
        blank=True
    )
    suspicious_path = models.CharField(
        _('Suspicious Path'),
        help_text=_('The the suspicious path that was accessed by the IP address.'),
        max_length=127,
        blank=True,
        null=True
    )
    note = models.CharField(
        _('Note'),
        help_text=_('Any notes associated with this IP address.'),
        max_length=255,
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        _('Banned On'),
        help_text=_('The date this IP address was banned on.'),
        auto_now_add=True,
        db_index=True
    )
    last_modified = models.DateTimeField(
        _('Last Modified'),
        help_text=_('The date this object was last modified.'),
        auto_now=True
    )
    meta = models.CharField(
        _('Meta'),
        help_text=_('Meta information associated with this banned IP address.'),
        max_length=511,
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'trapdoor'
        ordering = ('-created',)  # Ordered by latest creation date.
        db_table = 'trapdoor_banned_ips'
        verbose_name = _('Banned IP')
        verbose_name_plural = _('Banned IPs')

    def __str__(self):
        return str(self.address)
