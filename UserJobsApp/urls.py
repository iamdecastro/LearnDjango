from django.urls import path,include
from . import views


urlpatterns = [
    path("",views.index),
    path("register",views.register),
    path("login",views.login),
    path("log_out",views.log_out),
    path("dashboard",views.dashboard),
    path("Jobs/New",views.new_job),
    path("Jobs/Create",views.create_job),
    path("Jobs/Edit/<int:Job_ID>",views.edit_job),
    path("Jobs/Update/<int:Job_ID>",views.update_job),
    path("Jobs/View/<int:Job_ID>",views.view_job),
    path("Jobs/Assign/<int:Job_ID>",views.assign_job),
    path("Jobs/Unassign/<int:Job_ID>",views.unassign_job),
    path("Jobs/Remove/<int:Job_ID>",views.remove_job)


]


