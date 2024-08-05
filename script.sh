#!/bin/bash

# ��������� ����� 22 � 443
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# ��������� ������������� ���������� � ICMP ������
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

# ��������� ��� ��������� �������� ����������
iptables -A INPUT -j DROP

# ��������� SSH-�������
exec /usr/sbin/sshd -D
