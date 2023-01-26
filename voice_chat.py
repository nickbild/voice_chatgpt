################################################################
# Nick Bild
# January 2023
# https://github.com/nickbild/voice_chatgpt
#
# Voice-controlled ChatGPT prompt
################################################################
import os
import io
import sys
import asyncio
import argparse
import pyaudio
import wave
from google.cloud import speech
from google.cloud import texttospeech
from ChatGPT_lite.ChatGPT import Chatbot


gpt_response = ""


def speech_to_text(speech_file):
    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
            content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    stt = ""
    for result in response.results:
        stt += result.alternatives[0].transcript

    return stt


def ask_chat_gpt(args, prompt):
    global gpt_response
    chat = Chatbot(args.session_token, args.bypass_node)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat.wait_for_ready())
    response = loop.run_until_complete(chat.ask(prompt))
    chat.close()
    loop.stop()
    
    gpt_response = response['answer']

    return


def text_to_speech(tts):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=tts)

    # Build the voice request, select the language code ("en-US") and the ssml
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("result.wav", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)

    return


def record_wav():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 4096
    record_secs = 3
    dev_index = 1
    wav_output_filename = 'input.wav'

    audio = pyaudio.PyAudio()

    # Create pyaudio stream.
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []

    # Loop through stream and append audio chunks to frame array.
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # Stop the stream, close it, and terminate the pyaudio instantiation.
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio frames as .wav file.
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session_token_file', type=str, default="openai_session.txt")
    parser.add_argument('--bypass_node', type=str, default="https://gpt.pawan.krd")
    args = parser.parse_args()

    # Get OpenAI credentials from file.
    text_file = open(args.session_token_file, "r")
    args.session_token = text_file.read()
    text_file.close()

    # Get WAV from microphone.
    record_wav()

    # Convert audio into text.
    question = speech_to_text("input.wav")
    
    # Send text to ChatGPT.
    print("Asking: {0}".format(question))
    asyncio.coroutine(ask_chat_gpt(args, question))
    print("Response: {0}".format(gpt_response))

    # Convert ChatGPT response into audio.
    text_to_speech(gpt_response)

    # Play audio of reponse.
    os.system("aplay result.wav")


if __name__ == "__main__":
    main()
