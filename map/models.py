from django.db import models

# Create your models here.

class Markers(models.Model):
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    fromyear = models.SmallIntegerField(null=True) #be sure to have form validation (must be > 1950 || )
    storytext = models.CharField(max_length=350, null=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.latitude}, {self.longitude}: {self.storytext[:20]}'
    
    class Meta:
        ordering = ['date_posted']
        # add a constraint here later, or maybe just do form validation