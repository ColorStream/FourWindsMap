#from django.contrib.gis.db import models
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint

# Create your models here.

class Verification(models.Model):
    upload = models.ImageField(null=True) #requires pillow
    a1 = models.CharField(null=True, max_length=250) #a is short for answers
    a2 = models.CharField(null=True, max_length=250)
    a3 = models.CharField(null=True, max_length=250)

    def clean(self): #In case it somehow slips through the cracks...
        cleaned_data = super().clean()
        upload = cleaned_data.get("upload")
        answers = [cleaned_data.get("a1"), cleaned_data.get("a2"), cleaned_data.get("a3")]
        if upload == None and None in answers:
            raise ValidationError("You must validate with either an upload or questionnaire answers!")
        
    def __str__(self):
        return f'{self.a1}, {self.a2}, {self.a2}'
    
class Markers(models.Model):
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    fromyear = models.SmallIntegerField(null=True)
    geojson_data = models.JSONField(default=list, null=False)
    storytext = models.CharField(max_length=350, null=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    #Accompanying verification model - sets NULL when verification model is deleted
    verification = models.OneToOneField(Verification, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f'{self.fromyear}: {self.storytext[:20]}'
    
    def geojson_update(self): #should be updated through serializer, but in case
        if self.approved == True:
            self.geojson_data['approved'] = True
        elif self.approved == False or None:
            self.geojson_data['approved'] = False
        return self.save()
    
    class Meta:
        ordering = ['-date_posted'] #order by most recent
        constraints = [UniqueConstraint(fields=['fromyear', 'storytext'], name='unique_story')] #prevent duplicate fromyear and storytext