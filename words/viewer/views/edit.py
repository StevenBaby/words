# coding=utf-8
from __future__ import print_function, unicode_literals

import re
import logging

# from django.utils import timezone
from django.urls import reverse_lazy
# from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.views.generic import TemplateView
from django.views.generic import FormView
# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView

from django.http.response import JsonResponse
from django.http.response import HttpResponseNotFound
from django.http.response import HttpResponseBadRequest
from django.http.response import HttpResponseForbidden

# from django.http.response import HttpResponseRedirect


# from utils import youdao

from words import models
from words import functions
from viewer import forms
from utils import youdao

# import dandan

logger = logging.getLogger("words")


class RemoveView(FormView):

    form_class = forms.EmptyForm

    def remove_word(self):
        if not self.request.user.is_staff:
            return HttpResponseForbidden()
        id = int(self.kwargs["id"])
        word = models.Word.objects.filter(id=id).filter()
        if not word:
            return JsonResponse({
                "success": False,
                "error": 1,
                "description": _("Word not exists."),
            })
        word.delete()
        return JsonResponse({
            "success": True,
            "action": 'word',
            "description": _("Delete word success."),
        })

    def remove_review(self):
        id = int(self.kwargs["id"])
        review = functions.get_all_review(user=self.request.user).filter(id=id).first()
        if not review:
            return JsonResponse({
                "success": False,
                "error": 1,
                "description": _("Review not exists."),
            })
        review.delete()
        return JsonResponse({
            "success": True,
            "action": 'word',
            "description": _("Remove review success."),
        })

    def remove_para(self):
        if not self.request.user.is_staff:
            return HttpResponseForbidden()
        id = int(self.kwargs["id"])
        para = models.Paraphrase.objects.filter(id=id).first()
        if not para:
            return JsonResponse({
                "success": False,
                "error": 1,
                "description": _("Paraphrase not exists."),
            })
        para.delete()
        return JsonResponse({
            "success": True,
            "action": 'para',
            "description": _("Remove Paraphrase success."),
        })

    def form_valid(self, form):
        action = self.kwargs["action"]
        if action == "word":
            return self.remove_word()
        if action == "review":
            return self.remove_review()
        if action == "para":
            return self.remove_para()
        return HttpResponseBadRequest()


class AddView(FormView):

    form_class = forms.EmptyForm

    def save_word(self):
        title = self.kwargs["title"]
        if settings.IGNORED_PATTERN.match(title):
            return JsonResponse({
                "success": False,
                "error": 1,
                "description": _("Cause application design, this word can not add in directory."),
            })

        word = functions.consult(title)
        if not word:
            return JsonResponse({
                "success": False,
                "error": 2,
                "description": _("Word not found."),
            })
        if word.id:
            return word
        word = functions.save(word)
        return word

    def add_word(self):
        if not self.request.user.is_staff:
            return HttpResponseForbidden()
        word = self.save_word()
        if isinstance(word, JsonResponse):
            return word

        data = {
            "success": True,
            "action": 'word',
            "description": _("Add to dictionary success."),
        }
        if self.request.user.is_staff:
            data['edit_url'] = reverse_lazy("edit", kwargs={"id": word.id})
            logger.debug(data['edit_url'])
        return JsonResponse(data)

    def add_review(self):
        word = self.save_word()
        if isinstance(word, JsonResponse):
            return word
        review = functions.get_all_review(user=self.request.user).filter(word=word).first()
        if not review:
            review = functions.set_review(word=word, user=self.request.user)

        data = {
            "success": True,
            "action": 'review',
            "description": _("Add to review success."),
        }
        if self.request.user.is_staff:
            data['edit_url'] = reverse_lazy("edit", kwargs={"id": word.id})
            logger.debug(data['edit_url'])
        return JsonResponse(data)

    def form_valid(self, form):
        action = self.kwargs["action"]
        if action == "word":
            return self.add_word()
        if action == "review":
            return self.add_review()
        return HttpResponseBadRequest()


class AddParaphraseView(FormView):

    form_class = forms.EditForm

    def form_valid(self, form):
        word = models.Word.objects.filter(id=self.kwargs["word_id"]).first()
        if not word:
            return JsonResponse({
                "success": False,
                "description": _("Word does not exists!!!"),
            })
        para_type = form.cleaned_data.get("para_type").lower()
        if para_type not in youdao.PARA_TYPES:
            return JsonResponse({
                "success": False,
                "description": _("Paraphrase type invalid."),
            })
        para_content = form.cleaned_data.get("para_content")
        if not para_content:
            return JsonResponse({
                "success": False,
                "description": _("Paraphrase content must not empty."),
            })

        para_type = models.ParaType.objects.get_or_create(content=para_type)[0]
        para, created = models.Paraphrase.objects.get_or_create(type=para_type, content=para_content, word=word)
        if not created:
            return JsonResponse({
                "success": False,
                "description": _("Paraphrase already exists."),
            })
        return JsonResponse({
            "success": True,
            "action": 'add_paraphrase',
            "description": _("Add paraphrase success."),
        })


class EditView(FormView):

    template_name = "edit/edit.html"
    form_class = forms.EditForm

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        if not self.get_action():
            id = int(self.kwargs["id"])
            word = models.Word.objects.filter(id=id).first()
            context["word"] = word
            context["para_types"] = sorted(list(youdao.PARA_TYPES))
            context["detail"] = True
        return context

    def get_action(self):
        return self.kwargs["action"]

    def edit_title(self, form):
        word = models.Word.objects.filter(id=self.kwargs["id"]).first()
        if not word:
            return JsonResponse({
                "success": False,
                "description": _("Word does not exists!!!"),
            })
        title = form.cleaned_data.get('title', '').strip()
        if not title:
            return JsonResponse({
                "success": False,
                "description": _("Word title must not empty!!!"),
            })
        if settings.IGNORED_PATTERN.match(title):
            return JsonResponse({
                "success": False,
                "error": 1,
                "description": _("Cause application design, this word can not add in directory."),
            })
        if title == word.title:
            return JsonResponse({
                "success": True,
                "action": 'title',
                "description": _("Save word title success."),
            })

        if models.Word.objects.filter(title=title).exclude(id=word.id).exists():
            return JsonResponse({
                "success": False,
                "description": _("Word title already exists!!!"),
            })

        word.title = title
        word.save()

        return JsonResponse({
            "success": True,
            "action": 'title',
            "description": _("Save word title success."),
        })

    def edit_para(self, form):
        id = int(self.kwargs["id"])
        logger.debug("get paraphrase id %s", id)
        para = models.Paraphrase.objects.filter(id=id).first()
        if not para:
            return JsonResponse({
                "success": False,
                "description": _("Paraphrase does not exists."),
            })
        para_type = form.cleaned_data.get("para_type").lower()
        if para_type not in youdao.PARA_TYPES:
            return JsonResponse({
                "success": False,
                "description": _("Paraphrase type invalid."),
            })
        para_content = form.cleaned_data.get("para_content")
        if not para_content:
            return JsonResponse({
                "success": False,
                "description": _("Paraphrase content must not empty."),
            })

        save = False
        if para_type != para.type.content:
            para_type = models.ParaType.objects.get_or_create(content=para_type)[0]
            para.type = para_type
            save = True
        if para_content != para.content:
            para.content = para_content
            save = True

        if save:
            para.save()

        return JsonResponse({
            "success": True,
            "action": 'para',
            "description": _("Save paraphrase success."),
        })

    def edit_refresh(self, form):
        word = models.Word.objects.filter(id=self.kwargs["id"]).first()
        if not word:
            return JsonResponse({
                "success": False,
                "description": _("Word does not exists!!!"),
            })
        if not functions.refresh(word):
            return JsonResponse({
                "success": False,
                "description": _("Refresh word failure!!!"),
            })
        return JsonResponse({
            "success": True,
            "action": 'refresh',
            "description": _("Refresh word success."),
        })

    def edit_equals(self, form):
        word = models.Word.objects.filter(id=self.kwargs["id"]).first()
        if not word:
            return JsonResponse({
                "success": False,
                "description": _("Word does not exists!!!"),
            })
        word_ids = self.request.POST.getlist("word_ids")
        logger.debug("post equals word_ids %s", word_ids)
        word_ids = [int(var) for var in word_ids if re.match(r"\d+", var)]

        equals = models.Word.objects.filter(id__in=word_ids).exclude(id=word.id)

        word.similars.remove(*equals)

        logger.debug(equals)
        word.equals.set(equals)
        word.save()
        return JsonResponse({
            "success": True,
            "action": 'equals',
            "description": _("Save equal words success."),
        })

    def edit_similars(self, form):
        word = models.Word.objects.filter(id=self.kwargs["id"]).first()
        if not word:
            return JsonResponse({
                "success": False,
                "description": _("Word does not exists!!!"),
            })
        word_ids = self.request.POST.getlist("word_ids")
        logger.debug("post similars word_ids %s", word_ids)
        word_ids = [int(var) for var in word_ids if re.match(r"\d+", var)]
        similars = models.Word.objects\
            .filter(id__in=word_ids)\
            .exclude(id=word.id)\
            .exclude(id__in=word.equals.all())

        logger.debug(similars)
        word.similars.set(similars)
        word.save()
        return JsonResponse({
            "success": True,
            "action": 'similars',
            "description": _("Save similar words success."),
        })

    def edit_related(self, form):
        word = models.Word.objects.filter(id=self.kwargs["id"]).first()
        if not word:
            return JsonResponse({
                "success": False,
                "description": _("Word does not exists!!!"),
            })
        word_ids = self.request.POST.getlist("word_ids")
        logger.debug("post related word_ids %s", word_ids)
        word_ids = [int(var) for var in word_ids if re.match(r"\d+", var)]
        relateds = models.Word.objects\
            .filter(id__in=word_ids)\
            .exclude(id=word.id)

        logger.debug(relateds)
        word.relateds.set(relateds)
        word.save()
        return JsonResponse({
            "success": True,
            "action": 'related',
            "description": _("Save related words success."),
        })

    def edit_reset(self, form):
        review = functions.get_all_review(self.request.user).filter(id=self.kwargs["id"]).first()
        if not review:
            return JsonResponse({
                "success": False,
                "action": 'reset',
                "description": _("Review does not exists"),
            })

        functions.reset_review(review)

        return JsonResponse({
            "success": True,
            "action": 'reset',
            "description": _("Reset review success."),
        })

    def form_valid(self, form):
        if self.get_action() == "title":
            return self.edit_title(form)
        if self.get_action() == 'para':
            return self.edit_para(form)
        if self.get_action() == 'equals':
            return self.edit_equals(form)
        if self.get_action() == 'similars':
            return self.edit_similars(form)
        if self.get_action() == "related":
            return self.edit_related(form)
        if self.get_action() == 'refresh':
            return self.edit_refresh(form)
        if self.get_action() == 'reset':
            return self.edit_reset(form)
        return HttpResponseBadRequest()

    def render_to_response(self, context, **response_kwargs):
        if not context['word']:
            return HttpResponseNotFound()
        return super(EditView, self).render_to_response(context, **response_kwargs)


class SaveEditView(TemplateView):

    template_name = "edit/edit.html"

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        id = int(self.kwargs["id"])
        word = models.Word.objects.filter(id=id).first()
        context["word"] = word
        context["detail"] = True
        return context

    def render_to_response(self, context, **response_kwargs):
        if not context['word']:
            return HttpResponseNotFound()
        return super(EditView, self).render_to_response(context, **response_kwargs)
