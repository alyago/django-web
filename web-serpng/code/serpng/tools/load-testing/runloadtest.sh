#!/bin/bash

python loadtest.py | awk '/^[0-9]/ { print $0; if (NR == 1) { first=$1 }; last = $1; response_time += $5; count++; } END { print count/(last-first), "rps"; print response_time/count, "avg response time"  }'

