import json
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.urls import reverse
from .forms import UserLeafForm
from .models import Leaf, LeafKeypoint, Course, UserLeaf, UserCourses
from urllib.parse import urlparse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def process_node(data, node):
    children = [process_node(data, child) for child in data if child.parent_id == node.id]
    return {
        "name": node.name,
        "id": node.id,
        "children": children,
        "size": 1000  # здесь можно задать любое значение для атрибута size
    }


def format_tree_data(data):
    # находим корневой элемент, то есть элемент без родителя
    root = next((item for item in data if item.parent_id is None), None)
    print(root)
    # обрабатываем корневой элемент и все его дочерние элементы
    return process_node(data, root)


class TreeBranchView(ListView):
    template_name = 'tree/tree.html'
    context_object_name = 'object_list'
    model = Leaf

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        leafs = self.model.objects.all()
        url = self.request.build_absolute_uri()
        clean_url = urlparse(url)._replace(query=None).geturl()
        print(len(clean_url.split('/')), clean_url)
        if len(clean_url.split('/')) > 4:
            tree_data = process_node(leafs, leafs.filter(id=clean_url.split('/')[-2])[0])
            root_leaf_info = leafs.filter(id=clean_url.split('/')[-2])[0]
        else:
            tree_data = format_tree_data(leafs)
            root_leaf_info = leafs.filter(parent=None)[0]
        ctx['data_for_d3'] = tree_data
        ctx["user_leafs_start"] = []
        ctx["user_leafs_passed"] = []
        ctx["leaf"] = root_leaf_info

        if self.request.user.is_authenticated:
            user_leafs = UserLeaf.objects.all()
            all_leafs = Leaf.objects.all()
            ctx["NOT_INTERESTED"] = list(
                user_leafs.filter(user=self.request.user, status=5).values_list('leafs_id', flat=True))
            ctx["INTERESTED"] = list(
                user_leafs.filter(user=self.request.user, status=1).values_list('leafs_id', flat=True))
            ctx["LEARNING"] = list(
                user_leafs.filter(user=self.request.user, status=2).values_list('leafs_id', flat=True))
            ctx["LEARNED"] = list(
                user_leafs.filter(user=self.request.user, status=3).values_list('leafs_id', flat=True))
            ctx["VALIDATED"] = list(
                user_leafs.filter(user=self.request.user, status=4).values_list('leafs_id', flat=True))
            ctx["THEORY"] = list(
                all_leafs.filter(type='THEORY').values_list('id', flat=True))
            ctx["PRACTICE"] = list(
                all_leafs.filter(type='PRACTICE').values_list('id', flat=True))
            ctx["PROJECT"] = list(
                all_leafs.filter(type='PROJECT').values_list('id', flat=True))

        leaf = leafs.filter(id=root_leaf_info.id)[0]
        key_points = LeafKeypoint.objects.all().filter(leaf=leaf)
        ctx["key_points"] = key_points
        courses = Course.objects.all().filter(leafs=leaf)
        ctx["courses"] = courses
        # if key_point
        if leafs.filter(parent__id=root_leaf_info.id):
            children = leafs.filter(parent__id=root_leaf_info.id)
            ctx['children'] = children
        if leaf.parent and leafs.filter(id=root_leaf_info.id):
            parent = leafs.filter(id=leaf.parent.id)
            ctx['parent'] = parent
        ctx['leaf'] = leaf
        user_leaf = UserLeaf.objects.get_or_create(
            user_id=self.request.user.id,
            leafs_id=leaf.id,
        )
        ctx['user_leaf'] = user_leaf[0]
        initial = {'status': user_leaf[0].status}
        ctx['comment_form'] = UserLeafForm(initial=initial)
        return ctx


class LeafView(ListView):
    template_name = 'tree/leaf.html'
    context_object_name = 'object_list'
    model = Leaf

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        url = self.request.build_absolute_uri()
        clean_url = urlparse(url)._replace(query=None).geturl()
        leafs = self.model.objects.all()
        leaf = leafs.filter(id=clean_url.split('/')[-2])[0]
        key_points = LeafKeypoint.objects.all().filter(leaf=leaf)
        ctx["key_points"] = key_points
        courses = Course.objects.all().filter(leafs=leaf)
        ctx["courses"] = courses
        ctx['user'] = self.request.user
        # if key_point
        if leafs.filter(parent__id=clean_url.split('/')[-2]):
            children = leafs.filter(parent__id=clean_url.split('/')[-2])
            ctx['children'] = children
        if leaf.parent and leafs.filter(id=leaf.parent.id):
            parent = leafs.filter(id=leaf.parent.id)
            ctx['parent'] = parent
        user_leaf = UserLeaf.objects.get_or_create(
            user_id=self.request.user.id,
            leafs_id=leaf.id,
        )
        ctx['user_leaf'] = user_leaf[0]
        initial = {'status': user_leaf[0].status}

        ctx['comment_form'] = UserLeafForm(initial=initial)
        ctx['leaf'] = leaf
        return ctx


class CourseView(ListView):
    template_name = 'tree/course.html'
    context_object_name = 'object_list'
    model = Course

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        url = self.request.build_absolute_uri()
        clean_url = urlparse(url)._replace(query=None).geturl()
        course = self.model.objects.filter(id=clean_url.split('/')[-2])[0]
        ctx['course'] = course
        ctx['user'] = self.request.user
        user_course = UserCourses.objects.filter(user__id=self.request.user.id, course__id=course.id)
        if user_course:
            ctx['user_course'] = user_course[0]

        # print(course)
        # ctx['1'] = course

        return ctx


class CoursesView(ListView):
    template_name = 'tree/courses.html'
    context_object_name = 'object_list'
    model = Course

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        courses = self.model.objects.all()
        ctx['courses'] = courses

        return ctx


@csrf_exempt
def save_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        course_id = data.get('course_id')
        UserCourses.objects.get_or_create(
            user_id=user_id,
            course_id=course_id,
        )
        leafs = Course.objects.filter(id=course_id)[0].leafs.all()
        for i in leafs:
            UserLeaf.objects.update_or_create(
                user_id=user_id,
                leafs_id=i.id,
                defaults={
                    'status': 2,
                }
            )

        return JsonResponse({'status': 'ok'})
    print('-')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def update_status(request, pk):
    # получаем объект UserLeaf по его идентификатору

    user_leaf = get_object_or_404(UserLeaf, pk=pk)

    print(request.POST.get('status'))
    user_leaf.status = request.POST.get('status')
    user_leaf.save()
    return redirect(reverse('leaf_detail', args=[user_leaf.leafs.id]), pk=user_leaf.pk)


@csrf_exempt
def delete_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        course_id = data.get('course_id')

        user_course = UserCourses.objects.filter(user_id=user_id)
        user_course.filter(course_id=course_id).delete()
        return JsonResponse({'status': 'ok'})
    print('-')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def save_leaf(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        leaf_id = data.get('leaf_id')
        leaf = Leaf.objects.filter(id=leaf_id)[0]
        print(user_id, leaf_id)
        UserLeaf.objects.get_or_create(
            user_id=user_id,
            leafs=leaf,
        )
        return JsonResponse({'status': 'ok'})
    print('-')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def delete_leaf(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        leaf_id = data.get('leaf_id')

        UserLeaf.objects.filter(user_id=user_id, leafs_id=leaf_id)[0].delete()

        return JsonResponse({'status': 'ok'})
    print('-')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
