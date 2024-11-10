from django.urls import path
from .views import TutorListCreateView, AvailabilityListCreateView, AvailableTutorsView, AvailabilityDetailView, TutorRegistrationView

urlpatterns = [
        path('tutors/', TutorListCreateView.as_view(), name='tutor-list-create'),
        path('availability/', AvailabilityListCreateView.as_view(), name='availability-list-create'),
        path('availability/<int:pk>/', AvailabilityDetailView.as_view(), name='availability-detail'),
        path('available-tutors/', AvailableTutorsView.as_view(), name='available-tutors'),
        path("register/", TutorRegistrationView.as_view(), name="tutor-register"),
]
