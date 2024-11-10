from django.urls import path
from .views import StudentListCreateView, EnrollmentListCreateView, EnrollmentDetailView

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
]