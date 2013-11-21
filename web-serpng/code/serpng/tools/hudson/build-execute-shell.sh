#!/bin/bash

export PIP_MIRROR_ARGS='-i http://pypi.ksjc.sh.colo/simple -M'
#TODO: Restore 95 column limit once we get our lint under control.
#export MAX_LINE_LENGTH=95
export MAX_LINE_LENGTH=400

git clean -fdxq

echo ========================================================================
echo
echo Setting up virtualenvwrapper
echo
echo ========================================================================
export PIP_REQUIRE_VIRTUALENV=true
export PIP_RESPECT_VIRTUALENV=true
export WORKON_HOME="${WORKSPACE}/virtualenv" 
export VIRTUALENV_USE_DISTRIBUTE=true
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
source /usr/bin/virtualenvwrapper.sh

echo ========================================================================
echo
echo Creating virtualenv containing dependencies from virtualenv-reqs.txt
echo
echo ========================================================================
mkvirtualenv "${BUILD_TAG}"
pip install ${PIP_MIRROR_ARGS} -r configs/production/virtualenv-reqs.txt
pip freeze

echo ========================================================================
echo
echo Running pep8
echo
echo ========================================================================
pip install ${PIP_MIRROR_ARGS} pep8
pep8 --exclude=models.py --exclude=Cookie.py --max-line-length=${MAX_LINE_LENGTH} --format=pylint "${WORKSPACE}/code" | sed "s/^${WORKSPACE//\//\\/}\/code\/\(.\+\?:[[:digit:]]\+:\) \([^ ]\+\) \(.\+\)/\1 [\2] \3/" | tee "${WORKSPACE}/violations-pep8.txt"

echo ========================================================================
echo
echo Running pylint
echo
echo ========================================================================
pip install ${PIP_MIRROR_ARGS} pylint
pushd "${WORKSPACE}/code"
pylint --ignore=models.py --disable-msg=W0142,W0403,R0201,W0212,W0613,W0232,R0903,W0614,C0103,C0301,R0913,F0401,W0402,R0914 --max-returns=10 --max-statements=100 --min-public-methods=1 --max-line-length=${MAX_LINE_LENGTH} --generated-members=objects -f parseable -i y serpng -r n | sed 's/C0111/F/' | tee "${WORKSPACE}/violations-pylint.txt"
popd

#echo ========================================================================
#echo
#echo Running pyflakes
#echo
#echo ========================================================================
#pip install ${PIP_MIRROR_ARGS} pyflakes
#pyflakes "${WORKSPACE}/code" | sed "s/^${WORKSPACE//\//\\/}\/code\/\(.\+\?:[[:digit:]]\+:\) \(.\+\)/\1 [E] \2/" | tee "${WORKSPACE}/violations-pyflakes.txt"

#echo ========================================================================
#echo
#echo Running pydoctor
#echo
#echo ========================================================================
#pip install ${PIP_MIRROR_ARGS} pydoctor
#pip install ${PIP_MIRROR_ARGS} Twisted
#pip install ${PIP_MIRROR_ARGS} nevow
#pydoctor ${WORKSPACE}/code/serpng | cat

echo ========================================================================
echo
echo Running unit tests
echo
echo ========================================================================
pip install ${PIP_MIRROR_ARGS} django-jux
pip install ${PIP_MIRROR_ARGS} coverage
pip install ${PIP_MIRROR_ARGS} mock
pip install ${PIP_MIRROR_ARGS} beautifulsoup4
pip install ${PIP_MIRROR_ARGS} html5lib
coverage run --branch --source="${WORKSPACE}/code/serpng" "${WORKSPACE}/code/serpng/manage.py" test --settings=test_settings -v2 --noinput jobs
coverage report
coverage xml -o "${WORKSPACE}/coverage.xml"

echo ========================================================================
echo
echo Running JavaScript unit tests
echo
echo ========================================================================
$WORKSPACE/code/serpng/tools/testing/phantomjs-runner.sh | cat

echo ========================================================================
echo
echo Running web integration tests
echo
echo ========================================================================
$WORKSPACE/code/serpng/tools/testing/casperjs-runner.sh | cat

#echo ========================================================================
#echo
#echo Running selenium tests
#echo
#echo ========================================================================
#pip install ${PIP_MIRROR_ARGS} selenium
#python "${WORKSPACE}/code/serpng/tools/selenium-test/selenium_test.py"

echo ========================================================================
echo
echo Deleting virtualenv
echo
echo ========================================================================
deactivate
rmvirtualenv "${BUILD_TAG}"
