from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('list_students/', views.list_students_view, name='list_students'),
    path('edit_student/<int:student_id>/', views.edit_student_view, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student_view, name='delete_student'),
]
