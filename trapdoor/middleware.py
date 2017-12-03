# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from ipware.ip import get_real_ip, get_ip
from trapdoor import constants
from trapdoor.models import BannedIP


class TrapdoorMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

        # Assign our "TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES" settings variable.
        if hasattr(settings, 'TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES'):
            self.TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES = settings.TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES
        else:
            self.TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES = []

        # Assign our "TRAPDOOR_EXTRA_SUSPICIOUS_PATHS" settings variable.
        if hasattr(settings, 'TRAPDOOR_EXTRA_SUSPICIOUS_PATHS'):
            self.TRAPDOOR_EXTRA_SUSPICIOUS_PATHS = settings.TRAPDOOR_EXTRA_SUSPICIOUS_PATHS
        else:
            self.TRAPDOOR_EXTRA_SUSPICIOUS_PATHS = []

    def __call__(self, request):
        # Use our third party library to fetch the user's IP address.
        ip_address = get_real_ip(request)

        # Detect if we have the users REAL, public IP address for the request,
        # else we don't have the REAL public IP address so we'll have to just
        # get the IP.
        is_real_address = ip_address is not None
        if is_real_address == False:
            ip_address = get_ip(request)

        # Save the IP address to the request so the developers can use the
        # IP address in their development instead of creating their own
        # middleware.
        request.trapdoor = {
            'is_real_address': is_real_address,
            'ip_address': is_real_address
        }

        # Check if IP address is banned and deny entry if it is.
        banned = BannedIP.objects.filter(address=ip_address).exists()
        if banned:
            return HttpResponseForbidden(_('Your IP address has been banned! If you would like to dispute it, please contact the site administrator.'))

        # Accessing suspicious paths automatically bans IP address.
        if request.path in constants.SUSPICIOUS_PATHS or request.path in self.TRAPDOOR_EXTRA_SUSPICIOUS_PATHS:
            # Confirm we are allowed to ban the IP address.
            if ip_address not in self.TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES:
                BannedIP.objects.create(
                    address=ip_address,
                    is_real_address=is_real_address,
                    suspicious_path=request.path)
                return HttpResponseForbidden(_('You just got banned!'))

        # Else we have no reason to ban / enforce ban so therefore grant
        # acess to the view.
        return self.get_response(request)
