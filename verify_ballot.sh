#!/bin/bash
# OPSEC-focused ballot verification via w3m
TARGET_URL="https://pavoterservices.pa.gov"
w3m -dump "$TARGET_URL" | tac | head -n 50
