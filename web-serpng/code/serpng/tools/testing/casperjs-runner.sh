#!/bin/bash

SERPNG_ROOT=$(git rev-parse --show-toplevel)

# Run headless integration tests with CasperJS.
HEADLESS_TESTS_DIR="$SERPNG_ROOT/code/serpng/jobs/static/jobs/js/headless_tests"
HEADLESS_TESTS=$(ls $HEADLESS_TESTS_DIR/*.js 2>/dev/null)
CASPER_DIR="$SERPNG_ROOT/code/serpng/tools/casper/bin"

# Add tools/bin to path.
PATH=$PATH:$SERPNG_ROOT/code/serpng/tools/bin

if [ -z "$HEADLESS_TESTS" ]; then
  echo "There are no headless integration tests in the test directory."
  exit 1
fi

for headless_test in $HEADLESS_TESTS; do
  $CASPER_DIR/casperjs test $headless_test
  if [ $? != 0 ]; then
    exit 1 
  fi
done
