# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Alias, Habla, TextPost, ImagePost

admin.site.register(Habla)
admin.site.register(Alias)
admin.site.register(TextPost)
admin.site.register(ImagePost)
