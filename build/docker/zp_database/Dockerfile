# Create database to zabbix control with MySQL 5.7
#

FROM "mysql:5.7"

LABEL maintainer="Michel Peterson \
      <michel.peterson@l1nuxc0d3.com>"

LABEL description="This container run the \
	database to zabbix patrol \
	python application that \
	looking for issues triggered in zabbix."

#
# Copy zp database scheme
#

COPY ./sourceconf/db/zpdb.sql /docker-entrypoint-initdb.d/

#
# Set timezone
# 

RUN ln -sfv /usr/share/zoneinfo/America/Bahia /etc/localtime && \
    apt-get update --allow-insecure-repositories && apt-get -y --allow-unauthenticated install apt-utils locales && \
    apt-get clean && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

#
# Set the locale
#

ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US.UTF-8 
ENV LC_ALL en_US.UTF-8  

#
# Create database persistent data
#

VOLUME /var/lib/mysql

#
# Port to expose outside from container
#

EXPOSE 3306/tcp
