from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    has_used_symptom_checker = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

class symptoms(models.Model):
    symptomID = models.CharField(max_length = 122)
    symptomDescription = models.CharField(max_length = 122)

class Usersymptoms(models.Model):
    userID = models.CharField(max_length = 122)
    symptomID = models.CharField(max_length = 122)
    symptomEnteredAt = models.CharField(max_length = 122)

class diseasePrediction(models.Model):
    predictionID = models.CharField(max_length = 122)
    userID = models.CharField(max_length = 122)
    diseaseName = models.CharField(max_length = 122)
    predictionAccuracy = models.CharField(max_length = 122)

class recommendation(models.Model):
    recommendationID = models.CharField(max_length = 122)
    userID = models.CharField(max_length = 122)
    recommendationText = models.CharField(max_length = 122)
    recommendationType = models.CharField(max_length = 122)

# class appointments(models.Model):
#     userID = models.CharField(max_length = 122)
#     name = models.CharField(max_length = 122)

class chatbotInteraction(models.Model):
    conversationID = models.CharField(max_length = 122)
    userID = models.CharField(max_length = 122)
    message = models.CharField(max_length = 122)
    response = models.CharField(max_length = 122)
    interactionTimestamp = models.CharField(max_length = 122)

# class medicalHistory(models.Model):
#     userID = models.CharField(max_length = 122)
#     name = models.CharField(max_length = 122)

# class healthMetrics(models.Model):
#     userID = models.CharField(max_length = 122)
#     name = models.CharField(max_length = 122)

class notificationsAlerts(models.Model):
    notificationID = models.CharField(max_length = 122)
    userID = models.CharField(max_length = 122)
    notificationType = models.CharField(max_length = 122)
    notificationMessage = models.CharField(max_length = 122)
    sentAt = models.CharField(max_length = 122)
