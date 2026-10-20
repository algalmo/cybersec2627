from scapy.all import rdpcap, IP, TCP, UDP, ICMP, DNS
from collections import Counter

def analizar(ruta: str) -> None:
    paquetes = rdpcap(ruta)
    print(f"Paquetes leídos: {len(paquetes)}\n")

    protocolos: Counter[str] = Counter()
    conversaciones: Counter[tuple[str, str]] = Counter()
    puertos_tcp: Counter[int] = Counter()
    consultas_dns: list[str] = []

    for p in paquetes:
        if p.haslayer(TCP):
            protocolos["TCP"] += 1
            puertos_tcp[p[TCP].dport] += 1
        elif p.haslayer(UDP):
            protocolos["UDP"] += 1
        elif p.haslayer(ICMP):
            protocolos["ICMP"] += 1
        if p.haslayer(IP):
            conversaciones[(p[IP].src, p[IP].dst)] += 1
        if p.haslayer(DNS) and p[DNS].qd is not None:
            consultas_dns.append(p[DNS].qd.qname.decode())

    print("Protocolos:", dict(protocolos))
    print("\nConversaciones (origen -> destino):")
    for (src, dst), n in conversaciones.most_common():
        print(f"  {src:12} -> {dst:12}  {n}")
    print("\nPuertos destino TCP más contactados:")
    for puerto, n in puertos_tcp.most_common(5):
        print(f"  puerto {puerto:5}  {n} intento(s)")
    print("\nConsultas DNS:")
    for q in consultas_dns:
        print(f"  {q}")

if __name__ == "__main__":
    analizar("trafico.pcap")
