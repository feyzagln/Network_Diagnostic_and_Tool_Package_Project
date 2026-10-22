import socket
import threading
from datetime import datetime
import sys

# Mesajların kaydedileceği dosyanın adı
LOG_FILE = "chat_log.txt"

def mesaji_kaydet_ve_yazdir(rol, mesaj):
    """
    Task 3 & Output: Mesajları hem ekrana yazdırır hem de chat_log.txt dosyasına kaydeder.
    """
    zaman = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatli_mesaj = f"[{zaman}] {rol}: {mesaj}"
    
    # Ekrana yazdırma
    if rol == "Siz":
        print(f"[{zaman}] Siz: {mesaj}")
    else:
        # Karşıdan mesaj geldiğinde, terminal giriş (>) satırının bozulmaması için alt satıra atar
        print(f"\r[{zaman}] {rol}: {mesaj}\n> ", end="")

    # Dosyaya kaydetme (Append 'a' modu ile her mesajı dosyanın sonuna ekler)
    with open(LOG_FILE, "a", encoding="utf-8") as dosya:
        dosya.write(formatli_mesaj + "\n")

def mesaj_dinle(soket, karsi_taraf_ismi):
    """Arka planda sürekli karşı taraftan gelen mesajları dinler."""
    while True:
        try:
            veri = soket.recv(1024)
            if not veri:
                print("\nBağlantı karşı taraf tarafından kapatıldı.")
                break
            mesaj = veri.decode('utf-8')
            mesaji_kaydet_ve_yazdir(karsi_taraf_ismi, mesaj)
        except:
            print("\nBağlantı koptu.")
            break
    
    soket.close()
    sys.exit(0) # Karşı taraf çıkarsa programı kapat

def sunucu_baslat():
    host = input("Dinlenecek IP (Varsayılan 127.0.0.1): ") or '127.0.0.1'
    port = input("Port (Varsayılan 65432): ") or '65432'
    port = int(port)

    # TCP Soketi oluştur ve dinlemeye başla
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    
    print(f"\nSunucu {host}:{port} adresinde dinliyor. İstemci (Client) bekleniyor...")
    conn, addr = server.accept()
    print(f"✅ Bağlantı kuruldu! {addr} bağlandı. (Çıkmak için 'quit' yazın)\n")
    
    # Karşıdan gelen mesajları dinlemek için arka plan iş parçacığı (Thread) başlat
    threading.Thread(target=mesaj_dinle, args=(conn, "Client"), daemon=True).start()

    # Kendi mesajlarımızı göndermek için sonsuz döngü
    while True:
        msg = input("> ")
        if msg.lower() == 'quit':
            conn.close()
            server.close()
            break
        if msg:
            conn.sendall(msg.encode('utf-8'))
            mesaji_kaydet_ve_yazdir("Siz", msg)

def istemci_baslat():
    host = input("Bağlanılacak Sunucu IP (Varsayılan 127.0.0.1): ") or '127.0.0.1'
    port = input("Port (Varsayılan 65432): ") or '65432'
    port = int(port)

    # TCP Soketi oluştur ve sunucuya bağlan
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print(f"\n✅ {host}:{port} adresindeki sunucuya başarıyla bağlanıldı! (Çıkmak için 'quit' yazın)\n")
        
        # Karşıdan gelen mesajları dinlemek için arka plan iş parçacığı (Thread) başlat
        threading.Thread(target=mesaj_dinle, args=(client, "Server"), daemon=True).start()

        # Kendi mesajlarımızı göndermek için sonsuz döngü
        while True:
            msg = input("> ")
            if msg.lower() == 'quit':
                client.close()
                break
            if msg:
                client.sendall(msg.encode('utf-8'))
                mesaji_kaydet_ve_yazdir("Siz", msg)
    except Exception as e:
        print(f"❌ Bağlantı hatası: Sunucu bulunamadı. ({e})")

if __name__ == "__main__":
    print("--- Simple Chat Module ---")
    print("1. Server (Sunucu) olarak başlat")
    print("2. Client (İstemci) olarak başlat")
    
    # Task 1: Allow the user to choose mode
    secim = input("Rolünüzü seçin (1 veya 2): ")
    
    if secim == '1':
        sunucu_baslat()
    elif secim == '2':
        istemci_baslat()
    else:
        print("Geçersiz seçim yaptınız.")
