from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-dashboard/update-info/', views.student_update, name='student_update'),
    path('student-dashboard/training-plans/', views.student_training_plans, name='student_training_plans'),
    path('student-dashboard/schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher-dashboard/students/', views.teacher_students, name='teacher_students'),
    path('teacher-dashboard/appointments/', views.teacher_appointments, name='teacher_appointments'),
    path('teacher-dashboard/assign-training-plan/<int:user_id>/', views.assign_training_plan, name='assign_training_plan'),
    path('teacher-dashboard/delete-training-plan/<int:plan_id>/', views.delete_training_plan, name='delete_training_plan'),
    path('student-dashboard/delete-appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('teacher-dashboard/define-availability/', views.define_availability, name='define_availability'),
path('student-dashboard/schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('student-dashboard/delete-account/', views.delete_account, name='delete_account'),
    path('teacher-dashboard/delete-availability/<int:availability_id>/', views.delete_availability, name='delete_availability'),
    path('update-exercise-status/', views.update_exercise_status, name='update_exercise_status'),
    path('teacher-progress/<int:student_id>/', views.teacher_training_progress, name='teacher_training_progress'),
    path('appointment/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('logout/', views.logout_view, name='logout'),
]