"""
URL configuration for medication_scheduler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from health_service.detail_views import save_user_details, get_user_details, update_user_details, delete_user_details
from health_service.patient_table import save_patient_details,get_patient_details,update_patient_details,delete_patient_details
from health_service.schedule_views import save_medicine_details,get_medication_details,update_medication_details,delete_medication_details
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_details', save_user_details, name="save_user_details"),
    path('user_details/<str:user_id>', get_user_details, name="get_user_details"),
    path('user_details/update/<str:user_id>', update_user_details, name="update_user_details"),
    path('user_details/delete/<str:user_id>', delete_user_details, name="delete_user_details"),
    path('patient_details', save_patient_details , name="save_patient_details"),
    path('patient_details/<str:patient_id>', get_patient_details, name="get_patient_details"),
    path('patient_details/update/<str:patient_id>', update_patient_details, name="update_patient_details"),
    path('patient_details/delete/<str:patient_id>', delete_patient_details, name="delete_patient_details"),
    path('medication_details', save_medicine_details,name='save_medicine_details'),
    path('medication_details/<str:patient_id>', get_medication_details, name="get_medication_details"),
    path('medication_details/update/<str:patient_id>',update_medication_details, name="update_medication_details"),
    path('medication_details/delete/<str:patient_id>', delete_medication_details, name="delete_medication_details"),
]
