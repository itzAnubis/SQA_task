#!/bin/bash
# Run tests with clean PYTHONPATH to avoid ROS plugin conflicts
PYTHONPATH="" uv run pytest "$@"
