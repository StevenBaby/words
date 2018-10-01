# coding=utf-8
'''
Word ORM definition
'''
from __future__ import print_function, unicode_literals, division

import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_init
from django.dispatch import receiver

import logging

logger = logging.getLogger('words')

# Create your models here.


class WordType(models.Model):
    content = models.CharField(
        max_length=16,
        verbose_name=_('WordType'),)

    class Meta:
        verbose_name = _('WordType')
        verbose_name_plural = _('WordTypes')

    def __str__(self):
        return self.content


class Word(models.Model):
    type = models.ForeignKey(to=WordType, verbose_name=_('WordType'), on_delete=models.CASCADE)
    equals = models.ManyToManyField(to="self", verbose_name=_('Equal word'), symmetrical=True)
    similars = models.ManyToManyField(to="self", verbose_name=_('Similar word'), symmetrical=True)
    relateds = models.ManyToManyField(to="self", verbose_name=_('Related word'), symmetrical=True)

    create_time = models.DateTimeField(
        verbose_name=_("Create Time"),
        default=timezone.now)

    refresh_time = models.DateTimeField(
        verbose_name=_("Refresh Time"),
        default=timezone.now)

    title = models.TextField(
        verbose_name=_("Title"),
        unique=True,
    )

    star = models.IntegerField(
        verbose_name=_("Star"),
        default=0,
    )

    def paraphrases(self):
        result = {}
        for para in self.paraphrase.all():
            result.setdefault(para.type.content, [])
            result[para.type.content].append(para.content)
        for type in result.keys():
            result[type] = "，".join(result[type])
        return [[var[0], var[1]] for var in result.items()]

    class Meta:
        verbose_name = _('Word')
        verbose_name_plural = _('Words')
        get_latest_by = 'id'
        indexes = [
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return self.title


class ParaType(models.Model):
    content = models.CharField(
        max_length=16,
        verbose_name=_('ParaType'),)

    class Meta:
        verbose_name = _('ParaType')
        verbose_name_plural = _('ParaTypes')

    def __str__(self):
        return self.content


class Paraphrase(models.Model):
    type = models.ForeignKey(to=ParaType, verbose_name=_('ParaType'), on_delete=models.CASCADE)
    word = models.ForeignKey(to=Word, verbose_name=_("Word"), related_name='paraphrase', on_delete=models.CASCADE)
    content = models.TextField(verbose_name=_("Content"))

    class Meta:
        verbose_name = _('Paraphrase')
        verbose_name_plural = _('Paraphrases')

    def __str__(self):
        return "{}.{}".format(str(self.type), self.content)


class PhoneticType(models.Model):
    content = models.CharField(
        max_length=16,
        verbose_name=_('PhoneticType'),
        default="NO")

    class Meta:
        verbose_name = _('PhoneticType')
        verbose_name_plural = _('PhoneticTypes')

    def __str__(self):
        return self.content


class Phonetic(models.Model):
    type = models.ForeignKey(to=PhoneticType, verbose_name=_('PhoneticType'), on_delete=models.CASCADE)
    word = models.ForeignKey(to=Word, verbose_name=_("Word"), related_name='phonetic', on_delete=models.CASCADE)
    content = models.CharField(
        max_length=256,
        verbose_name=_('Phonetic'),
        null=True)

    @property
    def filename(self):
        title = self.word.title
        if self.type.content == "UK":
            dirname = settings.PHONETIC_PATH_UK
        elif self.type.content == "US":
            dirname = settings.PHONETIC_PATH_US
        return os.path.join(dirname, "{title}_.mp3".format(title=title))

    class Meta:
        verbose_name = _('Phonetic')
        verbose_name_plural = _('Phonetics')

    def __str__(self):
        return "{} {}".format(str(self.type), self.content)


class Rank(models.Model):
    content = models.CharField(
        max_length=16,
        verbose_name=_('Rank'),)

    word = models.ManyToManyField(
        to=Word,
        verbose_name=_("Word"),
        related_name='ranks')

    class Meta:
        verbose_name = _('Rank')
        verbose_name_plural = _('Ranks')

    def __str__(self):
        return self.content


class Review(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name=_('User'),
        related_name="review",
        on_delete=models.CASCADE
    )

    word = models.ForeignKey(
        to=Word,
        verbose_name=_('Word'),
        related_name="review",
        on_delete=models.CASCADE
    )

    first_time = models.DateTimeField(
        verbose_name=_("First Time"),
        default=timezone.now)

    update_time = models.DateTimeField(
        verbose_name=_("Update Time"),
        default=timezone.now)

    review_time = models.DateTimeField(
        verbose_name=_("Review Time"),
        default=timezone.now)

    hard_time = models.DateTimeField(
        verbose_name=_("Hard Time"),
        default=timezone.now)

    hard = models.IntegerField(
        verbose_name=_("Hard mark"),
        default=0,
    )

    level = models.IntegerField(
        verbose_name=_("Review level"),
        default=0,
    )

    times = models.IntegerField(
        verbose_name=_("Review times"),
        default=0,
    )

    right = models.IntegerField(
        verbose_name=_("Review right times"),
        default=0,
    )

    skip = models.IntegerField(
        verbose_name=_("Review skip times"),
        default=0,
    )

    error = models.IntegerField(
        verbose_name=_("Review error times"),
        default=0,
    )

    review = models.IntegerField(
        verbose_name=_("Review status"),
        default=0,
    )

    reset = models.IntegerField(
        verbose_name=_("Reset times"),
        default=0,
    )

    def __str__(self):
        return "[{word}] [{level:02}] [F {first_time}] [U {update_time}] [R {review_time}]".format(
            word=str(self.word),
            level=self.level,
            first_time=timezone.localtime(self.first_time).strftime(settings.DATETIME),
            update_time=timezone.localtime(self.update_time).strftime(settings.DATETIME),
            review_time=timezone.localtime(self.review_time).strftime(settings.DATETIME),
        )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        unique_together = (("user", "word"),)


class UserProfile(models.Model):
    user = models.OneToOneField(
        to=User,
        verbose_name=_('User'),
        related_name="profile",
        on_delete=models.CASCADE)

    STUDY_MODE_CHOICES = (
        (0, _("Random")),
        (1, _("Dictation")),
        (2, _("Paraphrase")),
    )
    settings_study_mode = models.IntegerField(
        default=0,
        verbose_name=_('Settings Study Mode'),
        choices=STUDY_MODE_CHOICES)

    settings_alert_delete_word = models.BooleanField(
        default=True,
        verbose_name=_('Settings Alert Delete Word')
    )

    settings_alert_delete_review = models.BooleanField(
        default=True,
        verbose_name=_('Settings Alert Delete Review')
    )

    settings_alert_delete_paraphrase = models.BooleanField(
        default=True,
        verbose_name=_('Settings Alert Delete Paraphrase')
    )

    settings_alert_reset_review = models.BooleanField(
        default=True,
        verbose_name=_('Settings Alert Reset Review')
    )

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfiles')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    instance.profile.save()


@receiver(post_init, sender=User)
def init_user_profile(sender, instance, **kwargs):

    if not hasattr(instance, "profile") and instance.id:
        instance.save()
