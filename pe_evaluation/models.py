from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    goal = models.CharField(max_length=50, choices=[
        ('Condicionamento Físico', 'Condicionamento Físico'),
        ('Emagrecimento', 'Emagrecimento'),
        ('Ganho de Massa Muscular', 'Ganho de Massa Muscular'),
        ('Melhora da Postura', 'Melhora da Postura'),
        ('Preparação para Testes Físicos', 'Preparação para Testes Físicos'),
        ('Melhoria da Resistência Cardiovascular', 'Melhoria da Resistência Cardiovascular'),
    ], null=True, blank=True)

    def __str__(self):
        return self.user.username

def create_or_update_student(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        Student.objects.get_or_create(user=instance)

class TrainingPlan(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='training_plans')
    plan_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plano para {self.student.user.username} criado em {self.created_at}"

class WeightHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='weight_history')
    weight = models.FloatField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.weight} kg em {self.date_recorded}"

class Appointment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.date and self.time:
            combined = timezone.make_aware(
                datetime.combine(self.date, self.time),
                timezone.get_current_timezone()
            )
            self.date = combined.date()
            self.time = combined.time()
        super().save(*args, **kwargs)

class Availability(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} {self.time} - {'Reservado' if self.is_booked else 'Disponível'}"
