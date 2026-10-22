import socket

def ayarlari_uygula_ve_goster():
    print("--- 1. SOCKET SETTINGS (AYARLAR) ---")
    
    # TCP Soketi oluştur
    soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 1. Varsayılan Buffer (Tampon) Boyutlarını Okuma
    varsayilan_gonderim = soket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    varsayilan_alim = soket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print(f"[*] Varsayılan Gönderim Buffer Boyutu : {varsayilan_gonderim} bytes")
    print(f"[*] Varsayılan Alım Buffer Boyutu     : {varsayilan_alim} bytes")
    
    # 2. Buffer Boyutlarını Değiştirme (Örneğin 4096 byte yapıyoruz)
    soket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)
    soket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
    
    yeni_gonderim = soket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    yeni_alim = soket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print(f"[+] YENİ Gönderim Buffer Boyutu       : {yeni_gonderim} bytes")
    print(f"[+] YENİ Alım Buffer Boyutu           : {yeni_alim} bytes")
    
    # 3. Timeout Ayarını Değiştirme
    print(f"[*] Varsayılan Timeout                : {soket.gettimeout()} (None = Sonsuza kadar bekler)")
    soket.settimeout(3.5) # 3.5 saniye zaman aşımı ekledik
    print(f"[+] YENİ Timeout Ayarı                : {soket.gettimeout()} saniye")
    
    # 4. Blocking / Non-blocking Modları Arasında Geçiş
    # Soketler varsayılan olarak blocking (bekleyen) moddadır.
    soket.setblocking(False) # Non-blocking (Beklemeyen) moda alıyoruz
    print("[+] Soket 'Non-blocking' (Beklemesiz) moda alındı.")
    
    soket.close()
    print("-" * 40 + "\n")


def hata_yonetimini_test_et():
    print("--- 2. ERROR MANAGEMENT (HATA YÖNETİMİ) ---")
    
    # Senaryo 1: Timeout (Zaman Aşımı) Hatası
    # Cevap vermeyen bir IP adresine (örneğin reserve edilmiş 192.0.2.1) bağlanmaya çalışıyoruz.
    print("[*] Senaryo 1: Cevap vermeyen sunucuya bağlanılıyor (Timeout Testi)...")
    soket_timeout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soket_timeout.settimeout(2.0) # 2 saniye sonra pes et
    try:
        soket_timeout.connect(('192.0.2.1', 80))
    except socket.timeout:
        print("[!] HATA YAKALANDI (Timeout): Sunucu belirlenen süre içinde cevap vermedi.")
    except Exception as e:
        print(f"[!] HATA: {e}")
    finally:
        soket_timeout.close()


    # Senaryo 2: Connection Refused (Bağlantı Reddedildi) Hatası
    # Kendi bilgisayarımızda (127.0.0.1) açık olmayan, rastgele bir porta bağlanmayı deniyoruz.
    print("\n[*] Senaryo 2: Kapalı bir porta bağlanılıyor (Connection Refused Testi)...")
    soket_refused = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soket_refused.connect(('127.0.0.1', 54321)) # 54321 portunda dinleyen kimse yok
    except ConnectionRefusedError:
        print("[!] HATA YAKALANDI (Connection Refused): Hedef makine bağlantıyı aktif olarak reddetti. (Port kapalı)")
    except Exception as e:
        print(f"[!] HATA: {e}")
    finally:
        soket_refused.close()


    # Senaryo 3: Non-blocking Modda Beklenen Hata
    # Non-blocking modda connect atıldığında bağlantı anında kurulamazsa kod beklemek yerine hata fırlatır.
    print("\n[*] Senaryo 3: Non-blocking soket ile anında bağlantı denemesi (BlockingIOError Testi)...")
    soket_nonblock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soket_nonblock.setblocking(False)
    try:
        soket_nonblock.connect(('8.8.8.8', 80))
    except BlockingIOError:
        print("[!] HATA YAKALANDI (BlockingIOError): Soket non-blocking modda olduğu için bağlantı arka planda sürerken program akışı kesilmedi.")
    except Exception as e:
        # Windows'ta bazen farklı bir hata (WSAEWOULDBLOCK) dönebilir
        print(f"[!] HATA YAKALANDI (Non-blocking): İşlem hemen tamamlanamadı. Detay: {e}")
    finally:
        soket_nonblock.close()

if __name__ == "__main__":
    print("Modül E Başlatılıyor...\n")
    ayarlari_uygula_ve_goster()
    hata_yonetimini_test_et()
