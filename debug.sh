echo "autospawn = no" > ~/.config/pulse/client.conf
pulseaudio --kill
pulseaudio --start
