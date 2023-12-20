# Use a imagem oficial do Apache
FROM httpd:latest

# Copie o arquivo de configuração personalizado para o diretório de configuração do Apache
RUN sed -i 's/^#LoadModule mpm_event_module/LoadModule mpm_event_module/' /usr/local/apache2/conf/httpd.conf

COPY ./app/ /usr/local/apache2/htdocs/

# Exponha a porta 80
EXPOSE 80
