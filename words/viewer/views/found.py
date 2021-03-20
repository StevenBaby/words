from django.views.generic import TemplateView
# from django.views.generic import FormView
from django.views.generic.list import ListView
from django.http.response import JsonResponse
# from django.http.response import HttpResponseNotFound
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

import dandan
import logging

from words import models
from words import functions

# from .. import forms


logger = logging.getLogger("words")


class FoundView(TemplateView):

    template_name = "found/found.html"

    def get_context_data(self, **kwargs):
        context = super(FoundView, self).get_context_data(**kwargs)
        title = self.kwargs.get('title', '')
        if not title:
            word = functions.get_random(models.Word.objects.all())
        else:
            word = functions.consult(title=title)
        context["word"] = word
        context["detail"] = True
        return context


class ResourcesView(ListView):

    template_name = "found/resources.html"
    context_object_name = "items"
    paginate_by = 20

    resource_names = []

    un_dictionary_list = []
    un_review_list = []
    resource_list = []
    resource_type = None

    def get_list(self):
        import resources

        url = reverse_lazy("resources")
        self.resource_names = [{"name": _("Resources"), "url": url}]
        self.resource_list = resources.get_resources()

        item = dandan.value.AttrDict()
        query = self.kwargs.get("query")
        if not query:
            return

        indices = query.split("/")

        for index in indices:
            try:
                index = int(index)
            except ValueError:
                return

            if len(self.resource_list) <= index:
                return

            item = self.resource_list[index]

            url += "{}/".format(index)
            name = dandan.value.AttrDict()
            name.name = item.name
            name.url = url

            self.resource_names.append(name)
            self.resource_type = item.type
            self.resource_list = item.list

        if self.resource_list and isinstance(self.resource_list[0], str):
            self.resource_dict = {title: index for index, title in enumerate(self.resource_list)}

        if self.get_status("dictionary") != 0 and self.resource_type == "list":
            words_list = models.Word.objects.values_list('title')
            words_set = set([var[0] for var in words_list])
            self.un_dictionary_list = list(set(self.resource_list) - words_set)
            self.un_dictionary_list = sorted(self.un_dictionary_list, key=lambda e: self.resource_dict[e])

            # logger.debug("un dictionary list length %s"a, len(self.un_dictionary_list))

        if self.get_status("review") != 0 and self.resource_type == "list":
            words_list = functions.get_all_review(user=self.request.user).values_list('word__title')
            words_set = set([var[0] for var in words_list])
            self.un_review_list = list(set(self.resource_list) - words_set)
            self.un_review_list = sorted(self.un_review_list, key=lambda e: self.resource_dict[e])
            # logger.debug("un dictionary list length %s"a, len(self.un_dictionary_list))

    def get_status(self, key):
        status = str(self.request.GET.get(key, "0"))
        if status == "0":
            return 0
        else:
            return status

    def get_context_data(self, **kwargs):
        context = super(ResourcesView, self).get_context_data(**kwargs)
        context['resource_names'] = self.resource_names
        context["dictionary"] = self.get_status("dictionary")
        context["review"] = self.get_status("review")
        return context

    def get_queryset(self):
        self.get_list()
        if self.get_status("dictionary") != 0 and self.resource_type == "list":
            return self.un_dictionary_list
        if self.get_status("review") != 0 and self.resource_type == "list":
            return self.un_review_list
        else:
            return self.resource_list


class WordCardView(TemplateView):

    template_name = "found/resources_word_card.html"

    def get_context_data(self, **kwargs):
        context = super(WordCardView, self).get_context_data(**kwargs)
        title = self.kwargs["title"]
        context['word'] = functions.consult(title=title)
        return context

    # def render_to_response(self, context, **response_kwargs):
    #     title = self.kwargs["title"]
    #     # if functions.exists(title=title):
    #     #     return JsonResponse({'success': False, "error": 1, "description": _("Word already exists"), })

    #     word = functions.consult(title=title)
    #     context["word"] = word
    #     return super(WordCardView, self).render_to_response(context, **response_kwargs)
