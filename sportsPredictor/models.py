from django.db import models

# Create your models here.

class PredictedHistory(models.Model):
    game = models.CharField(max_length=255)
    team_1 = models.CharField(max_length=255)
    team_2 = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    predicted_on = models.DateTimeField(auto_now_add=True)