from django.db import models

# Create your models here.
class meetings(models.Model):
    meeting_id = models.IntegerField(primary_key=True, auto_created=True)
    meeting_datetime = models.DateTimeField(null=False, blank=True)
    meeting_title = models.CharField(max_length=100, null=False, blank=True)
    meeting_organizer = models.CharField(max_length=100, null=False, blank=True)
    meeting_type = models.CharField(max_length=100, null=False, blank=True)
    meeting_channel = models.CharField(max_length=100, null=False, blank=True)
    meeting_participants = models.CharField(max_length=5000, null=False, blank=True)

    def __str__(self):
        return self.meeting_id

    class Meta:
        db_table = 'meetings'

class transcript(models.Model):
    transcript_id = models.IntegerField(primary_key=True, auto_created=True)
    meeting_id = models.ForeignKey(meetings, on_delete=models.CASCADE)
    transcript_raw = models.CharField(max_length=9999999, null=False, blank=True)

    def __str__(self):
        return self.transcript_id

    class Meta:
        db_table = 'transcript'

class summary(models.Model):
    summary_id = models.IntegerField(primary_key=True, auto_created=True)
    meeting_id = models.ForeignKey(meetings, on_delete=models.CASCADE)
    meeting_summary = models.CharField(max_length=1000, null=False, blank=True)
    meeting_agenda = models.CharField(max_length=500, null=False, blank=True)
    meeting_keypoints = models.CharField(max_length=1000, null=False, blank=True)

    def __str__(self):
        return self.summary_id

    class Meta:
        db_table = 'summary'
