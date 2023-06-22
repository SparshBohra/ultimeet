import os
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment
from google.cloud import storage
import openai

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "finoallied-rqli-12a4869f5fb5.json"

# def stereo_to_mono(audio_file_path):
#     sound = AudioSegment.from_wav(audio_file_path)
#     sound = sound.set_channels(1)
#     sound.export(audio_file_path, format="wav")

# stereo_to_mono("./test.wav")

# def split_audio_file(input_file, output_dir, segment_duration=20):
#     audio = AudioSegment.from_file(input_file)
#     duration_ms = len(audio)
#     segment_duration_ms = segment_duration * 1000
#     segment_start = 0
#     segment_end = segment_duration_ms
#     segment_count = 1
#     print(duration_ms)
#     print(segment_end)

#     while segment_end <= duration_ms:
#         segment = audio[segment_start:segment_end]
#         output_file = os.path.join(output_dir, f"segment_{segment_count}.wav")
#         segment.export(output_file, format="wav")
#         segment_start += segment_duration_ms
#         segment_end += segment_duration_ms
#         segment_count += 1
#     print(segment_count)

# def upload_to_gcs(segment_file, bucket_name):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(segment_file)
#     blob.upload_from_filename(segment_file)
#     gs_path = f"gs://{bucket_name}/{segment_file}"
#     print(gs_path)
#     return gs_path

# def transcribe_audio_file(gcs_uri):
#     client = speech.SpeechClient()

#     audio = speech.RecognitionAudio(uri=gcs_uri)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=48000,
#         language_code='en-US',  # Update with the language of your audio file
#         enable_speaker_diarization=True,
#         diarization_speaker_count=2  # Set the expected number of speakers
#     )

#     operation = client.long_running_recognize(config=config, audio=audio)
#     response = response = operation.result()#client.long_running_recognize(config=config, audio=audio)

#     transcript = ""
#     for result in response.results:
#         speaker_tag = result.alternatives[0].words[0].speaker_tag
#         #print(f"Speaker_TAG:{speaker_tag}")
#         word = result.alternatives[0].transcript
#         print(f"Speaker {speaker_tag}: {word}\n")
#         transcript += f"Speaker {speaker_tag}: {word}\n"
#     return transcript

# # Path to the long audio file
# input_file = "./test.wav"

# # Output directory for segmented audio files
# output_dir = "segments"

# # Google Cloud Storage bucket name
# bucket_name = "meeting-maestro"

# # Split the audio file into segments
# split_audio_file(input_file, output_dir)

# # Upload each segment to Google Cloud Storage and transcribe
# transcripts = []

# for file_name in os.listdir(output_dir):
#     segment_path = os.path.join(output_dir, file_name)
#     print("segment path:"+segment_path)
#     print("bucket path:"+bucket_name)
#     gcs_uri = upload_to_gcs(segment_path, bucket_name)
#     print("GCS_URI:"+gcs_uri)
#     transcript = transcribe_audio_file(gcs_uri)
#     print("transcript"+transcript)
#     transcripts.append(transcript)
#     #print("FULL YRANSCRIPT"+transcripts)

# # Print the combined transcript
# combined_transcript = " ".join(transcripts)
# print("Combined Transcript:")
# print(combined_transcript)

file_path = './combined_transcript.txt'
combined_transcript = ''

with open(file_path, 'r') as file:
    combined_transcript = file.read()

max_tokens = 4096  # maximum tokens allowed for GPT-3
# keep a buffer for response tokens. Let's assume 100 tokens for the completion
buffer_tokens = 100  
# a very long prompt
prompt = combined_transcript # suppose this is a long string of 5000 tokens

# calculate the maximum tokens we can use for the prompt
max_prompt_tokens = max_tokens - buffer_tokens

# use the Python textwrap library to split the text into chunks of `max_prompt_tokens` length
import textwrap

prompt_chunks = textwrap.wrap(prompt, max_prompt_tokens)

def agenda(text):
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
        return response.choices[0].text.strip()
    else:
        return "none"

def summarize_text(text):
    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nsummarize the meeting in less than 120 words:",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )
    if response: 
        return response.choices[0].text.strip()
    else:
        return "none"

def action_items(text):
    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nGenerate action items including action item title, the person who gave it, short description and deadline:",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )
    if response: 
        return response.choices[0].text.strip()
    else:
        return "none"

def key_points(text):
    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nWhat are the key points from the meeting",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )
    if response: 
        return response.choices[0].text.strip()
    else:
        return "none"

# summary = summarize_text(combined_transcript)
# actions = action_items(combined_transcript)
# meeting_agenda = agenda(combined_transcript)
keys = key_points(combined_transcript)
# print("Agenda:\n", meeting_agenda)
# print()
# print("Meeting Summary:\n", summary)
# print()
# print("Action Items:\n", actions)
print()
print("Key Items:\n", keys)