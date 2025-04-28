#!/bin/bash

# Check if a commit message is provided
if [ -z "$1" ]; then
    echo "Error: Please provide a commit message as the first argument."
    echo "Usage: ./gitpush.sh \"Your commit message\""
    exit 1
fi

commit_message="$*"

# Git operations
git add .
git commit -m "$commit_message"
git push