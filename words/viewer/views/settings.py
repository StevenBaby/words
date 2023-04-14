# coding=utf-8
import os
import logging
import dandan
import threading

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.conf import settings as djsettings
from django.utils.translation import ugettext_lazy as _

from words import models
from words import functions
from viewer import updater
from viewer import forms

logger = logging.getLogger("words")

settings = None


def save_settings():
    global settings
    dandan.value.put_json(settings, djsettings.SETTINGS_PATH, indent=4)


def initialize():
    # logger.debug("initialize for settings")
    global settings
    json = dandan.value.get_json(djsettings.SETTINGS_PATH) or {}
    settings = dandan.value.AttrDict(json)
    if not settings.phonetic:
        settings.phonetic.downloading = False
        settings.phonetic.value = 0
        try:
            settings.phonetic.total = models.Word.objects.count()
        except Exception:
            settings.phonetic.total = 0

    settings.updater.status = 'none'  # "none", "check", "updating"
    settings.updater.updating.status = "none"  # none, downloading, extracting
    settings.updater.updating.total = 0
    settings.updater.updating.value = 0

    save_settings()
    return settings


settings = initialize()


class SettingsView(FormView):

    template_name = 'settings/settings.html'
    form_class = forms.UserProfileForm
    success_url = reverse_lazy('settings')

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        settings.phonetic.total = models.Word.objects.count()
        context['phonetic_downloading'] = settings.phonetic.downloading
        context['phonetic_download_total'] = settings.phonetic.total
        context['phonetic_download_value'] = settings.phonetic.value
        context['backups'] = [os.path.basename(var) for var in functions.get_backups()]

        context["updater_status"] = settings.updater.status
        if settings.updater.status == "check":
            latest = updater.get_lastest()
            context['updater_latest'] = latest.version
            context['updater_reason'] = latest.reason

            settings.updater.status = 'none'
        elif settings.updater.status == 'updating':
            context['updating_status'] = settings.updater.updating.status
            context['updating_total'] = settings.updater.updating.total
            context['updating_value'] = settings.updater.updating.total

        return context

    def get_form_kwargs(self):
        kwargs = super(SettingsView, self).get_form_kwargs()
        kwargs["instance"] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.save()
        # logger.debug(form)
        return JsonResponse({
            "success": True,
            "description": _("Save success"),
        })

    def form_invalid(self, form):
        logger.debug("invalid form %s", form)
        return super().form_invalid(form)


class SettingsPhoneticView(TemplateView):

    thread = None

    def download_task(self):
        logger.info("phonetic download task start.")
        settings.phonetic.total = models.Word.objects.count()
        settings.phonetic.value = 0
        for review in models.Review.objects.all().order_by("review_time"):
            settings.phonetic.value += 1
            logger.info('downloading %s', review.word)
            functions.download_word(review.word)
            if not settings.phonetic.downloading:
                logger.info("phonetic download task stoped.")
                break

        settings.phonetic.downloading = False
        save_settings()
        logger.info("phonetic download task finish.")

    def get_action(self):

        return self.kwargs.get("action")

    def download(self):
        if not settings.phonetic.downloading:
            settings.phonetic.downloading = True
            self.thread = threading.Thread(target=self.download_task)
            self.thread.setDaemon(True)
            self.thread.start()
        return HttpResponseRedirect(reverse_lazy("settings"))

    def stop(self):
        if settings.phonetic.downloading:
            settings.phonetic.downloading = False
        return HttpResponseRedirect(reverse_lazy("settings"))

    def status(self):
        data = {
            "downloading": settings.phonetic.downloading,
            "total": settings.phonetic.total,
            "value": settings.phonetic.value,
            "percent": 0,
        }
        if settings.phonetic.total > 0:
            data["percent"] = int(settings.phonetic.value * 100.0 / settings.phonetic.total) or 1
        return JsonResponse(data)

    def render_to_response(self, context, **response_kwargs):
        if self.get_action() == "download":
            return self.download()
        elif self.get_action() == 'stop':
            return self.stop()
        elif self.get_action() == 'status':
            return self.status()
        return HttpResponseRedirect(reverse_lazy("settings"))


class SettingsBackupView(TemplateView):

    def get_action(self):

        return self.kwargs.get("action")

    def backup(self):
        backupname = os.path.basename(functions.backup())
        if not self.request.is_ajax():
            return HttpResponseRedirect(reverse_lazy("settings"))
        return JsonResponse({
            "success": True,
            "action": 'restore',
            "description": _("Backup {} success.").format(backupname),
        })

    def restore(self):
        # logger.debug("restore ajax {}".format(self.request.is_ajax()))
        basename = self.request.GET.get("backup_name", "").strip()
        filename = os.path.join(djsettings.BACKUP_PATH, basename)
        if not os.path.exists(filename) and not self.request.is_ajax():
            return HttpResponseRedirect(reverse_lazy("settings"))

        if not os.path.exists(filename) and self.request.is_ajax():
            return JsonResponse({
                "success": False,
                "action": 'restore',
                "description": _("Restore file does not exists."),
            })
        functions.restore(filename)
        if self.request.is_ajax():
            return JsonResponse({
                "success": True,
                "action": 'restore',
                "description": _("Restore {} success.").format(basename),
            })
        return HttpResponseRedirect(reverse_lazy("settings"))

    def render_to_response(self, context, **response_kwargs):
        if self.get_action() == 'backup':
            return self.backup()
        elif self.get_action() == 'restore':
            return self.restore()
        return HttpResponseRedirect(reverse_lazy("settings"))


class SettingsUpdateView(TemplateView):

    def update_callback(self, status, total, value):
        pass

    def update_task(self):
        updater.update(json_settings=settings)
        settings.updater.status = 'none'

    def get_action(self):

        return self.kwargs.get("action")

    def check(self):
        settings.updater.status = 'check'
        return HttpResponseRedirect(reverse_lazy("settings"))

    def update(self):
        if settings.updater.status == 'updating':
            return HttpResponseRedirect(reverse_lazy("settings"))

        settings.updater.status = 'updating'
        self.thread = threading.Thread(target=self.update_task)
        self.thread.setDaemon(True)
        self.thread.start()
        return HttpResponseRedirect(reverse_lazy("settings"))

    def status(self):
        data = {
            "updating": settings.updater.status == "updating",
            "status": settings.updater.updating.status,
            "total": settings.updater.updating.total,
            "value": settings.updater.updating.value,
            "percent": 0,
        }
        if settings.updater.updating.total > 0:
            data["percent"] = int(settings.updater.updating.value * 100.0 / settings.updater.updating.total) or 1
        logger.debug(data)
        return JsonResponse(data)

    def render_to_response(self, context, **response_kwargs):
        if self.get_action() == 'check':
            return self.check()
        elif self.get_action() == 'update':
            return self.update()
        elif self.get_action() == 'status':
            return self.status()
        return HttpResponseRedirect(reverse_lazy("settings"))
