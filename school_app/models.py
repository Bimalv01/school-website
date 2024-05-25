from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator,RegexValidator
from django.contrib.auth.models import User
PHONE_REGEX = '^[0-9]{10}$'
NAME_REGEX = '^[A-Za-z ]+$'



# Create your models here.
class school_files(models.Model):
    name=models.CharField(max_length=50)
    
def __str__(self):
    return self.name

class school_file(models.Model):
    subject_name=models.CharField(max_length=100)
    year=models.CharField(max_length=50)
    course = models.CharField(max_length=100)   # New field for course name
    upload=models.ImageField(upload_to='materials/') 

    
    def __str__(self):
        return self.subject_name
    


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    COURSE_CHOICES = (
        ('science', 'science'),
        ('commerce', 'commerce'),
        ('humanitice', 'humanitice'),
       
        
    )

    name = models.CharField(max_length=200, validators=[
        MinLengthValidator(2),
        RegexValidator(regex=NAME_REGEX, message='Enter a valid name with alphabets and spaces only')
    ])
    email = models.EmailField(max_length=254, validators=[EmailValidator()])
    parent_name = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    parent_contact = models.CharField(max_length=15, validators=[
        MinLengthValidator(10),
        RegexValidator(regex=PHONE_REGEX, message='Enter a valid 10-digit phone number')
    ])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    
    date_of_birth = models.DateField()
    registration_date = models.DateTimeField(auto_now_add=True)
    student_image = models.ImageField(upload_to='students/images/', null=True, blank=True)
    roll_number = models.CharField(max_length=50, unique=True, blank=True)
    password = models.CharField(max_length=100, validators=[MinLengthValidator(6)])
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)
        if not self.roll_number:
            self.roll_number = '23HS' + str(self.id)
            super(Student, self).save(*args, **kwargs)

    def _str_(self):
        return self.name
    
#feedback
class Feedback(models.Model):
    roll_number = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=200)
    date = models.DateField()
    feedback = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)

    

    