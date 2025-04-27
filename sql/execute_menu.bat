@echo off
mysql -h127.0.0.1 -uroot -pq1w2e3r4 --default-character-set=utf8mb4 hcare-final -e "source add_medical_menu.sql"
pause