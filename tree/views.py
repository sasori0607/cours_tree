from django.views.generic import ListView
from .models import Leaf, LeafKeypoint, Course, CustomUser, UserLeaf
from urllib.parse import urlparse


def format_tree_data(data):
    def process_node(node):
        children = [process_node(child) for child in data if child.parent_id == node.id]
        return {
            "name": node.name,
            "id": node.id,
            "children": children,
            "size": 1000  # здесь можно задать любое значение для атрибута size
        }

    # находим корневой элемент, то есть элемент без родителя
    root = next((item for item in data if item.parent_id is None), None)
    # обрабатываем корневой элемент и все его дочерние элементы
    return process_node(root)


class TreeView(ListView):
    template_name = 'tree/tree.html'
    context_object_name = 'object_list'
    model = Leaf

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        leaf = self.model.objects.all()
        tree_data = format_tree_data(leaf)
        ctx['data_for_d3'] = tree_data
        print(self.request.user)
        ctx["user_leafs"] = []
        if self.request.user.is_authenticated:
            print('+')
            ctx["user_leafs"] = list(UserLeaf.objects.filter(user=self.request.user).values_list('id', flat=True))
        # print(UserLeaf.objects.filter(user=self.request.user).values_list('id', flat=True)[0])


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
        print(course.leafs)
        ctx['1'] = course

        return ctx
