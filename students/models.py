from django.db import models
from tutors.models import Tutor
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile", null=True, blank=True)

    def __str__(self):
        return self.user.username if self.user else "Unlinked Student"

class Enrollment(models.Model):
    student = models.ForeignKey(
        'students.Student',  # Assuming there's a Student model
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student} -> {self.tutor} at {self.start_time} for {self.duration} minutes"
