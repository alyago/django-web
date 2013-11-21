#!/bin/bash

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERPNG_ROOT=`git rev-parse --show-toplevel`

VIRTUALENV_NAME=serpng
VIRTUALENV_REQ_PATH="$SERPNG_ROOT/configs/production/virtualenv-reqs.txt"
VIRTUALENV_REQ_DEV_PATH="$SCRIPT_PATH/virtualenv-reqs-dev.txt"

BUNDLE_GEMFILE="$SERPNG_ROOT/configs/production/Gemfile"
RUBY_VERSION=`cat $SERPNG_ROOT/configs/production/RUBY_VERSION`
RVM_COMMAND=/usr/local/rvm/bin/rvm

echo ===
echo === Initializing shared git submodules...
echo ===
pushd $SERPNG_ROOT > /dev/null
git submodule init
git submodule update
popd > /dev/null

echo ""
echo ===
echo === Setting up git hooks
echo ===
rm -rf $SERPNG_ROOT/.git/hooks
ln -s ../githooks/ $SERPNG_ROOT/.git/hooks

echo ""
echo ===
echo === Creating virtualenv $VIRTUALENV_NAME...
echo ===
source /usr/bin/virtualenvwrapper.sh
deactivate

mkvirtualenv $VIRTUALENV_NAME
if [ $? != 0 ]; then
  echo " - error running mkvirtualenv"
  exit
fi

workon $VIRTUALENV_NAME
if [ $? != 0 ]; then
  echo " - error running workon"
  exit
fi

echo ""
echo ===
echo === Installing required Python modules...
echo ===
pip install -r $VIRTUALENV_REQ_PATH -r $VIRTUALENV_REQ_DEV_PATH

echo ""
echo ===
echo === Installing ruby $RUBY_VERSION and required gems...
echo ===
source $($RVM_COMMAND $RUBY_VERSION do $RVM_COMMAND env --path)
if [ $? != 0 ]; then
  # Ruby version not found, attempt to install it.
  $RVM_COMMAND install $RUBY_VERSION
  source $($RVM_COMMAND $RUBY_VERSION do $RVM_COMMAND env --path)
  if [ $? != 0 ]; then
    echo "FATAL: Couldn't install ruby $RUBY_VERSION using rvm."  
    exit
  fi
fi
export BUNDLE_GEMFILE
bundle install

echo ""
echo ===
echo === Checking if /etc/hosts file has an entry for ip1...
echo ===
grep "^[^#]* ip1" /etc/hosts 1> /dev/null 2>&1
if [ $? != 0 ]; then

  INPUT_SUCCESS=0
  until [ $INPUT_SUCCESS == 1 ]; do
    read -p "No entry found. Please enter the IP address of the machine hosting the PHP Platform code: " BRIDGE_IP
    echo $BRIDGE_IP | grep "^[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}$" 1> /dev/null
    if [ $? == 0 ]; then
      INPUT_SUCCESS=1
    else
      echo " - the IP address you entered was invalid! Please enter it again."
    fi
  done

  echo === Updating /etc/hosts file...
  sudo sed -i "$ a\\$BRIDGE_IP ip1" /etc/hosts
else
  echo " - an entry for ip1 already exists in /etc/hosts; please ensure that ip1 points to the machine hosting PHP platform code."
fi

echo Done!
