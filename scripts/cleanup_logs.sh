#!/bin/bash

# Log Cleanup Automation

set -euo pipefail

LOG_DIR="${1:-monitoring/logs}"
DAYS="${2:-7}"
MODE="${3:---dry-run}"

echo "=================================="
echo "         LOG CLEANUP"
echo "=================================="

# Validate directory
if [ ! -d "$LOG_DIR" ]; then
    echo "Error: Directory does not exist: $LOG_DIR"
    exit 1
fi

# Validate number of days
if ! [[ "$DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: DAYS must be a non-negative integer."
    exit 1
fi

if [[ "$MODE" != "--dry-run" && "$MODE" != "--delete" ]]; then
    echo "Usage: $0 [log_directory] [days] [--dry-run|--delete]"
    exit 1
fi

echo "Directory: $LOG_DIR"
echo "Retention: $DAYS days"
echo "Mode: $MODE"

if [ "$MODE" = "--dry-run" ]; then
    echo ""
    echo "Preview: Files that would be deleted:"
    find "$LOG_DIR" -type f -name "*.log" -mtime +"$DAYS" -print

    echo ""
    echo "Dry run completed. No files were deleted."
else
    echo ""
    echo "Deleting old log files..."

    find "$LOG_DIR" -type f -name "*.log" -mtime +"$DAYS" -print -delete

    echo "Cleanup completed."
fi
