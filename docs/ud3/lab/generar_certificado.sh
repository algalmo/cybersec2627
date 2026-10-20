#!/bin/sh
# Genera un certificado autofirmado de laboratorio para Nginx.
# NO usar en producción: un certificado autofirmado solo vale para pruebas.
mkdir -p nginx/certs
openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout nginx/certs/key.pem \
    -out nginx/certs/cert.pem \
    -days 365 \
    -subj "/CN=intranet.local"
echo "Certificado creado en nginx/certs/"
