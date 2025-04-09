#!bin/bash

if [ -d "/home/frappe/frappe-bench/apps/frappe" ]; then
    echo "Bench already exists, skipping init"
    cd frappe-bench
    bench start
else
    echo "Creating new bench..."
fi

bench init --skip-redis-config-generation frappe-bench

cd frappe-bench

# Use containers instead of localhost
bench set-mariadb-host mariadb
bench set-redis-cache-host redis:6379
bench set-redis-queue-host redis:6379
bench set-redis-socketio-host redis:6379

# Remove redis, watch from Procfile
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

bench get-app teamplan

bench new-site teamplan.localhost \
    --force \
    --mariadb-root-password 123 \
    --admin-password admin \
    --no-mariadb-socket

bench --site teamplan.localhost install-app teamplan
bench --site teamplan.localhost set-config developer_mode 1
bench --site teamplan.localhost clear-cache
bench --site teamplan.localhost set-config mute_emails 1
bench --site teamplan.localhost add-user alex@example.com --first-name Alex --last-name Scott --password 123 --user-type 'System User' --add-role 'teamplan Admin'
bench use teamplan.localhost

bench start
