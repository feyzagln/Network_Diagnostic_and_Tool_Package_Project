import socket
import subprocess

def machine_info():
    # Hostname'i doğrudan socket kütüphanesi ile aldım
    hostname = socket.gethostname()
    print(f"Hostname: {hostname}\n")

    print("--- Ağ Arayüzleri ve IP Adresleri ---")

    # Ağ arayüzleri için subprocess kullandım
    ip_sorgu = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
    
    # Çıktıyı satır satır okuyarak ayrıştırıyoruz ve ip kısmını buluyrozu
    for satir in ip_sorgu.stdout.splitlines():
        satir = satir.strip()
        
        # Arayüz ismini yakalama
        if satir and satir[0].isdigit() and ":" in satir:
            parcalar = satir.split(":")
            if len(parcalar) >= 2:
                print(f"Arayüz: {parcalar[1].strip()}")
        
        # IPv4 adreslerini yakalama
        elif satir.startswith("inet "):
            ip_adresi = satir.split()[1].split('/')[0]
            print(f"  IPv4 Adresi: {ip_adresi}")
            
        # IPv6 adreslerini yakalama
        elif satir.startswith("inet6 "):
            ipv6_adresi = satir.split()[1].split('/')[0]
            print(f"  IPv6 Adresi: {ipv6_adresi}")
            
if __name__ == "__main__":
    machine_info()
