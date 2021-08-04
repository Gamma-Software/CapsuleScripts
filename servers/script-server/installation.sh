#!/bin/bash
virtualenv .venv

.venv/bin/python3 -m pip install -r requirements.txt

ln -s $(pwd)/script_server.service /lib/systemd/system/script_server.service

systemctl daemon-reload
systemctl enable script_server.service
systemctl start script_server.service