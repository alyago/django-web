#!/bin/bash

SERPNG_ROOT=$(git rev-parse --show-toplevel)

# Run JavaScript unit tests with PhantomJS.
JS_DIR="$SERPNG_ROOT/code/serpng/jobs/static/jobs/js"
JS_TESTS_DIR="$JS_DIR/sh"
JS_TESTS=$(ls $JS_TESTS_DIR/*_test.html 2>/dev/null)
SERPNG_TOOLS_DIR="$SERPNG_ROOT/code/serpng/tools/bin"

if [ -z "$JS_TESTS" ]; then
  echo "There are no JavaScript tests in the test directory."
  exit 1
fi

for js_test in $JS_TESTS; do
  $SERPNG_TOOLS_DIR/phantomjs $JS_DIR/test/runner.js $js_test
  if [ $? != 0 ]; then
    exit 1 
  fi
done
