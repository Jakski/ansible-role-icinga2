#!/usr/bin/env bash
################################################################################
# Link Ansible Mitogen plugin
################################################################################

set -o errexit
set -o nounset

plugins_dir="${MOLECULE_SCENARIO_DIRECTORY}/plugins"
mitogen_path=$(python -c 'import os, ansible_mitogen;print(os.path.dirname(ansible_mitogen.__file__))')
[ ! -d "$plugins_dir" ] && mkdir "$plugins_dir"
ln -sf "${mitogen_path}/plugins/strategy" "${plugins_dir}/strategy"
