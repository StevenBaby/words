# coding=utf-8
from __future__ import print_function, unicode_literals
import json

import logging
import dandan
import random

from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _
from django.http.response import JsonResponse
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from django.utils import timezone

from words import functions
from words import study
from words import models

from viewer import forms


logger = logging.getLogger("words")


class StudyView(FormView):

    template_name = "study/study.html"
    form_class = forms.CheckForm
    study_type = "study"
    study_description = _("study")

    STUDY_TYPE_REVIEW = "review"
    STUDY_TYPE_HARD = "hard"
    STUDY_TYPE_PRACTICE = "practice"

    methods = [
        "dictation",
        "paraphrase",
    ]

    def get_next(self, context):
        return

    def has_next(self):
        return False

    def right(self, word):
        pass

    def error(self, word):
        pass

    def check_valid(self, word):
        return True

    def check(self, word, titles):
        data = study.check(word, titles)
        data.success = True
        if data.error:
            self.error(word)
        else:
            self.right(word)
        return data

    # def get_context_data(self, **kwargs):
    #     context = super(StudyView, self).get_context_data(**kwargs)
    #     return context

    def form_valid(self, form):
        if self.kwargs.get("action", None) != "check":
            return JsonResponse({'success': False, "error": 4, "description": _("Wrong approach"), })

        id = form.cleaned_data.get("id", 0)
        input_line = form.cleaned_data.get("input_line", "")
        word = models.Word.objects.filter(id=id).first()
        if not word:
            return JsonResponse({'success': False, "error": 1, "description": _("Word not found."), })
        if not self.check_valid(word):
            return JsonResponse({'success': False, "error": 2, "description": _("Word not vaild to this study method")})
        titles = [title.strip() for title in functions.split(input_line) if len(title.strip()) > 1]
        if not titles:
            return JsonResponse({'success': False, "error": 3, "description": _("Title is Empty")})
        return JsonResponse(self.check(word, titles))

    def deal_redirect(self):
        if self.study_type == self.STUDY_TYPE_PRACTICE:
            words = self.request.session.get('practice', None)
            if 'practice' in self.request.session and not words:
                del self.request.session['practice']
                return HttpResponseRedirect(reverse_lazy("practice", kwargs={"action": "start"}))
            return None

        has_hard = study.has_hard(user=self.request.user)

        if self.study_type == "hard" and has_hard:
            return None
        if self.study_type != "hard" and has_hard:
            return HttpResponseRedirect(reverse_lazy("hard", kwargs={"action": "next"}))

        has_review = study.has_review(user=self.request.user)
        if self.study_type != "review" and has_review:
            return HttpResponseRedirect(reverse_lazy("review", kwargs={"action": "next"}))
        return None

    def render_to_response(self, context, **response_kwargs):
        action = self.kwargs.get('action', None)
        if action == "start" and not self.has_next():
            action = "next"
        elif action == "next":
            redirect = self.deal_redirect()
            if redirect:
                return redirect
        if action == "next":
            self.get_next(context)

        context["action"] = action
        context["study"] = True
        context["study_type"] = self.study_type
        context["study_description"] = self.study_description

        if 'word' in context and context["word"]:
            profile = self.request.user.profile
            if profile.settings_study_mode == 1:
                context["method"] = "dictation"
            elif profile.settings_study_mode == 2:
                context["method"] = "paraphrase"
            else:
                context["method"] = random.choice(self.methods)

        response = super(FormView, self).render_to_response(context, **response_kwargs)
        return response


class ReviewView(StudyView):
    study_type = StudyView.STUDY_TYPE_REVIEW
    study_description = _("review")

    def has_next(self):
        return study.has_review(user=self.request.user)

    def get_next(self, context):
        review = study.get_random_review(user=self.request.user)
        if review:
            context["word"] = review.word
            context["review"] = review
            return

        next_review = study.get_near_review(self.request.user)
        if next_review:
            context["next_review_time"] = next_review.review_time - timezone.now()

    def right(self, word):
        study.review_right(word, self.request.user)

    def error(self, word):
        study.review_error(word, self.request.user)

    def check_valid(self, word):
        return study.can_review(word, self.request.user)


class HardView(StudyView):

    study_type = StudyView.STUDY_TYPE_HARD
    study_description = _("Conquer hard")

    def has_next(self):
        return study.has_hard(user=self.request.user)

    def get_next(self, context):
        review = study.get_random_hard(user=self.request.user)
        if review:
            context["word"] = review.word
            context["review"] = review
            return

        next_hard = study.get_near_hard(self.request.user)
        if next_hard:
            # logger.debug("now {} hard_time {} review_time {} ".format(timezone.now(), next_hard.hard_time, next_hard.review_time))
            context["next_review_time"] = next_hard.hard_time - timezone.now()

    def right(self, word):
        study.hard_right(word, self.request.user)

    def error(self, word):
        study.hard_error(word, self.request.user)

    def check_valid(self, word):
        return study.can_hard(word, self.request.user)


class PracticeView(StudyView):

    study_type = StudyView.STUDY_TYPE_PRACTICE
    study_description = _("practice")

    def prepare_words(self, form):
        input_line = form.cleaned_data.get("input_line", "[]")
        try:
            words = json.loads(input_line)
            words = [int(var) for var in words]
        except Exception:
            return

        words = models.Word.objects.filter(id__in=words).values('id')
        words = [item["id"] for item in words]
        self.request.session['practice'] = words

    def form_valid(self, form):
        if self.kwargs.get("action", None) != "start":
            return super().form_valid(form)
        self.prepare_words(form)
        return HttpResponseRedirect(reverse_lazy("practice", kwargs={"action": "start"}))

    def has_next(self):
        if self.request.session.get('practice', None):
            return True
        return study.has_practice(user=self.request.user)

    def get_next(self, context):
        words = self.request.session.get('practice', [])
        word = None
        if words:
            word = models.Word.objects.filter(id=random.choice(words)).first()
        if not word:
            word = study.get_random_practice(user=self.request.user)
        context["word"] = word

    def check_valid(self, word):
        return models.Word.objects.filter(title=word).exists()

    def check(self, word, titles):
        data = study.check(word, titles, save=False)
        data.success = True
        if data.error:
            self.error(word)
        else:
            self.right(word)
        return data

    def right(self, word):
        words = self.request.session.get('practice', [])
        if not words:
            return

        if word.id in words:
            words.remove(word.id)
        self.request.session['practice'] = words
