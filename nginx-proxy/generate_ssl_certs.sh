sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d 7wik-pk.online -d iteration1.7wik-pk.online

# # To renew the certificates automatically, add a cron job by running:
# sudo crontab -e
# # Add the following line to the crontab file to run the renewal twice daily
# 0 0 * * * certbot renew --quiet && docker restart safetrek-proxy

