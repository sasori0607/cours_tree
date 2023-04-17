import json

from django.views.generic import ListView
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


#
#
# class TreeView(ListView):
#     template_name = 'tree/tree.html'
#     context_object_name = 'object_list'
#     model = Leaf
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         leaf = self.model.objects.all()
#         tree_data = format_tree_data(leaf)
#         ctx['data_for_d3'] = tree_data
#         ctx["user_leafs"] = []
#         if self.request.user.is_authenticated:
#             ctx["user_leafs"] = list(UserLeaf.objects.filter(user=self.request.user).values_list('leafs_id', flat=True))
#         return ctx


class TreeBranchView(ListView):
    template_name = 'tree/tree.html'
    context_object_name = 'object_list'
    model = Leaf

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        leaf = self.model.objects.all()
        url = self.request.build_absolute_uri()
        clean_url = urlparse(url)._replace(query=None).geturl()
        print(len(clean_url.split('/')), clean_url)
        if len(clean_url.split('/')) > 4:
            tree_data = process_node(leaf, Leaf.objects.filter(id=clean_url.split('/')[-2])[0])
        else:
            tree_data = format_tree_data(leaf)
        ctx['data_for_d3'] = tree_data
        ctx["user_leafs_start"] = []
        ctx["user_leafs_passed"] = []

        if self.request.user.is_authenticated:
            user_leafs = UserLeaf.objects.all()
            ctx["user_leafs_start"] = list(
                user_leafs.filter(user=self.request.user, status='ST').values_list('leafs_id', flat=True))
            ctx["user_leafs_passed"] = list(
                user_leafs.filter(user=self.request.user, status='CP').values_list('leafs_id', flat=True))
            print( user_leafs.filter(user=self.request.user, status='ST').values_list('leafs_id', flat=True))
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
        # if key_point
        if leafs.filter(parent__id=clean_url.split('/')[-2]):
            children = leafs.filter(parent__id=clean_url.split('/')[-2])
            ctx['children'] = children
        if leaf.parent and leafs.filter(id=leaf.parent.id):
            parent = leafs.filter(id=leaf.parent.id)
            ctx['parent'] = parent

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

        print(course)
        ctx['1'] = course

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
            UserLeaf.objects.get_or_create(
                user_id=user_id,
                leafs_id=i.id,
            )

        return JsonResponse({'status': 'ok'})
    print('-')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def delete_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        course_id = data.get('course_id')

        user_course = UserCourses.objects.filter(user_id=user_id)
        leafs_to_live = []
        leafs_on_rm = []
        for course in user_course:
            if course.course.id == int(course_id):
                for i in course.course.leafs.all():
                    leafs_on_rm.append(i)
            else:
                for i in course.course.leafs.all():
                    leafs_to_live.append(i)
        print(leafs_on_rm)
        print(leafs_to_live)

        for i in set(leafs_on_rm) - set(leafs_to_live):
            UserLeaf.objects.filter(user_id=user_id, leafs_id=i.id).all().delete()

        user_course.filter(course_id=course_id).delete()
        return JsonResponse({'status': 'ok'})
    print('-')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
