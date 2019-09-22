接收外来连接命令
sudo iptables -A INPUT -p tcp --dport 5006 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 5005 -j ACCEPT

sudo iptables -A INPUT -p udp --dport 5678 -j ACCEPT

sudo iptables -A INPUT -p udp --dport 5006 -j ACCEPT