from django.urls import path

from . import views

urlpatterns = [
    path('', views.TreeBranchView.as_view(), name='tree'),
    path('tree/<int:id>/', views.TreeBranchView.as_view(), name='leaf_branch'),
    path('leafs/<int:id>/', views.LeafView.as_view(), name='leaf_detail'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('course/<int:id>/', views.CourseView.as_view(), name='course_detail'),
    path('course/save_course/', views.save_course, name='save_course'),
    path('course/delete_course/', views.delete_course, name='delete_course'),
    path('course/save_leaf/', views.save_leaf, name='save_leaf'),
    path('course/delete_leaf/', views.delete_leaf, name='delete_leaf'),
    path('update_status/<int:pk>/', views.update_status, name='update_status'),
]