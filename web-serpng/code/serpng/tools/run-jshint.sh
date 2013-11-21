#!/bin/env /bin/bash

# Enable extended bash globbing
#
shopt -s extglob

GIT_ROOT=$(git rev-parse --show-toplevel)

# Add node and npm to the front of the path.
#
PATH=$GIT_ROOT/code/serpng/tools/node-v0.8.12-linux-x64/bin:$PATH

if [ "$1" == "--all" ]; then

  # Enumerate all eligible .js files in the tree
  #
  JSFILES=$(find $GIT_ROOT/code/serpng/!(static-root|external|tools) \
      ! -name *.min.js \
      ! -name *-min.js \
      ! -name backbone.js \
      ! -name backbone*.js \
      ! -name bootstrap*.js \
      ! -name jquery*.js \
      ! -name json2.js \
      ! -name qunit*.js \
      ! -name sinon*.js \
      ! -name underscore.js \
      ! -name zepto.js \
      -name *.js \
      | sort)
else

  # By default, we only look for .js files in the index.
  #
  JSFILES=$(git diff-index --name-only HEAD | grep \.js$ | xargs -I@ echo $GIT_ROOT/@)
fi

# Execute JSHint against each of the files.
#
ERRORSTATUS=0
for i in $JSFILES; do
    jshint $i
    if [ $? != 0 ]; then
      ERRORSTATUS=1
    fi
done

exit $ERRORSTATUS
