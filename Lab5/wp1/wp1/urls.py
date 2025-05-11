"""
URL configuration for wp1 project.

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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path 
from journal import views 
  
urlpatterns = [ 
    # головна сторінка проекту
    re_path(r'^(?:index.html/)?$', views.index, name='authorization'),     
    # user + необов'язкове закінчення .html:
    re_path(r'^user(?:\.html)?/', views.user),   
    # teacher + необов'язкове закінчення .html:
    re_path(r'^teacher(?:\.html)?/', views.teacher),
    # student + необов'язкове закінчення .html:
    re_path(r'^student(?:\.html)?/', views.student), 

    path('api/groups/', views.groups), 
    path('api/users/hello', views.findUser),
    path('api/users/<int:id>', views.getUser),
    path('api/users/new', views.newUser),
    path('api/users/edit', views.editUser),
    path('api/users/', views.users),        
    path('api/users/delete/<int:id>', views.deleteUser),
    path('api/subjects/', views.subjects),         
    path('api/journals/', views.journals), 
    path('api/lessons/find', views.findLesson),
    path('api/lessons/new', views.newLesson),
    path('api/lessons/edit', views.editLesson),
    path('api/lessons/delete/<int:id>', views.deleteLesson),
    path('api/rating/', views.rating),  
    path('api/rating/student/<int:idStudent>/<int:idJournal>/<int:idSubject>', views.ratingStudent),    
    path('api/rating/new', views.newRating),
    path('api/rating/edit', views.editRating),
    path('api/rating/delete', views.deleteRating),        
]
