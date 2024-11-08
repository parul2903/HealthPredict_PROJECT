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
    

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    doctor = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    phone = models.CharField(max_length=15)
   

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.time}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


## NEW

# models.py

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)  # Options: "male" or "female"

    def __str__(self):
        return f"User - Age: {self.age}, Gender: {self.gender}"

class SymptomDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()  # Store symptoms as a comma-separated string
    predicted_disease = models.CharField(max_length=100)
    description = models.TextField()  # Description of the disease
    def __str__(self):
        return f"Prediction: {self.predicted_disease} for {self.user}"
    


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()  # Years of experience
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)  # New field for image

    def __str__(self):
        return self.name



class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/')
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-pub_date']  # Show most recent posts first



class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_frequency = models.PositiveIntegerField()
    diet_quality = models.PositiveIntegerField()
    sleep_hours = models.PositiveIntegerField()
    appointment_feedback = models.CharField(max_length=20, choices=[
        ('helpful', 'Helpful'),
        ('somewhat helpful', 'Somewhat Helpful'),
        ('not helpful', 'Not Helpful')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Health Data for {self.user.username} on {self.created_at}"
    
class updateData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_frequency = models.PositiveIntegerField()
    diet_quality = models.PositiveIntegerField()
    sleep_hours = models.PositiveIntegerField()
    appointment_feedback = models.CharField(
        max_length=20,
        choices=[('helpful', 'Helpful'), ('somewhat helpful', 'Somewhat Helpful'), ('not helpful', 'Not Helpful')]
    )

    def __str__(self):
        return f"Health Data for {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    # Add other fields if necessary

    def __str__(self):
        return f"{self.user.username}'s Profile"