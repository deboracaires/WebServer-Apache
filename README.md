Configurar DNS 

`sudo nano /etc/hosts`

adicionar a linha

`127.0.0.1 www.trabalhofinalfrc.com`

Ctrl+o Enter Ctrl+x

Configurar servidor apache

`sudo nano /etc/apache2/sites-available/frcfinal.conf`

dentro colocar com as alterações devidas para o caminho no seu pc

```
  <VirtualHost *:80>
    ServerName www.trabalhofinalfrc.com
    ProxyPass /socket.io http://localhost:5000/socket.io
    ProxyPassReverse /socket.io http://localhost:5000/socket.io
    ProxyPass / http://localhost:5000/
    ProxyPassReverse / http://localhost:5000/
    WSGIScriptAlias / /home/deboracaires/Documentos/facul/redes/trabalho_final/app.wsgi
    <Directory /home/deboracaires/Documentos/facul/redes/trabalho_final>
        WSGIProcessGroup app
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
```

Ctrl+o Enter Ctrl+x

sudo systemctl reload apache2

migrations

flask db init

flask db migrate -m "Initial migration"

flask db upgrade
