#!/bin/bash

echo "Killing old sessions and Redis server..."
tmux kill-session -t $SESSION &>/dev/null || true
redis-cli shutdown &>/dev/null || pkill redis-server
