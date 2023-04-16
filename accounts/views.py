from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.db.models import Case, When
from tree.models import *


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        status_order = {s: i for i, (s, _) in enumerate(UserCourses.STATUS_CHOICES)}
        print(self.request.user)
        ctx["user"] = CustomUser.objects.filter(username=self.request.user)[0]
        ctx["courses"] = UserCourses.objects.filter(user=self.request.user).order_by(Case(When(status=UserCourses.STARTED, then=status_order[UserCourses.STARTED]),
                                                    When(status=UserCourses.COMPLETED, then=status_order[UserCourses.COMPLETED]),
                                                    When(status=UserCourses.REJECTED, then=status_order[UserCourses.REJECTED]),
                                                    default=status_order[UserCourses.REJECTED],
                                                    output_field=models.IntegerField()))
        ctx["leafs"] = UserLeaf.objects.filter(user=self.request.user).order_by(Case(When(status=UserLeaf.STARTED, then=status_order[UserLeaf.STARTED]),
                                                    When(status=UserLeaf.COMPLETED, then=status_order[UserLeaf.COMPLETED]),
                                                    When(status=UserLeaf.REJECTED, then=status_order[UserLeaf.REJECTED]),
                                                    default=status_order[UserLeaf.REJECTED],
                                                    output_field=models.IntegerField()))
        return ctx
