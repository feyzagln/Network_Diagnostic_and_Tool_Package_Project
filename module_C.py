import socket
import struct
from datetime import datetime

def sntp_istegi_gonder(host, port):
    """
    Task 1: Send a request to an SNTP server.
    """
    # NTP (SNTP) paket formatı: Toplam 48 byte, sadece ilk byte 0x1b olarak ayarlı
    istek_paketi = b'\x1b' + 47 * b'\0'
    
    # UDP (SOCK_DGRAM) türünde bir soket oluştur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5.0) # Bağlantı donmasını engellemek için 5 saniye limit
    
    try:
        # Sunucuya NTP isteğini yolla
        client_socket.sendto(istek_paketi, (host, port))
        
        # Sunucudan gelen 48 bytelık yanıtı al
        gelen_veri, _ = client_socket.recvfrom(1024)
        return gelen_veri
    finally:
        client_socket.close()

def zamani_parse_et(gelen_veri):
    """
    Task 2: Parse the time from the response (processing raw data).
    """
    # NTP zamanı (1900) ile Unix zamanı (1970) arasındaki saniye farkı
    TIME1970 = 2208988800
    
    # Struct ile gelen 48 bytelık veriyi 12 adet 32-bit tam sayıya bölüyoruz.
    # 10. indeks (40. byte) bize sunucunun saniye bilgisini (Zaman Damgası) verir.
    zaman_damgasi = struct.unpack('!12I', gelen_veri)[10]
    
    # Bilgisayarın anlayacağı Unix zamanına çevirip datetime objesine dönüştür
    unix_zamani = zaman_damgasi - TIME1970
    return datetime.fromtimestamp(unix_zamani)

def run_sntp_test(host="time.google.com", port=123):
    try:
        # 1. İstemciyi çalıştır, sunucuya bağlan ve ham veriyi al
        gelen_veri = sntp_istegi_gonder(host, port)
        
        # 2. Ham veriyi parse edip anlaşılır zaman formuna getir
        sunucu_zamani = zamani_parse_et(gelen_veri)
        yerel_zaman = datetime.now()
        
        # Task 3: Compare the obtained time with the local system time
        fark = (sunucu_zamani - yerel_zaman).total_seconds()
        
        # Output: Print the current time information received from the server
        print("--- SNTP Time Synchronization ---")
        print("Connection successful, time parsed.")
        print(f"  Server          : {host}")
        print(f"  Server Time     : {sunucu_zamani.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Local Time      : {yerel_zaman.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Time Difference : {abs(fark):.4f} seconds")
        
    except socket.timeout:
        print(f"Connection failed: '{host}' sunucusu cevap vermedi (Timeout).")
    except socket.gaierror:
        print(f"Connection failed: '{host}' adresi çözümlenemedi.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    print("SNTP zaman senkronizasyonu başlatılıyor...\n")
    run_sntp_test()
