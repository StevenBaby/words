from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect

from viewer import forms


class RegisterSuperUserView(FormView):

    template_name = "registration/register.html"
    form_class = forms.RegisterSuperUserForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        user = authenticate(request=self.request, username=user.username, password=form.cleaned_data['password1'])
        if user and user.is_active:
            login(request=self.request, user=user)
        return super(RegisterSuperUserView, self).form_valid(form)


class LoginView(DjangoLoginView):

    def render_to_response(self, context, **response_kwargs):
        if not User.objects.filter(id=1).exists():
            return HttpResponseRedirect(reverse_lazy("register"))
        return super(LoginView, self).render_to_response(context, **response_kwargs)
