# Use a imagem oficial do Apache
FROM httpd:latest

# Copie o arquivo de configuração personalizado para o diretório de configuração do Apache
RUN sed -i 's/^#LoadModule mpm_event_module/LoadModule mpm_event_module/' /usr/local/apache2/conf/httpd.conf

COPY ./app/ /usr/local/apache2/htdocs/

RUN echo "ProxyPass /ws ws://localhost:5000/" >> /usr/local/apache2/conf/httpd.conf
RUN echo "ProxyPassReverse /ws ws://localhost:5000/" >> /usr/local/apache2/conf/httpd.conf

# Configurações do Apache para reconhecer o nome de host
RUN echo "ServerName www.trabalhofinalfrc.com" >> /usr/local/apache2/conf/httpd.conf

# Exponha a porta 80
EXPOSE 80
