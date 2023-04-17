from django.urls import path

from . import views

urlpatterns = [
    path('', views.TreeBranchView.as_view(), name='tree'),
    path('tree/<int:id>/', views.TreeBranchView.as_view(), name='leaf_branch'),
    path('leafs/<int:id>/', views.LeafView.as_view(), name='leaf_detail'),
    path('course/<int:id>/', views.CourseView.as_view(), name='course_detail'),
    path('course/save_course/', views.save_course, name='save_course'),
    path('course/delete_course/', views.delete_course, name='delete_course'),
]