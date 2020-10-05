FROM php:7.4-fpm

RUN docker-php-ext-install mysqli

WORKDIR /app

COPY index.php connect.php ./
