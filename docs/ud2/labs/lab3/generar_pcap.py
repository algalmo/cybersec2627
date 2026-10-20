from scapy.all import Ether, IP, TCP, UDP, ICMP, DNS, DNSQR, wrpcap

# Tráfico de laboratorio: un saludo TCP, una consulta DNS, un ping,
# y una IP que toca varios puertos (patrón de escaneo).
paquetes = [
    Ether()/IP(src="10.0.0.5", dst="10.0.0.1")/TCP(sport=44321, dport=80, flags="S"),
    Ether()/IP(src="10.0.0.1", dst="10.0.0.5")/TCP(sport=80, dport=44321, flags="SA"),
    Ether()/IP(src="10.0.0.5", dst="10.0.0.1")/TCP(sport=44321, dport=80, flags="A"),
    Ether()/IP(src="10.0.0.5", dst="8.8.8.8")/UDP(sport=5353, dport=53)/DNS(rd=1, qd=DNSQR(qname="ejemplo.local")),
    Ether()/IP(src="10.0.0.9", dst="10.0.0.1")/ICMP(),
    Ether()/IP(src="10.0.0.9", dst="10.0.0.1")/TCP(sport=51000, dport=22, flags="S"),
    Ether()/IP(src="10.0.0.9", dst="10.0.0.1")/TCP(sport=51001, dport=23, flags="S"),
    Ether()/IP(src="10.0.0.9", dst="10.0.0.1")/TCP(sport=51002, dport=445, flags="S"),
]
wrpcap("trafico.pcap", paquetes)
print(f"Creado trafico.pcap con {len(paquetes)} paquetes")
