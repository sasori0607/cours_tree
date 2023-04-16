from django.urls import path

from . import views

urlpatterns = [
    path('', views.TreeView.as_view(), name='tree'),
    path('leafs/<int:id>/', views.LeafView.as_view(), name='leaf_detail'),
    path('course/<int:id>/', views.CourseView.as_view(), name='course_detail'),
]