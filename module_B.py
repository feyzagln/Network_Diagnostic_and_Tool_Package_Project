import socket
import threading
import time

def echo_sunucusu(host, port):
    """
    Task 1: On the server side, create a socket and listen on a specified port.
    """
    # IPv4 (AF_INET) ve TCP (SOCK_STREAM) türünde bir soket oluştur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Portun işletim sistemi tarafından hemen tekrar kullanılabilmesi için ayar
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Sunucuyu belirtilen IP ve Porta bağla ve dinlemeye başla
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    try:
        # İstemciden gelecek bağlantıyı kabul et
        conn, addr = server_socket.accept()
        with conn:
            # Veriyi al (maksimum 1024 byte)
            data = conn.recv(1024)
            if data:
                # Task 2'nin sunucu kısmı: Gelen veriyi aynen geri gönder (Echo)
                conn.sendall(data)
    except Exception as e:
        print(f"Sunucu hatası: {e}")
    finally:
        server_socket.close()

def echo_istemcisi(host, port, mesaj):
    """
    Task 2: On the client side, connect to the server and receive the same data that was sent.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Sunucuya bağlan
        client_socket.connect((host, port))
        
        # Veriyi gönder (string'i byte'a çevirerek)
        client_socket.sendall(mesaj.encode('utf-8'))
        
        # Sunucudan gelen cevabı (yankıyı) al
        gelen_veri = client_socket.recv(1024)
        
        # Byte formatındaki cevabı tekrar string'e çevir
        return gelen_veri.decode('utf-8')
    finally:
        client_socket.close()

def run_echo_test(host='127.0.0.1', port=65432, gonderilen_mesaj="Test Data 123"):
    # Sunucuyu arka planda (ayrı bir thread olarak) başlat ki kod bloklanmasın
    server_thread = threading.Thread(target=echo_sunucusu, args=(host, port))
    server_thread.daemon = True
    server_thread.start()
    
    # Sunucunun ayağa kalkıp dinlemeye başlaması için çok kısa bir süre bekle
    time.sleep(0.5)
    
    try:
        # İstemciyi çalıştır ve gönderilen mesajı sunucuya ilet
        alinan_mesaj = echo_istemcisi(host, port, gonderilen_mesaj)
        
        # Task 3: Compare the sent and received data.
        if gonderilen_mesaj == alinan_mesaj:
            # Output: Display the connection test result on the screen
            print("Connection successful, data matches.")
            print(f"  Sent     : {gonderilen_mesaj}")
            print(f"  Received : {alinan_mesaj}")
        else:
            print("Connection successful, but data DOES NOT match!")
            print(f"  Sent     : {gonderilen_mesaj}")
            print(f"  Received : {alinan_mesaj}")
            
    except ConnectionRefusedError:
        print("Connection failed: Sunucuya bağlanılamadı.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    print("Echo testi başlatılıyor...\n")
    run_echo_test()
