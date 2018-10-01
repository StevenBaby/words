# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from words import models


admin.site.register(models.Word)
admin.site.register(models.WordType)

admin.site.register(models.ParaType)
admin.site.register(models.Paraphrase)

admin.site.register(models.PhoneticType)
admin.site.register(models.Phonetic)

admin.site.register(models.Rank)
admin.site.register(models.Review)


class ProfileInline(admin.StackedInline):
    model = models.UserProfile
    max_num = 1
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
