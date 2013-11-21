#!/bin/bash

# Use this script to make a Git tag and push it to the remote repository.
# This script also updates the DEPLOY_TAG configuration setting in Django.

if [ $# -gt 0 ]; then
    git_dir=$(git rev-parse --show-toplevel)

    # 1. Replace tag name in "code/serpng/config/default_configs.py" with tag given on command line
    tag_name=$1
    eval "sed -i 's|^DEPLOY_TAG\s*=.*|DEPLOY_TAG = \"${tag_name}\"|' ${git_dir}/code/serpng/config/default_configs.py"

    # 2. Commit the change.
    eval "git commit -m 'Updated DEPLOY_TAG for tagging' -n ${git_dir}/code/serpng/config/default_configs.py"

    # 3. Make git tag
    eval "git tag -a ${tag_name}"

    # 4. Push tag to remote Git repo
    eval "git push --tags"

    # 5. Change tag back to 'dev'
    tag_name="dev"
    eval "sed -i 's|^DEPLOY_TAG\s*=.*|DEPLOY_TAG = \"${tag_name}\"|' ${git_dir}/code/serpng/config/default_configs.py"

    # 6. Commit the change.
    eval "git commit -m 'Reverted DEPLOY_TAG back to dev' -n ${git_dir}/code/serpng/config/default_configs.py"
    eval "git push origin HEAD"
  
else
    echo "Please provide a tag name!"
    echo "Usage: tag.sh <tag_name>"
fi
