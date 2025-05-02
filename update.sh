#!/bin/bash

# Get the directory where the script is being executed from
CWD="$(pwd)"

# Check if a commit message is provided
if [ -z "$1" ]; then
    echo "Error: Please provide a commit message as the first argument."
    echo "Usage: ./gitpush.sh \"Your commit message\""
    exit 1
fi

commit_message="$*"

# Git operations (using -C to specify the working directory)
git -C "$CWD" add .
git -C "$CWD" commit -m "$commit_message"
git -C "$CWD" push