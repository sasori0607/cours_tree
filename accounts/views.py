from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.db.models import Case, When
from tree.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


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
        user = CustomUser.objects.filter(username=self.request.user)[0]
        ctx["user"] = user
        if user.gradation == "student":
            sort_by = self.request.GET.get('sort_by', 'name')  # по умолчанию сортируем по названию
            sort_order = self.request.GET.get('sort_order', 'asc')  # по умолчанию сортируем по возрастанию

            courses = UserCourses.objects.filter(user=self.request.user).order_by(
                f'course__{sort_by}'
            )

            ctx["courses"] = courses
            ctx["leafs"] = UserLeaf.objects.filter(user=self.request.user).order_by('status')
        else:
            courses = Course.objects.filter(author=user)
            ctx["courses"] = courses

        return ctx


class TeacherCourseView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/course_changes.html"

    def get_context_data(self, **kwargs):
        course_id = self.kwargs.get('id')
        ctx = super().get_context_data(**kwargs)
        user = CustomUser.objects.filter(username=self.request.user)[0]
        ctx["user"] = user

        course = Course.objects.filter(id=course_id)[0]
        print('course', course)
        users_course = UserCourses.objects.filter(course=course, status="ST")
        print('users_course', users_course)
        leafs = course.leafs.all().order_by('id')
        ctx['leafs'] = leafs
        print(leafs)
        magic_dict = {}
        for user_course in users_course:
            user_leafs = UserLeaf.objects.filter(user=user_course.user, leafs__in=leafs).order_by('leafs__id')
            magic_dict[user_course.user] = user_leafs
            # Хранить инфу по листу будем в ячейке с айди, айди отправлять и перезаписывать.

        ctx["magic_dict"] = magic_dict
        return ctx


@csrf_exempt
def change_leafs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        object_id = data.get('value')
        status = data.get('status')
        if status == 'done':
            user_leaf = UserLeaf.objects.filter(id=object_id)[0]
            user_leaf.status = 3
            user_leaf.save()
        elif status == 'not_done':
            user_leaf = UserLeaf.objects.filter(id=object_id)[0]
            user_leaf.status = 2
            user_leaf.save()
        return JsonResponse({'status': 'ok'})
    print('-')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def change_status_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        button_name = data.get('button_name')
        user_id = data.get('button_value')
        course_id = data.get('url').split('/')[-2]
        print(button_name, user_id, course_id)
        if button_name == 'complitle':
            UserCourses.objects.update_or_create(
                user_id=user_id,
                course_id=course_id,
                defaults={
                    'status': 'CP',
                }
            )
            leafs = Course.objects.filter(id=course_id)[0].leafs.all()
            for i in leafs:
                UserLeaf.objects.update_or_create(
                    user_id=user_id,
                    leafs_id=i.id,
                    defaults={
                        'status': 4,
                    }
                )
        if button_name == 'refusal':
            UserCourses.objects.update_or_create(
                user_id=user_id,
                course_id=course_id,
                defaults={
                    'status': 'RJ',
                }
            )

        return JsonResponse({'status': 'ok'})
    print('-')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
