from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tutor_profile", null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Availability(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField()

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

"""
API to register a new tutor user.
"""
class TutorRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow unrestricted access

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        name = request.data.get("name")

        if not username or not password or not name:
            return Response(
                {"detail": "Username, password, and name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the user and link them to a tutor
        user = User.objects.create_user(username=username, password=password)
        tutor = Tutor.objects.create(user=user, name=name)

        return Response(
            {
                "id": tutor.id,
                "username": user.username,
                "name": tutor.name,
            },
            status=status.HTTP_201_CREATED,
        )
