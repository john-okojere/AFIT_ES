from django.db import models
from ckeditor.fields import RichTextField
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Category/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.name

EVENT_TYPE = (
    ('Single Event', 'Single Event'),
    ('Recurring Event', 'Recurring Event')
)

class Event(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Event Type", max_length=255, choices=EVENT_TYPE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255, verbose_name="Where will the event take place")
    description = RichTextField()
    image = models.ImageField(upload_to='Event/%Y/%m/%d/')
    ticket_name = models.CharField(max_length=255, verbose_name="Ticket Name")
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ticket Price")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_free(self):
        return self.ticket_price <= 0

    def __str__(self):
        return self.title

class Attendee(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_name = models.CharField(max_length=255)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)  # Adjusted to handle currency
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_name} - {self.event.title}"

class Payment(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255)  # e.g., 'Credit Card', 'Crypto', etc.
    transaction_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Payment for Ticket ID {self.ticket.id} - Amount {self.amount}"
