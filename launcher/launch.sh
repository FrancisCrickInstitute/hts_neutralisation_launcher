#!/bin/bash

# Launch all necessary programs for neutralisation analysis in a tmux server

SESSION="ne"
MAMBA_ENV="dev-hts-neut"

echo "Killing old sessions and Redis server..."
tmux kill-session -t $SESSION &>/dev/null || true
redis-cli shutdown &>/dev/null || pkill redis-server

echo "Starting Redis server..."
redis-server --daemonize yes

echo "Creating new TMUX session: $SESSION"
tmux new-session -s $SESSION -d

# Function to create a new TMUX window with mamba environment activated
create_window() {
    local name=$1
    local command=$2
    local sleep_time=${3:-3}
    echo "Starting $name..."
    tmux new-window -t $SESSION -n "$name"
    tmux send-keys -t $SESSION "source /opt/homebrew/Caskroom/miniforge/base/bin/activate $MAMBA_ENV && export PYTHONPATH="$(pwd)" && $command" C-m
    sleep $sleep_time
}

# Start Celery workers and Flower
create_window "celery-analysis" \
    "celery -A launcher.task worker -Q analysis --concurrency=1 --loglevel=INFO -E -n analysis"

create_window "celery-stitching" \
    "celery -A launcher.task worker -Q image_stitch --concurrency=3 --loglevel=INFO -E -n image_stitcher"

create_window "celery-titration" \
    "celery -A launcher.task worker -Q titration --concurrency=1 --loglevel=INFO -E -n titration"

create_window "celery-titration-stitching" \
    "celery -A launcher.task worker -Q image_stitch_titration --concurrency=3 --loglevel=INFO -E -n image_stitcher_titration"

create_window "flower" \
    "celery -A launcher.task --broker=redis://localhost flower --address=0.0.0.0 --port=5555 --basic_auth=hts:1010"

echo "All tasks started"
# tmux attach-session -t $SESSION
