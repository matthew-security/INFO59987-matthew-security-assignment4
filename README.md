# Assignment 4: Container Security with SecComp Profiles

INFO59987 Containerization

Custom seccomp profiles for the three APIs from Assignment 2 (books-api, staff-api, readers-api), plus a test script and a stress test. Screenshots and explanations are in the PDF.

## Files

- seccomp-profiles/ has the profile for each API and the handout's template.json
- docker-compose.yml is the Assignment 2 file with security_opt added to the three APIs
- validate_seccomp.sh is the test script
- stress_test.py is the stress test
- make_profile.py builds the profiles
- *-syscalls.txt is what strace found for each API

## Running it

    cp .env.example .env
    docker compose up -d --build
    ./validate_seccomp.sh
    python3 stress_test.py

The stress test needs the requests library.
