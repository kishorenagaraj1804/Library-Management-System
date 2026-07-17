"""
URL configuration for Library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: rom path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login, name='login'),
    path('home/', views.home,name='home'),
    path('student_list/',views.student_list, name='student_list'),
    path('add_student/',views.add_student, name='add_student'),
    path('book/',views.book, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path('return_book/', views.return_book, name='return_book'),
    path('delete_book/<int:id>/', views.delete_book, name='delete_book'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('edit_book/<int:id>/', views.edit_book, name='edit_book'),
    path('export_student_excel/',views.export_student_excel, name='export_student_excel'),
    path('export_book_excel/',views.export_book_excel, name='export_book_excel'),
    path('setting/',views.setting, name='setting'),
    
]
