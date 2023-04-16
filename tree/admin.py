from django.contrib import admin
from tree.models import *

admin.site.register(Leaf)
admin.site.register(Course)
admin.site.register(CustomUser)
admin.site.register(LeafKeypoint)
admin.site.register(UserCourses)
admin.site.register(UserLeaf)

