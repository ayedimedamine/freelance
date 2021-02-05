docker run --name mariadb --restart unless-stopped -v mariadb_db:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3307:3306 mariadb
