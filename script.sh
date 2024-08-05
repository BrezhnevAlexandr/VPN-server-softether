#!/bin/bash

# Открываем порты 22 и 443
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Разрешаем установленные соединения и ICMP пакеты
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

# Блокируем все остальные входящие соединения
iptables -A INPUT -j DROP

# Запускаем SSH-сервера
exec /usr/sbin/sshd -D
