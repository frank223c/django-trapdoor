# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 02:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannedIP',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('address', models.GenericIPAddressField(db_index=True, help_text='The IP address that is banned.', unique=True, verbose_name='Address')),
                ('is_real_address', models.BooleanField(default=True, help_text='Indicates whether the "ipware" detected this IP address is real or not.', verbose_name='Is Real Address')),
                ('suspicious_path', models.CharField(blank=True, help_text='The the suspicious path that was accessed by the IP address.', max_length=127, null=True, verbose_name='Suspicious Path')),
                ('note', models.CharField(blank=True, help_text='Any notes associated with this IP address.', max_length=255, null=True, verbose_name='Note')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date this IP address was banned on.', verbose_name='Banned On')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='The date this object was last modified.', verbose_name='Last Modified')),
                ('meta', models.CharField(blank=True, help_text='Meta information associated with this banned IP address.', max_length=511, null=True, verbose_name='Meta')),
            ],
            options={
                'verbose_name': 'Banned IP',
                'verbose_name_plural': 'Banned IPs',
                'db_table': 'trapdoor_banned_ips',
                'ordering': ('-created',),
            },
        ),
    ]
