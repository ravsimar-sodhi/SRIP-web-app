pkill mongod
sudo mongod &
pkill gunicorn
./prod_gunicorn.bash
service apache2 restart
