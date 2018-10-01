import six

# from django.views.generic import TemplateView
# from django.views.generic import FormView
# from django.http.response import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.utils import timezone

import logging
import datetime
# import dandan

# from words import models
# from words import functions
from words import statistics

logger = logging.getLogger("words")


class ComingView(ListView):

    template_name = "statistics/coming.html"
    paginate_by = 20
    context_object_name = "items"

    def get_queryset(self):
        return statistics.get_coming(user=self.request.user)


class LevelView(ListView):

    template_name = "statistics/level.html"
    paginate_by = 40
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super(LevelView, self).get_context_data(**kwargs)
        level = self.get_level()
        context["level"] = level
        context["title"] = "{} {}".format(_("Level"), level)
        if level:
            context["reviewlist"] = True
            self.template_name = "found/wordlist.html"
        else:
            self.template_name = "statistics/level.html"
        return context

    def get_level(self):
        return self.kwargs.get("level")

    def get_queryset(self):
        if not self.get_level():
            return statistics.get_level_count(user=self.request.user)
        else:
            return statistics.get_level(user=self.request.user, level=self.get_level())


class ErrorView(ListView):

    template_name = "statistics/error.html"
    paginate_by = 40
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        error = self.get_error()
        context["error"] = error
        context["title"] = "{} {}".format(_("Error"), error)
        if error:
            context["reviewlist"] = True
            self.template_name = "found/wordlist.html"
        else:
            self.template_name = "statistics/error.html"
        return context

    def get_error(self):
        return self.kwargs.get("error")

    def get_queryset(self):
        if not self.get_error():
            return statistics.get_error_count(user=self.request.user)
        else:
            return statistics.get_error(user=self.request.user, error=self.get_error())


class DateView(ListView):

    template_name = "statistics/date.html"
    paginate_by = 30
    context_object_name = "items"

    date = timezone.now().date()

    def get_context_data(self, **kwargs):
        context = super(DateView, self).get_context_data(**kwargs)
        context["date"] = self.get_date()
        context["date_count"] = statistics.get_date_count(self.get_date())
        return context

    def get_date(self):
        today = timezone.localtime(timezone.now()).date()
        date = self.kwargs.get("date", today)
        if isinstance(date, six.string_types):
            try:
                return timezone.datetime.strptime(date, "%Y-%m-%d").date()
            except Exception:
                pass
        if type(date) == datetime.date:
            return date
        return today

    def get_queryset(self):

        return statistics.get_date(date=self.get_date(), user=self.request.user)


class CountView(ListView):

    template_name = "statistics/count.html"
    paginate_by = 20
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super(CountView, self).get_context_data(**kwargs)
        context["all_word_count"] = statistics.get_word_count()
        context["all_review_count"] = statistics.get_review_count(user=self.request.user)
        return context

    def get_queryset(self):
        return statistics.get_count(user=self.request.user)
