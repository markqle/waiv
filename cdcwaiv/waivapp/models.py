from django.db import models

# Create your models here.
class student_personal_info(models.Model):
    csulb_id = models.CharField(primary_key= True, max_length= 15, unique= True)
    participant_id = models.IntegerField(max_length= 15, unique= True)
    last_name = models.CharField(null=False,max_length=30)
    first_name = models.CharField(null=False,max_length=30)
    birthdate = models.DateField()
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    employ_goal = models.CharField(max_length= 200)
    city = models.CharField(max_length= 30)
    enrollment_date = models.DateField()
    updated_date = models.DateTimeField(auto_now_add=True)
    case_manager = models.CharField()



