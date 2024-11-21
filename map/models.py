#from django.contrib.gis.db import models
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Markers(models.Model):
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    fromyear = models.SmallIntegerField(null=True) #TODO be sure to have form validation (must be > 1950 || )
    geojson_data = models.JSONField(default=list, null=False)
    storytext = models.CharField(max_length=350, null=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False) #TODO when moderation panel finished, include geojson update for approval

    def __str__(self):
        return f'{self.fromyear}: {self.storytext[:20]}'
    
    def geojson_update(self): #make sure this is right later; should only be used by admin
        if self.approved == True:
            self.geojson_data['approved'] = True
        elif self.approved == False or None:
            self.geojson_data['approved'] = False
        return self.save()
            
    
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

    def clean(self): #In case it somehow slips through the cracks...
        cleaned_data = super().clean()
        upload = cleaned_data.get("upload")
        answers = [cleaned_data.get("a1"), cleaned_data.get("a2"), cleaned_data.get("a3")]
        if upload == None and None in answers:
            raise ValidationError("You must validate with either an upload or questionnaire answers!")
        
    def __str__(self):
        return f'{self.marker}'