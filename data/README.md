# IoT Cybersecurity Dataset - Feature Descriptions

## Overview
This document provides an overview of the extracted features from the **IoT Cybersecurity Dataset**. The dataset includes various network traffic indicators that help analyze and detect cyber threats in IoT environments.

## Extracted Features

| #  | Feature             | Description |
|----|---------------------|-------------|
| 1  | **Header Length**   | Mean of the header lengths of the transport layer |
| 2  | **Time-To-Live**    | Time-To-Live (TTL) value of packets |
| 3  | **Rate**            | Speed of packet transmission within a window (packets/sec) |
| 4  | **fin flag number** | Proportion of packets with FIN flags in the window |
| 5  | **syn flag number** | Proportion of packets with SYN flags in the window |
| 6  | **rst flag number** | Proportion of packets with RST flags in the window |
| 7  | **psh flag number** | Proportion of packets with PSH flags in the window |
| 8  | **ack flag number** | Proportion of packets with ACK flags in the window |
| 9  | **ece flag number** | Proportion of packets with ECE flags in the window |
| 10 | **cwr flag number** | Proportion of packets with CWR flags in the window |
| 11 | **syn count**       | Count of SYN flag occurrences in packets |
| 12 | **ack count**       | Count of ACK flag occurrences in packets |
| 13 | **fin count**       | Count of FIN flag occurrences in packets |
| 14 | **rst count**       | Count of RST flag occurrences in packets |
| 15 | **IGMP**            | Average number of IGMP packets in the window |
| 16 | **HTTPS**           | Average number of HTTPS packets in the window |
| 17 | **HTTP**            | Average number of HTTP packets in the window |
| 18 | **Telnet**          | Average number of Telnet packets in the window |
| 19 | **DNS**             | Average number of DNS packets in the window |
| 20 | **SMTP**            | Average number of SMTP packets in the window |
| 21 | **SSH**             | Average number of SSH packets in the window |
| 22 | **IRC**             | Average number of IRC packets in the window |
| 23 | **TCP**             | Average number of TCP packets in the window |
| 24 | **UDP**             | Average number of UDP packets in the window |
| 25 | **DHCP**            | Average number of DHCP packets in the window |
| 26 | **ARP**             | Average number of ARP packets in the window |
| 27 | **ICMP**            | Average number of ICMP packets in the window |
| 28 | **IPv**             | Average number of IPv packets in the window |
| 29 | **LLC**             | Average number of LLC packets in the window |
| 30 | **Tot Sum**         | Total packet length within the aggregated packets (window) |
| 31 | **Min**             | Shortest packet length within the aggregated packets (window) |
| 32 | **Max**             | Longest packet length within the aggregated packets (window) |
| 33 | **AVG**             | Mean of the packet length within the aggregated packets (window) |
| 34 | **Std**             | Standard deviation of the packet length within the aggregated packets (window) |
| 35 | **Tot Size**        | (AVG.) Length of the Packet |
| 36 | **IAT**             | Interval mean between the current and previous packet in the window |
| 37 | **Number**          | Total number of packets in the window |
| 38 | **Variance**        | Variance of the packet lengths in the window |
| 39 | **Protocol Type**   | Mode of protocols found in the window |
