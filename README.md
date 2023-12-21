## Projeto de pesquisa - servidor de diálogos usando camada de aplicação

Repositório destinado a matéria de Fundamentos de Redes de Computadores da Universidade de Brasília (2023-2). 

O contexto do projeto envolve a criação e implementacão de um servidor de comunicação destinado a diversos clientes, utilizando o modelo cliente/servidor.

## Integrantes
| Nome                            | Matrícula      |
|---------------------------------|----------------|
| Artur de Sousa Vieira           | 19/0010606     |
| Carlos Eduardo Miranda Roriz    | 19/0011424     |
| Débora Caires de S. Moreira     | 22/2015103     |
| João Victor Teixeira Batista    | 19/0109963     |
| Laura Pinos de Oliveira         | 19/0090901     |

## Como rodar o projeto
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
