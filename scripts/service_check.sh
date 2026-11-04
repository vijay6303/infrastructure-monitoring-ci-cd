#!/bin/bash

# Linux Service Health Checker

echo "=================================="
echo "       SERVICE HEALTH CHECK"
echo "=================================="

# Use supplied service names, or check SSH by default
if [ "$#" -eq 0 ]; then
    services=("ssh")
else
    services=("$@")
fi

failed=0

for service in "${services[@]}"
do
    echo ""
    echo "Checking service: $service"

    if systemctl is-active --quiet "$service"; then
        echo "Status: RUNNING"
    else
        echo "Status: NOT RUNNING"
        failed=1
    fi
done

echo ""
echo "=================================="

if [ "$failed" -eq 0 ]; then
    echo "All checked services are running."
else
    echo "One or more services need attention."
fi

exit "$failed"
