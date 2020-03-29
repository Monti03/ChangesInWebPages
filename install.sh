#!/usr/bin/env bash

if [[ -z $(which sed) ]] ; then
	echo "Please install sed before installing"
	exit 1
fi

current_dir=$(pwd)

# link commands to be available with PATH
sudo ln -s "${current_dir}"/cwp_cli.py /usr/local/bin/cwp-cli
sudo ln -s "${current_dir}"/cwpd.py /usr/local/bin/cwpd
sudo ln -s "${current_dir}"/gui.py /usr/local/bin/cwp

# install dependencies
pip install --user -r requirements.txt

# activate and launch user service
sed -i "s|__CWPD_LOC__|${current_dir}|" service/cwpd.service
systemctl enable --user "${current_dir}"/service/cwpd.service
systemctl start --user cwpd.service

