from django.db import models
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Category/%y/%m/%d/', null=True)

    def __str__(self):
        return self.name

EVENT_TYPE = (
    ('Single Event', 'Single Event'),
    ('Recurring Event', 'Recurring Event')
)

class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Event Type",max_length=255, choices=EVENT_TYPE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255, verbose_name="Where will the event take place")
    description = RichTextField()
    image = models.ImageField(upload_to='Event/%y/%m/%d/')
    ticket_name = models.CharField( max_length=255)
    ticket_price = models.IntegerField()

    def is_free(self):
        if self.price == 0:
            return True 
        return False 
    
    def __str__(self):
        return self.title