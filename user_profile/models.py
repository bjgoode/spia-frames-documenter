from django.db import models
from django.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class State(models.Model):     

#    current_project =   
#    current_role = 

    MODE_CHOICES = [
        (1,'preview'),
        (2,'edit'),    
    ]
    current_mode = models.PositiveIntegerField(choices=MODE_CHOICES, default=1)
    last_page = models.URLField(default="/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    