from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, default='USN-ID')
    name = models.CharField(max_length=100)
    cgpa = models.FloatField()

    def __str__(self):
        return self.name
