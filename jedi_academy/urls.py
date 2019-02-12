"""jedi_academy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from academy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('candidate', views.new_candidate),
    path('test', views.entry_test),
    path('jedi/', views.jedi_list),
    path('jedi/answertest/<int:candidate_id>/', views.answer_test),
    path('jedi/send/<int:jedi_id>/<int:candidate_id>/', views.jedi_candidates),
    path('jedi/jedicand', views.jedi_list_candidate),
    path('index', views.index),
    path('count/', views.show_jedi_count),
    path('jedi_one/', views.jedi_candidate_one),

]

