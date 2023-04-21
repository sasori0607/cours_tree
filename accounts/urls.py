from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from . import views
from accounts.views import ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('register/', views.register, name='register'),
    path('course-changes/<int:id>/', views.TeacherCourseView.as_view(), name='course_changes'),
    path('course-changes/<int:id>/', views.TeacherCourseView.as_view(), name='course_changes'),
    path('change-leafs/', views.change_leafs, name='change_leafs'),
    path('change-status-course/', views.change_status_course, name='change_status_course'),
    # path('', include('django.contrib.auth.urls')),
]