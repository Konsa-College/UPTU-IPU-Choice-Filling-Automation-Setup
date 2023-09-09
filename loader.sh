#!/bin/bash

# Function to show a cute loading animation
function show_loading() {
    local spin='-\|/'
    local i=0
    while true; do
        i=$(( (i+1) % 4 ))
        printf "\r[%c] Loading..." "${spin:$i:1}"
        sleep 0.1
    done
}

# Start the loading animation in the background
show_loading &

# Sleep for a few seconds (simulating some task)
sleep 5

# Stop the loading animation (kill the background process)
kill $!

# Display a message
printf "\r[✓] Task completed.     \n"
