"""studio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    url(r'^$', login_required(views.basic.WordlistView.as_view()), name="index"),
    url(r'^register/$', views.account.RegisterSuperUserView.as_view(), name="register"),
    url(r'^login/$', views.account.LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),


    url(r'^wordlist/$', login_required(views.basic.WordlistView.as_view()), name="wordlist"),
    url(r'^test/$', login_required(views.basic.TestView.as_view()), name="test"),


    url(r'^settings/$', staff_member_required(views.settings.SettingsView.as_view()), name="settings"),
    url(r'^settings/phonetic/(?P<action>download|stop|status)$', staff_member_required(views.settings.SettingsPhoneticView.as_view()), name="settings_phonetic"),
    url(r'^settings/backup/(?P<action>backup|restore)$', staff_member_required(views.settings.SettingsBackupView.as_view()), name="settings_backup"),
    url(r'^settings/update/(?P<action>check|update|status)$', staff_member_required(views.settings.SettingsUpdateView.as_view()), name="settings_update"),

    # url(r'^search/(?P<query>.+)/$', views.basic.SearchView.as_view(), name="search"),
    url(r'^search(?:/(?P<query>.+|))?/$', views.basic.SearchView.as_view(), name="search"),
    url(r'^phonetic/(?P<type>UK|US)/(?P<title>[-\w ]+)/$', login_required(views.basic.PhoneticView.as_view()), name="phonetic"),

    url(r'^study/$', RedirectView.as_view(url=reverse_lazy("review", kwargs={'action': 'start'})), name="study"),
    url(r'^review/(?P<action>start|next|check)/$', login_required(views.study.ReviewView.as_view()), name="review"),
    url(r'^hard/(?P<action>start|next|check)/$', login_required(views.study.HardView.as_view()), name="hard"),
    url(r'^practice/(?P<action>start|next|check)/$', login_required(views.study.PracticeView.as_view()), name="practice"),

    url(r'^edit(?:/(?P<action>para|title|equals|similars|related|refresh|reset))?/(?P<id>[0-9]+)/$', staff_member_required(views.edit.EditView.as_view(), login_url="login"), name="edit"),
    url(r'^edit/save/(?P<id>[0-9]+)/$', staff_member_required(views.edit.EditView.as_view(), login_url="login"), name="save"),
    url(r'^add/(?P<action>review|word)/(?P<title>[-\w ]+)/$', login_required(views.edit.AddView.as_view()), name="add"),
    url(r'^add/paraphrase/(?P<word_id>[0-9]+)/$', staff_member_required(views.edit.AddParaphraseView.as_view()), name="add_paraphrase"),
    url(r'^remove/(?P<action>review|word|para)/(?P<id>[0-9]+)/$', login_required(views.edit.RemoveView.as_view()), name="remove"),

    url(r'^found(?:/(?P<title>[-\w ]+|))?/$', login_required(views.found.FoundView.as_view()), name="found"),
    url(r'^resources(?:/(?P<query>[0-9/]+|))?/$', login_required(views.found.ResourcesView.as_view()), name="resources"),
    url(r'^wordcard/(?P<title>[-\w ]+)/$', login_required(views.found.WordCardView.as_view()), name="wordinfo"),

    url(r'^statistics/$', RedirectView.as_view(url=reverse_lazy("coming")), name="statistics"),
    url(r'^statistics/coming/$', login_required(views.statistics.ComingView.as_view()), name="coming"),
    url(r'^statistics/date(?:/(?P<date>[-0-9]+|))?/$', login_required(views.statistics.DateView.as_view()), name="date"),
    url(r'^statistics/count/$', login_required(views.statistics.CountView.as_view()), name="count"),
    url(r'^statistics/level(?:/(?P<level>[0-9]+|))?/$$', login_required(views.statistics.LevelView.as_view()), name="level"),
    url(r'^statistics/error(?:/(?P<error>[0-9]+|))?/$$', login_required(views.statistics.ErrorView.as_view()), name="error"),
]
