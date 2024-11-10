from rest_framework import generics
from .models import Tutor, Availability
from .serializers import TutorSerializer, AvailabilitySerializer
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from django.db.models import F, ExpressionWrapper, Func, DateTimeField
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

class TutorListCreateView(generics.ListCreateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class AvailabilityListCreateView(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    """
    Filter availabilities based on query parameters: start_time and duration.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        start_time = self.request.query_params.get('start_time')
        duration = self.request.query_params.get('duration')

        if start_time and duration:
            requested_start_time = parse_datetime(start_time)
            requested_duration = int(duration)

            # Ensure the requested start_time is on the hour or half-hour
            if requested_start_time.minute not in {0, 30}:
                raise ValidationError("start_time must be on the hour (:00) or half-hour (:30).")

            requested_end_time = requested_start_time + timedelta(minutes=requested_duration)

            # Filter availabilities based on overlap
            queryset = queryset.filter(
                start_time__lte=requested_start_time,  # Starts before or at the requested start
            ).exclude(
                start_time__gte=requested_end_time  # Exclude availabilities that start after requested end
            )

            # Exclude availabilities that end before the requested end
            queryset = [
                availability for availability in queryset
                if (availability.start_time + timedelta(minutes=availability.duration)) >= requested_end_time
            ]

        return queryset

    """
    Validate that the new availability does not overlap with existing availabilities for the tutor.
    TODO: may be wiser to expand the overlapping availability
    """
    def perform_create(self, serializer):
        tutor = serializer.validated_data['tutor']
        start_time = serializer.validated_data['start_time']
        duration = serializer.validated_data['duration']
        end_time = start_time + timedelta(minutes=duration)

        # Check for overlapping availabilities for the same tutor
        overlapping_availabilities = Availability.objects.filter(
            tutor=tutor,
            start_time__lt=end_time,  # Starts before the end of the new availability
            start_time__gte=start_time - timedelta(minutes=duration)  # Prevent overlaps before the new start time
        )

        if overlapping_availabilities.exists():
            raise ValidationError("This availability overlaps with an existing one.")

        # If no overlaps, save the availability
        serializer.save()

class AvailableTutorsView(APIView):
    """
    Get a list of tutors available for a given start_time and duration.
    """
    def get(self, request):
        start_time = request.query_params.get('start_time')
        duration = request.query_params.get('duration')

        if not start_time or not duration:
            raise ValidationError("start_time and duration are required parameters.")

        requested_start_time = parse_datetime(start_time)
        if requested_start_time.minute not in {0, 30}:
            raise ValidationError("start_time must be on the hour (:00) or half-hour (:30).")

        requested_duration = int(duration)
        if requested_duration not in {30, 60}:
            raise ValidationError("duration must be either 30 or 60 minutes.")

        requested_end_time = requested_start_time + timedelta(minutes=requested_duration)

        # Query availabilities that overlap the requested time
        available_availabilities = Availability.objects.filter(
            start_time__lte=requested_start_time,  # Starts before or at the requested start
        ).exclude(
            start_time__gte=requested_end_time  # Exclude availabilities starting after requested end
        )

        # Post-process to filter by end_time
        available_availabilities = [
            availability for availability in available_availabilities
            if (availability.start_time + timedelta(minutes=availability.duration)) >= requested_end_time
        ]

        # Extract tutors from the available availabilities
        tutor_ids = {availability.tutor_id for availability in available_availabilities}
        available_tutors = Tutor.objects.filter(id__in=tutor_ids)

        serializer = TutorSerializer(available_tutors, many=True)

        return Response(serializer.data)

class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
