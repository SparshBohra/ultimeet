# use the Python textwrap library to split the text into chunks of `max_prompt_tokens` length
import textwrap
import openai

# django imports
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response, RequestContext, log
from .models import meetings, transcript, summary
from .forms import MeetingForm

# maximum tokens allowed for GPT-3
max_tokens = 4096  
# keep a buffer for response tokens. Let's assume 100 tokens for the completion
buffer_tokens = 100  
# calculate the maximum tokens we can use for the prompt
max_prompt_tokens = max_tokens - buffer_tokens

def meeting_information(request, id):
    meeting_object = meetings.objects.get(meeting_id = id)
    return HttpResponse("{%s}" % meeting_object)

def meeting_agenda(request, id):
    trancript_object = transcript.objects.get(meeting_id = id)
    prompt = trancript_object.transcript_raw
    prompt_chunks = textwrap.wrap(prompt, max_prompt_tokens)

    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nAgenda of meeting in less than 12 words",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )
    if response: 
        output = response.choices[0].text.strip()
        return HttpResponse("{%s}" % output)
    else:
        return HttpResponse("{None}")

def meeting_summary(request, id):
    trancript_object = transcript.objects.get(meeting_id = id)
    prompt = trancript_object.transcript_raw
    prompt_chunks = textwrap.wrap(prompt, max_prompt_tokens)

    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nGive me a brief summary of the meeting in less than 120 words",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )
    if response: 
        output = response.choices[0].text.strip()
        return HttpResponse("{%s}" % output)
    else:
        return HttpResponse("{None}")

def meeting_keypoints(request, id):
    trancript_object = transcript.objects.get(meeting_id = id)
    prompt = trancript_object.transcript_raw
    prompt_chunks = textwrap.wrap(prompt, max_prompt_tokens)

    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nGive me keypoints discussed in the meeting in a list format",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )
    if response: 
        output = response.choices[0].text.strip()
        return HttpResponse("{%s}" % output)
    else:
        return HttpResponse("{None}")

def meeting_participants(request, id):
    meeting_object = meetings.objects.get(meeting_id = id)
    participants = []
    for i in range(len(meeting_object.meeting_participants)):
        participants[i] = meeting_object.meeting_participants[i]
    return HttpResponse("{%s}" % participants)

def new_meeting(request):
    if request.POST:
        meeting_form = MeetingForm(request.POST)
        
        if (meeting_form.is_valid()):
            log.debug("test....")
            meeting=meeting_form.save()
            meeting.save()

            return redirect('/meeting_information/')
        else:
            meeting_form=MeetingForm()
            return render_to_response('{}',{'form':meeting_form},context_instance=RequestContext(request))