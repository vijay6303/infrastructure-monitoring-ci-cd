#!/bin/bash

# System Health Monitoring Script

echo "=================================="
echo "       SYSTEM HEALTH REPORT"
echo "=================================="

echo ""
echo "Hostname:"
hostname

echo ""
echo "Current Date:"
date

echo ""
echo "CPU Load:"
uptime

echo ""
echo "Memory Usage:"
free -h

echo ""
echo "Disk Usage:"
df -h /

echo ""
echo "Top 5 Memory Consuming Processes:"
ps aux --sort=-%mem | head -n 6

echo ""
echo "System Health Check Completed"
