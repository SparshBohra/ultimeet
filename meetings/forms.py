from django import forms
from django.forms import ModelForm
from .models import meetings, transcript, summary


class MeetingForm(ModelForm):
    class Meta:
        model = meetings

        fields=['meeting_id','meeting_title','meeting_datetime','meeting_organizer','meeting_type','meeting_channel','meeting_participants']        

 