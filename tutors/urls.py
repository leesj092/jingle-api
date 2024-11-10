from django.urls import path
from .views import TutorListCreateView, AvailabilityListCreateView, AvailableTutorsView

urlpatterns = [
        path('tutors/', TutorListCreateView.as_view(), name='tutor-list-create'),
        path('availability/', AvailabilityListCreateView.as_view(), name='availability-list-create'),
        path('available-tutors/', AvailableTutorsView.as_view(), name='available-tutors'),
]
