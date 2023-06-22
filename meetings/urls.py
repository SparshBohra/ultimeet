from django.urls import path
from . import views

urlpatterns = [
    path('meeting_information/<int:id>', views.meeting_information, name='meeting_information'),
    path('meeting_agenda/<int:id>', views.meeting_agenda, name='meeting_agenda'),
    path('meeting_summary/<int:id>', views.meeting_summary, name='meeting_summary'),
    path('meeting_keypoints/<int:id>', views.meeting_keypoints, name='meeting_keypoints'),
    path('meeting_participants/<int:id>', views.meeting_participants, name='meeting_participants'),
    path('new_meeting/<int:id>', views.new_meeting, name='new_meeting'),
]