1. place .service files in /lib/systemd/system
2. sudo systemctl daemon-reload
3. sudo systemctl enable sample.service

If the service file is changed, the following has to be run:
1. sudo systemctl daemon-reload
2. sudo systemctl reload sample.service
