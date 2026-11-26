#!/bin/bash

# Test script for validating SecComp profiles
TEST_CONTAINERS=("books-api" "staff-api" "readers-api")

for container in "${TEST_CONTAINERS[@]}"; do
    echo "Testing $container..."
    route=${container%-api}   # books-api -> books (matches the Nginx routes)

    # Test 1: Verify container starts with profile (and is still running after 5s)
    docker compose up -d $container
    sleep 5
    if docker compose ps --status running --services | grep -qx "$container"; then
        echo "✓ Container starts successfully with SecComp profile"
    else
        echo "✗ Container failed to start with SecComp profile"
    fi

    # Test 2: Verify API functionality (through Nginx)
    curl -sf http://localhost/api/$route > /dev/null
    if [ $? -eq 0 ]; then
        echo "✓ API endpoints functioning correctly"
    else
        echo "✗ API endpoints not responding"
    fi

    # Test 3: Verify blocked syscalls (unshare)
    docker compose exec $container unshare 2>&1 | grep -q "Operation not permitted"
    if [ $? -eq 0 ]; then
        echo "✓ Unauthorized syscalls properly blocked (unshare)"
    else
        echo "✗ Unauthorized syscalls not blocked (unshare)"
    fi

    # Test 4: Blocked by our profile but allowed by Docker's default (setpriority)
    docker compose exec $container python -c "import os; os.nice(1)" 2>&1 | grep -q "Operation not permitted"
    if [ $? -eq 0 ]; then
        echo "✓ Custom profile blocks setpriority (Docker's default allows it)"
    else
        echo "✗ setpriority not blocked"
    fi
    echo
done
