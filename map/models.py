#from django.contrib.gis.db import models
from django.db import models

# Create your models here.

class Markers(models.Model):
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    fromyear = models.SmallIntegerField(null=True) #be sure to have form validation (must be > 1950 || )
    geojson_data = models.JSONField(default=list, null=False)
    storytext = models.CharField(max_length=350, null=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.fromyear}: {self.storytext[:20]}'
    
    #def geojson_update(self):
            
    
    class Meta:
        ordering = ['date_posted']
        # add a constraint here later, or maybe just do form validation
        #unique_together= ['latitude, longitude, storytext']

class Verification(models.Model):
    upload = models.ImageField(null=True) #INSTALL PILLOW
    a1 = models.CharField(null=True, max_length=250) #a is short for answers
    a2 = models.CharField(null=True, max_length=250)
    a3 = models.CharField(null=True, max_length=250)

    marker = models.ForeignKey("Markers", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.marker}'