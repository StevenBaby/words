# coding=utf-8
from __future__ import print_function, unicode_literals

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


# logger = logging.getLogger("words")


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
        if self.kwargs["action"] != "check":
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
        action = self.kwargs['action']
        if action == "start" and not self.has_next():
            action = "next"
        elif action == "next" and self.study_type != StudyView.STUDY_TYPE_PRACTICE:
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

        return super(FormView, self).render_to_response(context, **response_kwargs)


class ReviewView(StudyView):
    study_type = StudyView.STUDY_TYPE_REVIEW
    study_description = _("review")

    def has_next(self):
        return study.has_review(user=self.request.user)

    def get_next(self, context):
        review = study.get_random_review(user=self.request.user)
        word = None
        if review:
            word = review.word
        context["word"] = word
        context["review"] = review
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
        word = None
        if review:
            word = review.word
        context["word"] = word
        context["review"] = review
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

    def has_next(self):
        return study.has_practice(user=self.request.user)

    def get_next(self, context):
        word = study.get_random_practice(user=self.request.user)
        context["word"] = word

    def check_valid(self, word):
        return study.can_practice(word, self.request.user)

    def check(self, word, titles):
        data = study.check(word, titles, save=False)
        data.success = True
        if data.error:
            self.error(word)
        else:
            self.right(word)
        return data
