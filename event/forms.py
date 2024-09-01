from django import forms
from .models import Event, EVENT_TYPE, Ticket
from ckeditor.widgets import CKEditorWidget

class EventForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Event
        fields = ['title', 'category', 'type', 'start_date', 'start_time', 'end_time', 'location', 'description', 'image']
        widgets = {
                'type': forms.RadioSelect(choices=EVENT_TYPE),
                'start_date': forms.DateInput(attrs={'type': 'date'}),
                'start_time': forms.TimeInput(attrs={'type': 'time'}),
                'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_name', 'ticket_price']