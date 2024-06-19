#!/bin/bash

# Check if an argument was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_audio_file>"
    exit 1
fi

# Get the duration of the audio file in seconds using ffprobe
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$1")

# Calculate the cost (rate is $0.00010 per second)
COST=$(echo "$DURATION * 0.00010" | bc -l)

# Print the cost formatted to two decimal places
printf "The cost of processing is: $%.2f\n" $COST

