from django.urls import path
from . import views

app_name = "tasklists"

urlpatterns = [
    # ADD TASK AND RETRIEVE TASK
    path('', views.todo_index, name="toDo"),
    path('delete/<uuid:pk>/', views.delete, name="task_delete"),
    path('status/change/<uuid:pk>/', views.changestatus, name="change_status"),
    path('edit/<uuid:pk>/', views.edittask, name="edit_task"),
]
