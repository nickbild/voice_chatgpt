# VoiceGPT

VoiceGPT is a voice assistant that leverages the powerful ChatGPT chatbot to answer your questions.  You speak the requests, and VoiceGPT responds with realistic, synthesized speech.

![](https://raw.githubusercontent.com/nickbild/voice_chatgpt/main/media/voicegpt_title.jpg)

## How It Works

![](https://raw.githubusercontent.com/nickbild/voice_chatgpt/main/media/voicegpt_overview.jpg)

I chose a Raspberry Pi 4 single board computer to host the project, because it runs Linux and provides a lot of versatility.  A custom [Python script](https://github.com/nickbild/voice_chatgpt/blob/main/voice_chat.py) collects audio of a speaker's voice using a USB microphone.  The Google Cloud Speech-to-Text API is then used to convert that audio file into text.  The text is then queried against ChatGPT using an [unofficial API](https://github.com/acheong08/ChatGPT-lite) that returns a text string of ChatGPT's response.  That response is then processed by Google Cloud's Text-to-Speech API to turn it into realistic, synthetic speech that the Raspberry Pi can play through a speaker.

The concept of a voice assistant is well established (e.g. Google Home, Amazon Alexa), but this proof of concept shows how a voice assistant can use ChatGPT, which, in my opinion, provides a far better experience than anything currently on the market.

In the future, I may add a keyword spotting algorithm to the project so that it can always run in the background, waiting for a keyword (e.g. "Hey, ChatGPT") to wake up.  Before I have the chance to do much of anything else, there will probably be a commercial product including ChatGPT on the backend — then I'll just buy that because it will be smaller and better.  :)

## Media

[Demonstration video](https://www.youtube.com/watch?v=ajUCMu7de80)

![](https://raw.githubusercontent.com/nickbild/voice_chatgpt/main/media/voicegpt_sm.jpg)

## Bill of Materials

- 1 x Raspberry Pi 4
- 1 x USB microphone (I use a webcam with a built-in microphone)
- 1 x Speaker

## About the Author

[Nick A. Bild, MS](https://nickbild79.firebaseapp.com/#!/)
