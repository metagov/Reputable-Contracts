#!/bin/bash

while true; do
    # Run the first Python script
    python3 ./Attest/3_getMemberAttestationURI.py

    # Wait for 5 minutes
    sleep 300  # 300 seconds = 5 minutes

    # Run the second Python script
    python3 ./Attest/4_attestationSsd.py

    # Wait for 5 minutes before the next iteration
    sleep 300
done
