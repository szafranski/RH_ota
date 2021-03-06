#!/bin/bash

sudo cp /etc/rc.local /etc/rc.local.iptables_saved

sudo sed -i 's/exit 0//' /etc/rc.local

sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables-save

echo "
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables-save
exit 0
" | sudo tee -a /etc/rc.local

echo "
port forwarding added - server available on default port 80
no need to type server port number in a browser address bar
just type RotorHazard server IP address (probably: $(hostname -I | awk '{ print $1 }'))"