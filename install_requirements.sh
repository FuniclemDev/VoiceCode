pip install SpeechRecognition pyttsx3
sudo dnf install alsa-utils jack-audio-connection-kit pulseaudio-utils pulseaudio espeak
echo "autospawn = no" > ~/.config/pulse/client.conf
pulseaudio --kill
pulseaudio --start
