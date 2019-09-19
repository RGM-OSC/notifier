#!/bin/bash
##
## License: GPL
## Copyleft 2013 Vincent Fricou (vincent@fricouv.eu)
##
##
## Notifier (2.1.3) database creation script.
##

SERVER=127.0.0.1
PORT=3306
DATABASE="notifier"
MYSQL_NOTIFIERUSER="notifierSQL"
MYSQL_NOTIFIERPASSWORD="Notifier66"
DATABASE_STRUCT="/usr/share/doc/notifier/sql/notifier.sql"

mysql -h${SERVER} -P${PORT} -e "CREATE DATABASE notifier;"
mysql -h${SERVER} -P${PORT} -D ${DATABASE} < ${DATABASE_STRUCT}
mysql -h${SERVER} -P${PORT} -e "GRANT ALL PRIVILEGES ON notifier.* TO '${MYSQL_NOTIFIERUSER}'@'localhost' IDENTIFIED BY '${MYSQL_NOTIFIERPASSWORD}';"
