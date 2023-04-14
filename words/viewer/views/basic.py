# coding=utf-8
from __future__ import print_function, unicode_literals

import logging

# from django.utils import timezone
from django.urls import reverse_lazy
from django.templatetags.static import static
# from django.utils.translation import ugettext_lazy as _

from django.db.models import Q

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView

from django.http.response import JsonResponse
from django.http.response import HttpResponseNotFound
from django.http.response import HttpResponseRedirect


from utils import youdao

from words import models
from words import functions
from viewer import forms

import dandan

logger = logging.getLogger("words")


class WordlistView(FormView, ListView):
    template_name = "wordlist.html"
    paginate_by = 12
    context_object_name = "items"
    form_class = forms.FilterForm

    review = 0
    level = -1
    hard = 0

    def get_context_data(self, **kwargs):
        context = super(WordlistView, self).get_context_data(**kwargs)
        context["review"] = self.review
        context["level"] = self.level
        context["hard"] = self.hard
        context["detail"] = True
        return context

    def get_queryset(self):
        queryset = models.Word.objects.all()
        logger.info("query word count %s", queryset.count())
        reviews = models.Review.objects.filter(user=self.request.user)
        if self.review == 2:
            queryset = queryset.exclude(id__in=reviews.values("word"))
            return queryset.order_by("-id")
        if self.review == 1:
            queryset = queryset.filter(id__in=reviews.values("word"))

        if self.level >= 0:
            reviews = reviews.filter(level=self.level)
            queryset = queryset.filter(id__in=reviews.values("word"))

        if self.hard:
            reviews = reviews.filter(hard__gt=0)
            queryset = queryset.filter(id__in=reviews.values("word"))

        logger.debug(queryset.query)
        return queryset.order_by("-id")

    def get(self, request, *args, **kwargs):
        form = self.form_class(self.request.GET or None)
        if not form.is_valid():
            return super(WordlistView, self).get(request, *args, **kwargs)
        self.filter(form)
        return super(WordlistView, self).get(request, *args, **kwargs)

    def filter(self, form):
        self.review = form.cleaned_data.get("review", 0) or 0
        self.level = form.cleaned_data.get("level", -1) or -1
        self.hard = form.cleaned_data.get("hard", 0) or 0


class SearchView(ListView):

    context_object_name = "items"

    def render_to_response(self, context, **response_kwargs):
        data = dandan.value.AttrDict()
        data.results = []
        data.success = True
        for word in context["items"]:
            item = dandan.value.AttrDict()
            item.title = word.title
            item.para = str(word.paraphrase.all().first())
            # item.name = '[{title}] [{paraphrase}]'.format(
            #     title=word.title,
            #     paraphrase=item.para,
            # )
            item.id = word.id
            item.url = reverse_lazy("found", kwargs={"title": word.title})
            data.results.append(item)

        return JsonResponse(data=data, safe=False)

    def get_queryset(self):
        query = self.kwargs.get("query", None)
        if not query:
            query = ""

        query = query.strip()
        query_title = Q(title__contains=query)
        query_para = Q(paraphrase__content__contains=query)
        return models.Word.objects\
            .filter(query_title | query_para)\
            .distinct()\
            .extra(select={'length': 'Length(title)'}).order_by('length')[:7]


class PhoneticView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        title = self.kwargs.get("title", None)
        content = self.kwargs.get("type", None)
        word = models.Word.objects.filter(title=title).first()
        if not word:
            url = youdao.get_phonetic_url(title, content)
        else:
            if content not in {youdao.CONTENT_UK, youdao.CONTENT_US}:
                return HttpResponseNotFound()
            phontype = models.PhoneticType.objects.get_or_create(content=content)[0]
            phon = models.Phonetic.objects.get_or_create(type=phontype, word=word)[0]
            functions.download_phonetic(phon)
            url = static("/phonetic/{}/{}_.mp3".format(content, title))
        return HttpResponseRedirect(redirect_to=url)


class TestView(TemplateView):

    template_name = "test/test.html"
