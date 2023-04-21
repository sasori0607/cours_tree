from django.contrib import admin
from tree.models import *

admin.site.register(Leaf)
admin.site.register(Course)
admin.site.register(LeafKeypoint)
admin.site.register(UserCourses)
admin.site.register(UserLeaf)


@admin.register(Diplomas)
class DiplomasAdmin(admin.ModelAdmin):
    fields = ('user', 'course', 'created_at')
    list_display = ('user', 'course')


@admin.register(CoursesLogs)
class CoursesLogsAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'created_at')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = (
    'password', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'gradation')
