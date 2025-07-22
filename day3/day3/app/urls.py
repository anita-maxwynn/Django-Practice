from django.urls import path
from .views import student_list,student_create,student_delete,student_detail,student_update

urlpatterns = [
    path('', student_list, name='student_list'),
    path('student/<uuid:student_id>/', student_detail, name='student_detail'),
    path('student/create/', student_create, name='student_create'),
    path('student/update/<uuid:student_id>/', student_update, name='student_update'),
    path('student/delete/<uuid:student_id>/', student_delete, name='student_delete')
]