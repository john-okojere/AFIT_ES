from django import forms
from .models import Event, EVENT_TYPE
from ckeditor.widgets import CKEditorWidget

class EventForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Event
        fields = ['title', 'category', 'type', 'start_date', 'start_time', 'end_time', 'location', 'description', 'image', 'ticket_name', 'ticket_price']
        widgets = {
                'type': forms.RadioSelect(choices=EVENT_TYPE),
                'start_date': forms.DateInput(attrs={'type': 'date'}),
                'start_time': forms.TimeInput(attrs={'type': 'time'}),
                'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
