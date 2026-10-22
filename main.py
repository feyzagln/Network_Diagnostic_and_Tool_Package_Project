import tkinter as tk # Uygulamanın görsel arayüzünü (GUI) oluşturan temel kütüphanem. Pencereler, metin kutuları ve çerçeveleri bununla çizdim.
from tkinter import ttk, messagebox # ttk: Tkinter'a daha modern ve şık görünen butonlar/menüler sağlıyor. messagebox: Kullanıcıya gösterilen hata pop-up pencerelerini oluşturur.
import datetime # Sistemin saatini okumak, zaman farklarını hesaplamak için kullanılır.
import platform # İşletim sistemini tespit etmek için kullanıyoruz
import socket # İnternete veya yerel ağa bağlanmak, port açıp dinlemek ve veri alıp göndermek için zorunlu.
import subprocess # Pythonun içinden işletim sisteminin terminaline komut gönderip, dönen sonuçları kodun içine çekmemizi sağlar.
import threading # Aynı anda birden fazla threadi yürütmemizi sağlar. Ağ bağlantısı veya mesaj beklerken GUIın donmasını bu sayede engelliyoruz.
import time # Koda belirli noktalarda kısa süreli molalar (beklemeler) verdirmek için kullanılır (Örn: Sunucunun ayağa kalkması için 0.5 saniye beklemek).
import struct #NTP sunucusundan gelen verileri Python'un anlayabileceği sayılara çevirmek için kullanıyormuşuz bunu.

class NetworkToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CEN322 - Network Diagnostic and Tool Package")
        self.root.geometry("1100x650")
        self.root.minsize(1000, 600)
        
        # RENK PALETİ 
        self.bg_dark = "#2C1E21"       
        self.bg_sidebar = "#3D2B2E"    
        self.bg_content = "#FAF3F3"    
        self.accent_red = "#C85C6A"    
        self.accent_hover = "#A94452"  
        self.card_bg = "#FFFFFF"       
        self.text_dark = "#3A2A2D"     
        self.text_light = "#FBEBEB"    
        self.border_color = "#EAD1D4"  
        self.log_bg = "#1A1113"        
        self.log_fg = "#FFD2D7"        
        
        self.setup_styles()
        self.create_layout()
        
        self.show_page("machine_info") 
        self.log_system("GUI Başlatıldı. Modül kodları bekleniyor...")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("TFrame", background=self.bg_content)
        self.style.configure("Card.TFrame", background=self.card_bg, relief="flat", borderwidth=1)
        self.style.configure("TLabel", background=self.bg_content, foreground=self.text_dark, font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10), background=self.accent_red, foreground="#FFFFFF", borderwidth=0)
        self.style.map("TButton", background=[("active", self.accent_hover)])
        self.style.configure("TEntry", fieldbackground="#FFFFFF", foreground=self.text_dark)

    def create_layout(self):
        self.main_pane = tk.PanedWindow(self.root, orient="horizontal", sashwidth=1, bg=self.border_color)
        self.main_pane.pack(fill="both", expand=True)

        # SOL MENÜ (SIDEBAR)
        self.sidebar = tk.Frame(self.main_pane, bg=self.bg_sidebar, width=240)
        self.sidebar.pack_propagate(False)
        self.main_pane.add(self.sidebar)

        brand_frame = tk.Frame(self.sidebar, bg=self.bg_sidebar, pady=25)
        brand_frame.pack(fill="x")
        tk.Label(brand_frame, text="☄", font=("Segoe UI", 26), fg=self.accent_red, bg=self.bg_sidebar).pack(side="left", padx=(20, 10))
        tk.Label(brand_frame, text="Diagnostic\n& Tool Package", font=("Segoe UI", 13, "bold"), fg=self.text_light, bg=self.bg_sidebar, justify="left").pack(side="left")

        self.nav_buttons = {}
        menu_items = [
            ("Machine Info", "machine_info", "ℹ"),
            ("Echo Test", "echo_test", "⇆"),
            ("SNTP Time", "sntp_time", "🕒"),
            ("Chat Client/Server", "chat", "💬"),
            ("Socket Settings", "socket_settings", "⚙"),
            ("Error Logs", "logs", "⚠")
        ]

        for text, page_id, icon in menu_items:
            btn = tk.Button(
                self.sidebar, text=f"  {icon}  {text}", font=("Segoe UI", 11, "bold"),
                anchor="w", bg=self.bg_sidebar, fg="#D1B0B4", activebackground=self.accent_red,
                activeforeground="#FFFFFF", bd=0, cursor="hand2", pady=12, padx=20,
                command=lambda p=page_id: self.show_page(p)
            )
            btn.pack(fill="x", pady=2)
            # Mouse üzerine gelince hafif parlaması için basit animasyon eventleri
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#4E373B", fg="#FFFFFF"))
            btn.bind("<Leave>", lambda e, b=btn: self.restore_btn_color(b))
            self.nav_buttons[page_id] = btn

        # SAĞ İÇERİK ALANI
        self.right_container = tk.Frame(self.main_pane, bg=self.bg_content)
        self.main_pane.add(self.right_container)

        self.top_bar = tk.Frame(self.right_container, bg="#FFFFFF", height=60, bd=0, highlightbackground=self.border_color, highlightthickness=1)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        self.page_title = tk.Label(self.top_bar, text="Machine Information", font=("Segoe UI", 14, "bold"), fg=self.text_dark, bg="#FFFFFF")
        self.page_title.pack(side="left", padx=25, pady=15)


        self.page_frame = tk.Frame(self.right_container, bg=self.bg_content, padx=25, pady=20)
        self.page_frame.pack(fill="both", expand=True)

        self.bottom_panel = tk.Frame(self.right_container, bg="#FFFFFF", height=120, bd=0, highlightbackground=self.border_color, highlightthickness=1)
        self.bottom_panel.pack(fill="x", side="bottom")
        self.bottom_panel.pack_propagate(False)

        tk.Label(self.bottom_panel, text="System Log Console", font=("Segoe UI", 9, "bold"), fg=self.accent_red, bg="#FFFFFF").pack(anchor="w", padx=25, pady=(5, 2))
        self.log_text = tk.Text(self.bottom_panel, bg=self.log_bg, fg=self.log_fg, font=("Consolas", 9), state="disabled", bd=0)
        self.log_text.pack(fill="both", expand=True, padx=25, pady=(0, 10))

    def restore_btn_color(self, btn):
        for p_id, b in self.nav_buttons.items():
            if b == btn:
                if self.current_page == p_id:
                    b.config(bg=self.accent_red, fg="#FFFFFF")
                else:
                    b.config(bg=self.bg_sidebar, fg="#D1B0B4")

    def show_page(self, page_id):
        self.current_page = page_id
        titles = {
            "machine_info": "Machine Information Module (A)",
            "echo_test": "Echo Test Module (B)",
            "sntp_time": "SNTP Time Synchronization Module (C)",
            "chat": "Chat Client/Server Module (D)",
            "socket_settings": "Socket & Error Management Module (E)",
            "logs": "All Error & Activity Logs"
        }
        self.page_title.config(text=titles.get(page_id, "Module"))

      
        for p_id, btn in self.nav_buttons.items():
            if p_id == page_id:
                btn.config(bg=self.accent_red, fg="#FFFFFF")
            else:
                btn.config(bg=self.bg_sidebar, fg="#D1B0B4")

        
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        
        if page_id == "machine_info": self.load_machine_info_page()
        elif page_id == "echo_test": self.load_echo_test_page()
        elif page_id == "sntp_time": self.load_sntp_time_page()
        elif page_id == "socket_settings": self.load_socket_settings_page()
        elif page_id == "chat": self.load_chat_page()
        elif page_id == "logs": self.load_logs_page()

    def log_system(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}\n"
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, formatted)
        self.log_text.see(tk.END) # Her zaman en son gelen logu göstersin diye ekranı aşağı kaydırıyoruz
        self.log_text.config(state="disabled")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MODÜL A ARAYÜZÜ (Makine Bilgisi)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_machine_info_page(self):
        card = tk.Frame(self.page_frame, bg=self.card_bg)
        card.pack(fill="both", expand=True, padx=20, pady=10)
        
        info_text = tk.Text(card, font=("Segoe UI", 11), bg=self.bg_content, bd=0)
        info_text.pack(fill="both", expand=True, padx=20, pady=20)

        def run_machine_info():
            info_text.delete(1.0, tk.END)
            
            try:
                
                # 1. Bilgisayarın ağdaki adını (Hostname) alıyoruz
                hostname = socket.gethostname()
                info_text.insert(tk.END, "\n--- Hostname Sorgusu ---\n")
                info_text.insert(tk.END, f"Hostname: {hostname}\n\n")
                info_text.insert(tk.END, "--- Ağ Arayüzleri ve IP Adresleri ---\n")

                # 2. İşletim sistemini denetleyip uygun terminal komutunu çalıştırıyoruz
                isletim_sistemi = platform.system()
                
                if isletim_sistemi == "Windows":
                    # --- WINDOWS İÇİN (ipconfig) ---
                    # Türkçe Windows'ta Türkç karakter hatası almamak için errors='ignore' ekliyoruz
                    ip_sorgu = subprocess.run(['ipconfig'], capture_output=True, text=True, errors='ignore')
                    
                    for satir in ip_sorgu.stdout.splitlines():
                        satir = satir.strip()
                        # Windows arayüz isimleri ":" ile biter
                        if satir.endswith(":"):
                            arayuz_adi = satir[:-1] # Sondaki ":" işaretini atıyoruz.
                            info_text.insert(tk.END, f"\nArayüz: {arayuz_adi}\n")
                        # IPv4 ve IPv6 satırlarını yakalayıp ":" işaretinden sonrasını alıyoruz
                        elif "IPv4" in satir:
                            ip_adresi = satir.split(":")[-1].strip()
                            info_text.insert(tk.END, f"  IPv4 Adresi: {ip_adresi}\n")
                        elif "IPv6" in satir:
                            ipv6_adresi = satir.split(":")[-1].strip()
                            info_text.insert(tk.END, f"  IPv6 Adresi: {ipv6_adresi}\n")
                            
                else:
                    # --- LINUX / MAC İÇİN (ip addr) ---
                    ip_sorgu = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
                    
                    for satir in ip_sorgu.stdout.splitlines():
                        satir = satir.strip()
                        # Ethernet veya Wi-Fi bağdaştırıcı ismini yakalama mantığı burası
                        if satir and satir[0].isdigit() and ":" in satir:
                            parcalar = satir.split(":")
                            if len(parcalar) >= 2:
                                info_text.insert(tk.END, f"\nArayüz: {parcalar[1].strip()}\n")
                        # Cihazın yerel ağdaki IPv4 adresini çekip (/) kısmından ayırıyoruz
                        elif satir.startswith("inet "):
                            ip_adresi = satir.split()[1].split('/')[0]
                            info_text.insert(tk.END, f"  IPv4 Adresi: {ip_adresi}\n")
                        # IPv6 adresini de listeliyoruz
                        elif satir.startswith("inet6 "):
                            ipv6_adresi = satir.split()[1].split('/')[0]
                            info_text.insert(tk.END, f"  IPv6 Adresi: {ipv6_adresi}\n")
                            
            except Exception as e:
                info_text.insert(tk.END, f"Sistem bilgileri alınırken hata oluştu:\n{e}")

            self.log_system(f"Makine bilgisi ({isletim_sistemi}) arayüzü tetiklendi.")

        btn_run = ttk.Button(card, text="Fetch Machine Info", command=run_machine_info)
        btn_run.pack(pady=10)
        
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MODÜL B ARAYÜZÜ (Echo Test)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_echo_test_page(self):
        card = tk.Frame(self.page_frame, bg=self.card_bg)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        # Üst kısımdaki form alanı (Host, Port, Mesaj)
        form_frame = tk.Frame(card, bg=self.card_bg, pady=15)
        form_frame.pack(fill="x", padx=20)

        tk.Label(form_frame, text="Server Host:", bg=self.card_bg).grid(row=0, column=0)
        host_ent = ttk.Entry(form_frame, width=15)
        host_ent.grid(row=0, column=1, padx=5)
        host_ent.insert(0, "127.0.0.1") 

        tk.Label(form_frame, text="Port:", bg=self.card_bg).grid(row=0, column=2)
        port_ent = ttk.Entry(form_frame, width=8)
        port_ent.grid(row=0, column=3, padx=5)
        port_ent.insert(0, "65432") 

        tk.Label(form_frame, text="Message:", bg=self.card_bg).grid(row=1, column=0, pady=5)
        msg_ent = ttk.Entry(form_frame, width=30)
        msg_ent.grid(row=1, column=1, columnspan=3, pady=5, sticky="w", padx=5)
        msg_ent.insert(0, "Hadi Bakalım Çalışacak mı?") 

        # Sonuçların yazdırılacağı metin alanı
        result_text = tk.Text(card, bg=self.bg_content, bd=0)
        result_text.pack(fill="both", expand=True, padx=20, pady=15)

        # 1. SUNUCU (SERVER) FONKSİYONU
        def echo_sunucusu(host, port):
            # TCP üzerinden güvenli bir köprü kuruyoruz
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # SO_REUSEADDR: Kodu kapatıp açtığımızda port'un "zaten kullanılıyor" hatası vermesini engeller
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server_socket.bind((host, port))
                server_socket.listen(1) # Sadece 1 istemci bekliyoruz
                conn, addr = server_socket.accept() # İstemci gelene kadar kod burada pusuda bekler
                with conn:
                    data = conn.recv(1024)
                    if data:
                        # Gelen veriyi hiçbir işlemden geçirmeden aynen geri yolluyoruz (Echo)
                        conn.sendall(data)
            except Exception as e:
                pass # Arka planda sessiz sedasız kapandığında hata fırlatmasın.
            finally:
                server_socket.close()

        # 2. İSTEMCİ (CLIENT) FONKSİYONU
        def echo_istemcisi(host, port, msg):
            # Tkinter threadleri ile kavga etmesin diye arayüze yazma işlerini güvenli bir sarmalayıcıya(!) alıyoruz
            def arayuze_yaz(metin):
                result_text.insert(tk.END, metin)
                
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(3.0) # Sunucu yoksa sonsuza kadar bekleyip programı dondurmamak için 3 saniye sınır koydum
                client_socket.connect((host, port))
                
                # Metni ağ üzerinden göndermek için encode ediyoruz
                client_socket.sendall(msg.encode('utf-8'))
                
                # Sunucunun yankısını alıp tekrar decode ediyoruz
                gelen_veri = client_socket.recv(1024).decode('utf-8')
                client_socket.close()
                
                # Orijinal mesaj ile gelen yankıyı karşılaştırıyoruz
                if msg == gelen_veri:
                    self.root.after(0, arayuze_yaz, "✅ Connection successful, data matches.\n\n")
                else:
                    self.root.after(0, arayuze_yaz, "❌ Connection successful, but data DOES NOT match!\n\n")
                    
                self.root.after(0, arayuze_yaz, f"  Sent     : {msg}\n")
                self.root.after(0, arayuze_yaz, f"  Received : {gelen_veri}\n")
            
            except socket.timeout:
                self.root.after(0, arayuze_yaz, "❌ Hata: Bağlantı zaman aşımına uğradı (Timeout). Karşı taraf cevap vermiyor.\n")
            except Exception as e:
                self.root.after(0, arayuze_yaz, f"❌ Connection failed: Sunucuya bağlanılamadı.\nDetay: {e}\n")

        # 3. TESTİ TETİKLEYEN ANA FONKSİYON
        def start_echo_test():
            host = host_ent.get()
            msg = msg_ent.get()
            
            try:
                port = int(port_ent.get())
            except ValueError:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Hata: Port geçerli bir sayı olmalıdır!")
                return

            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Hedef: {host}:{port}\nMesaj: {msg}\nEcho testi başlatılıyor...\n\n")
            self.log_system(f"Echo testi tetiklendi ({host}:{port}).")

            # Arayüzümüzün kilitlenmesini engellemek için Sunucuyu arka planda Thread olarak başlatıyoruz.
            server_thread = threading.Thread(target=echo_sunucusu, args=(host, port))
            server_thread.daemon = True # Program kapanırsa bu thread de otomatik ölsün (öldühttp) 
            server_thread.start()

            # Clienti anında başlatırsak sunucu henüz ayağa kalkmamış olabilir ve bağlantı reddedilir.
            # Bu yüzden clienti de ayrı bir thread içinde çok kısa bir gecikme ile yolluyoruz.
            def arka_planda_istemci_calistir():
                time.sleep(0.5) 
                echo_istemcisi(host, port, msg)

            client_thread = threading.Thread(target=arka_planda_istemci_calistir)
            client_thread.daemon = True
            client_thread.start()

        ttk.Button(form_frame, text="Run Echo Test", command=start_echo_test).grid(row=1, column=4, padx=10)
        
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MODÜL C ARAYÜZÜ (SNTP Zaman Senkronizasyonu)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_sntp_time_page(self):
        card = tk.Frame(self.page_frame, bg=self.card_bg)
        card.pack(fill="both", expand=True, padx=20, pady=10)
        
        info_text = tk.Text(card, font=("Segoe UI", 11), bg=self.bg_content, bd=0)
        info_text.pack(fill="both", expand=True, padx=20, pady=20)

        def arka_planda_sntp_calistir():
            # Tkinter arayüzünü güvenle güncellemek için kullandığımız köprü fonksiyon
            def sntp_arayuze_yaz(metin):
                info_text.insert(tk.END, metin)

            host = "time.google.com" # pool.ntp.org kullanmıştım fakat nedense kendi ağımda başta çalıştı sonra çalışmadı falan, Google daha güvenilir geldi onu kullandım.
            port = 123
            
            # İlginç bilgi: İnternet saati 1 Ocak 1900'den, Python saati ise 1 Ocak 1970'ten başladığı için iki takvim arasındaki 70 yıllık saniye farkını sabit olarak belirliyoruz ki eşitleme yapabilelim.
            TIME1970 = 2208988800
            
            # NTP protokolü sunucuya "Bana saati ver" demek için 48 bytelık bir paket bekliyormuş. 
            # 0x1b (27) ile "Ben sürüm 3 kullanan bir clientim" diyoruz ve geri kalan 47 bytı sıfırlarla dolduruyoruz.
            istek_paketi = b'\x1b' + 47 * b'\0'
            
            # Hız önemli olduğu için TCP değil, UDP (SOCK_DGRAM) soketi seçtik.
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.settimeout(5.0) 
            
            try:
                # İsteği yolla ve 1024 bytelık dönüş kotasıyla cevabı bekle
                client.sendto(istek_paketi, (host, port))
                gelen_veri, _ = client.recvfrom(1024)
                
                # Gelen cevap anlamsız ham baytlardır. Struct ile bu 48 bytı 12 parçaya bölüyoruz (!12I).
                # 10. indeks bize saf saniye bilgisini (Timestamp) veriyormuş.
                zaman_damgasi = struct.unpack('!12I', gelen_veri)[10]
                
                # 70 yıllık farkı çıkarıp bilgisayarımızın anlayacağı yıla (1970 sonrası) getiriyoruz.
                unix_zamani = zaman_damgasi - TIME1970
                sunucu_zamani = datetime.datetime.fromtimestamp(unix_zamani)
                yerel_zaman = datetime.datetime.now()
                
                # Sunucu ile yerel bilgisayar saatimiz arasındaki fark (saniye cinsinden sapma oranı)
                fark = (sunucu_zamani - yerel_zaman).total_seconds()
                
                # Sonuçları güvenli bir şekilde arayüze yansıtıyoruz
                self.root.after(0, sntp_arayuze_yaz, "✅ Başarılı: Zaman senkronize edildi.\n\n")
                self.root.after(0, sntp_arayuze_yaz, f"  Server          : {host}\n")
                self.root.after(0, sntp_arayuze_yaz, f"  Server Time     : {sunucu_zamani.strftime('%Y-%m-%d %H:%M:%S')}\n")
                self.root.after(0, sntp_arayuze_yaz, f"  Local Time      : {yerel_zaman.strftime('%Y-%m-%d %H:%M:%S')}\n")
                self.root.after(0, sntp_arayuze_yaz, f"  Time Difference : {abs(fark):.4f} seconds\n")
                self.root.after(0, self.log_system, "SNTP Zaman senkronizasyonu başarıyla tamamlandı.")
                
            except socket.timeout:
                self.root.after(0, sntp_arayuze_yaz, f"❌ Timeout Error: '{host}' sunucusu cevap vermedi.\n")
            except Exception as e:
                self.root.after(0, sntp_arayuze_yaz, f"❌ Beklenmeyen hata: {e}\n")
            finally:
                client.close()

        def fetch_sntp_time():
            info_text.delete(1.0, tk.END)
            info_text.insert(tk.END, "SNTP sunucusuna bağlanılıyor...\nLütfen bekleyin (Maksimum 5 saniye)\n\n")
            self.log_system("SNTP Zaman senkronizasyonu tetiklendi.")
            
            # UDP ağ isteği anında cevap vermeyebilir, GUI'nin kilitlenmemesi için işi arka plana atıyoruz.
            sntp_thread = threading.Thread(target=arka_planda_sntp_calistir)
            sntp_thread.daemon = True
            sntp_thread.start()

        ttk.Button(card, text="Fetch Current Time", command=fetch_sntp_time).pack(pady=10)
     
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MODÜL D ARAYÜZÜ (Basit Sohbet Uygulaması)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_chat_page(self):
        card = tk.Frame(self.page_frame, bg=self.card_bg)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        ctrl_frame = tk.Frame(card, bg=self.card_bg)
        ctrl_frame.pack(fill="x", padx=20, pady=10)

        # Kullanıcı uygulamanın Server mı yoksa Client mi olacağını buradan seçer. Rol belirler.
        tk.Label(ctrl_frame, text="Role:", bg=self.card_bg).pack(side="left")
        role_cb = ttk.Combobox(ctrl_frame, values=["Server", "Client"], width=8, state="readonly")
        role_cb.pack(side="left", padx=5)
        role_cb.set("Server")

        tk.Label(ctrl_frame, text="Host:", bg=self.card_bg).pack(side="left")
        host_ent = ttk.Entry(ctrl_frame, width=15)
        host_ent.pack(side="left", padx=5)
        host_ent.insert(0, "127.0.0.1")

        tk.Label(ctrl_frame, text="Port:", bg=self.card_bg).pack(side="left")
        port_ent = ttk.Entry(ctrl_frame, width=8)
        port_ent.pack(side="left", padx=5)
        port_ent.insert(0, "65432")

        # Sohbet geçmişinin akacağı ana ekran (Dışarıdan metin girilmesini engellemek için state="disabled" yapıyoruz)
        chat_box = tk.Text(card, bg=self.bg_content, state="disabled", wrap="word")
        chat_box.pack(fill="both", expand=True, padx=20, pady=5)

        msg_frame = tk.Frame(card, bg=self.card_bg)
        msg_frame.pack(fill="x", padx=20, pady=10)
        
        msg_ent = ttk.Entry(msg_frame, width=50)
        msg_ent.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # --- AĞ VE SOHBET MANTIĞI ---
        
        self.chat_socket = None # Aktif olarak mesajlaştığımız canlı soketi burada tutacağız.
        self.server_socket = None # Dinleme modunda bekleyen ana sunucu soketi. İptal edebilmek için ayrı tuttuk.
        self.islem_devam_ediyor = False # Çift tıklama ve art arda bağlanma isteklerini bloklamak için kilit mantığı.
        LOG_FILE = "chat_log.txt" 

        def mesaji_ekrana_yaz_ve_kaydet(gonderen, mesaj):
            # 1. Mesajı formatla
            zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatli_mesaj = f"[{zaman}] {gonderen}: {mesaj}\n"
            
            # 2. Arayüz kilidini açıp metni yazdır, sonra ekranı aşağı kaydırıp geri kilitle
            chat_box.config(state="normal")
            chat_box.insert(tk.END, formatli_mesaj)
            chat_box.see(tk.END) 
            chat_box.config(state="disabled")
            
            # 3. Çıktıyı log dosyasına yaz
            try:
                with open(LOG_FILE, "a", encoding="utf-8") as dosya:
                    dosya.write(formatli_mesaj)
            except Exception as e:
                self.log_system(f"Log dosyasına yazılamadı: {e}")

        def mesaj_dinle(soket, karsi_isim):
            # Arka planda sonsuz bir döngüyle karşı taraftan gelen paketleri dinler.
            while True:
                try:
                    veri = soket.recv(1024)
                    if not veri:
                        # Eğer veri boş gelirse (0 byte), karşı taraf bağlantıyı bilerek kesti demektir.
                        self.root.after(0, mesaji_ekrana_yaz_ve_kaydet, "Sistem", "Karşı taraf bağlantıyı kesti.")
                        self.chat_socket = None
                        self.islem_devam_ediyor = False
                        break
                    gelen_mesaj = veri.decode('utf-8')
                    # Thread içinden UI'ye güvenli aktarım
                    self.root.after(0, mesaji_ekrana_yaz_ve_kaydet, karsi_isim, gelen_mesaj)
                except:
                    # Hata varsa (örn: programı aniden kapatmak) döngüyü kırar ve thread'i sonlandırır
                    break

        def toggle_connection():
            # Eğer halihazırda bağlıysak veya butona yeni basıldıysa (işlem sürüyorsa), ikinci tıklamayı yoksay
            if self.chat_socket or getattr(self, 'islem_devam_ediyor', False):
                mesaji_ekrana_yaz_ve_kaydet("Sistem", "Zaten aktif bir bağlantınız veya süren bir işleminiz var.")
                return

            self.islem_devam_ediyor = True
            role = role_cb.get()
            host = host_ent.get()
            
            try:
                port = int(port_ent.get())
            except ValueError:
                mesaji_ekrana_yaz_ve_kaydet("Sistem", "Hata: Port numarası rakam olmalıdır.")
                self.islem_devam_ediyor = False
                return

            if role == "Server":
                mesaji_ekrana_yaz_ve_kaydet("Sistem", f"Sunucu {host}:{port} üzerinde dinliyor... Bağlantı bekleniyor.")
                
                def sunucu_baslat():
                    try:
                        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        self.server_socket.bind((host, port))
                        self.server_socket.listen(1)
                        # Kod burada server gelene kadar bekler. 
                        # Eğer arayüz thread'inde yapsaydık, program biri bağlanana kadar donardı.
                        conn, addr = self.server_socket.accept() 
                        
                        self.chat_socket = conn
                        self.root.after(0, mesaji_ekrana_yaz_ve_kaydet, "Sistem", f"✅ {addr} bağlandı!")
                        # İletişim başladığı için artık karşı tarafı dinlemeye başlayabiliriz
                        threading.Thread(target=mesaj_dinle, args=(conn, "Client"), daemon=True).start()
                    except Exception as e:
                        # Eğer soketi biz kendimiz Disconnect diyerek kapattıysak gereksiz hata göstermesin
                        if self.islem_devam_ediyor: 
                            self.root.after(0, mesaji_ekrana_yaz_ve_kaydet, "Hata", str(e))
                        self.islem_devam_ediyor = False
                        
                threading.Thread(target=sunucu_baslat, daemon=True).start()

            elif role == "Client":
                mesaji_ekrana_yaz_ve_kaydet("Sistem", f"Sunucuya ({host}:{port}) bağlanılıyor...")
                
                def istemci_baslat():
                    try:
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((host, port))
                        
                        self.chat_socket = client
                        self.root.after(0, mesaji_ekrana_yaz_ve_kaydet, "Sistem", "✅ Bağlantı başarılı!")
                        # Karşıdan (sunucudan) gelecek olan mesajları dinlemeye başla
                        threading.Thread(target=mesaj_dinle, args=(client, "Server"), daemon=True).start()
                    except Exception as e:
                        self.islem_devam_ediyor = False
                        self.root.after(0, mesaji_ekrana_yaz_ve_kaydet, "Hata", f"Bağlanılamadı: {e}")
                        
                threading.Thread(target=istemci_baslat, daemon=True).start()

        def disconnect_connection():
            # Hem açık olan sohbeti hem de arkada pusuda dinleyen sunucu soketini zorla kapatır.
            if not self.chat_socket and not self.server_socket:
                mesaji_ekrana_yaz_ve_kaydet("Sistem", "Zaten aktif bir bağlantınız yok.")
                return

            if self.chat_socket:
                try: self.chat_socket.close()
                except: pass
                self.chat_socket = None

            if self.server_socket:
                try: self.server_socket.close()
                except: pass
                self.server_socket = None

            self.islem_devam_ediyor = False
            mesaji_ekrana_yaz_ve_kaydet("Sistem", "Bağlantı sizin tarafınızdan sonlandırıldı.")

        def send_message(event=None):
            mesaj = msg_ent.get()
            if not mesaj:
                return 
                
            if not self.chat_socket:
                mesaji_ekrana_yaz_ve_kaydet("Sistem", "Önce Start/Connect ile bağlantı kurmalısınız!")
                return
                
            try:
                # Yazıyı UTF-8 bayt dizisine çevirip hatta bırakıyoruz
                self.chat_socket.sendall(mesaj.encode('utf-8'))
                mesaji_ekrana_yaz_ve_kaydet("Siz", mesaj)
                msg_ent.delete(0, tk.END) # Kullanıcı kolaylığı: Gönderdikten sonra mesaj kutusunu temizle
            except Exception as e:
                mesaji_ekrana_yaz_ve_kaydet("Hata", f"Mesaj gönderilemedi: {e}")
                self.chat_socket = None
                self.islem_devam_ediyor = False

        ttk.Button(ctrl_frame, text="Start/Connect", command=toggle_connection).pack(side="left", padx=10)
        ttk.Button(ctrl_frame, text="Disconnect", command=disconnect_connection).pack(side="left", padx=5)
        ttk.Button(msg_frame, text="Send", command=send_message).pack(side="right")
        
        # Kullanıcının butona tıklamak yerine sadece "Enter" tuşuna basarak mesaj gönderebilmesini sağlıyor
        msg_ent.bind("<Return>", send_message)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MODÜL E ARAYÜZÜ (Hata ve Ayar Yönetimi)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_socket_settings_page(self):
        card = tk.Frame(self.page_frame, bg=self.card_bg)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        form_frame = tk.Frame(card, bg=self.card_bg)
        form_frame.pack(fill="x", padx=20, pady=15)

        tk.Label(form_frame, text="Timeout (sec):", bg=self.card_bg).grid(row=0, column=0, sticky="w")
        timeout_ent = ttk.Entry(form_frame, width=10)
        timeout_ent.grid(row=0, column=1, padx=10, pady=5)
        timeout_ent.insert(0, "3.5") 

        tk.Label(form_frame, text="Send Buffer:", bg=self.card_bg).grid(row=1, column=0, sticky="w")
        sndbuf_ent = ttk.Entry(form_frame, width=10)
        sndbuf_ent.grid(row=1, column=1, padx=10, pady=5)
        sndbuf_ent.insert(0, "4096")

        tk.Label(form_frame, text="Receive Buffer:", bg=self.card_bg).grid(row=2, column=0, sticky="w")
        rcvbuf_ent = ttk.Entry(form_frame, width=10)
        rcvbuf_ent.grid(row=2, column=1, padx=10, pady=5)
        rcvbuf_ent.insert(0, "4096")
        
        settings_text = tk.Text(card, bg=self.bg_content, bd=0)
        settings_text.pack(fill="both", expand=True, padx=20, pady=15)

        def ekrana_yazdir(metin):
            settings_text.insert(tk.END, metin + "\n")
            settings_text.see(tk.END)

        def arka_planda_test_et(t_val, s_val, r_val):
            # Gerçek bir ağ hatası test alanı. Burada bilerek Exceptions yaratıp programı çöktürmeden nasıl atlatacağımızı gösteriyoruz.
            self.root.after(0, ekrana_yazdir, "--- 1. SOCKET SETTINGS (AYARLAR) ---")
            try:
                soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # İşletim sisteminin bu ağ bağlantısı için RAM'de varsayılan olarak ne kadar buffer ayırdığına bakıyoruz
                def_snd = soket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
                def_rcv = soket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
                self.root.after(0, ekrana_yazdir, f"[*] Varsayılan Gönderim Buffer : {def_snd} bytes")
                self.root.after(0, ekrana_yazdir, f"[*] Varsayılan Alım Buffer     : {def_rcv} bytes")
                
                # Arayüzden kullanıcının girdiği yeni buffer değerlerini kernelde zorunlu kılıyoruz
                soket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, s_val)
                soket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, r_val)
                # Ağın sonsuza kadar donmasını önlemek için timeout ayarlıyoruz
                soket.settimeout(t_val)
                
                new_snd = soket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
                new_rcv = soket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
                self.root.after(0, ekrana_yazdir, f"[+] YENİ Gönderim Buffer       : {new_snd} bytes")
                self.root.after(0, ekrana_yazdir, f"[+] YENİ Alım Buffer           : {new_rcv} bytes")
                self.root.after(0, ekrana_yazdir, f"[+] YENİ Timeout Ayarı         : {soket.gettimeout()} saniye")
                
                # Non-blocking mod: Bağlantı kurulamazsa veya veri gelmezse kodu o satırda bekletmek yerine direkt alt satıra geçer.
                soket.setblocking(False)
                self.root.after(0, ekrana_yazdir, "[+] Soket 'Non-blocking' moda alındı.\n")
                soket.close()

                # --- HATA YÖNETİMİ (ERROR HANDLING) SENARYOLARI ---
                self.root.after(0, ekrana_yazdir, "--- 2. ERROR MANAGEMENT (HATA YÖNETİMİ) ---")
                
                # Senaryo 1: Bilerek var olmayan/cevap vermeyen bir IP adresine istek atıyoruz ki Timeout mekanizması çalışsın.
                self.root.after(0, ekrana_yazdir, "[*] Senaryo 1: Timeout Testi (192.0.2.1 bağlanılıyor)...")
                soket_timeout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soket_timeout.settimeout(t_val)
                try:
                    soket_timeout.connect(('192.0.2.1', 80))
                except socket.timeout:
                    self.root.after(0, ekrana_yazdir, "[!] HATA YAKALANDI (Timeout): Sunucu cevap vermedi.\n")
                except Exception as e:
                    self.root.after(0, ekrana_yazdir, f"[!] HATA: {e}\n")
                finally:
                    soket_timeout.close()

                # Senaryo 2: Kendi bilgisayarımızda açık olmayan (kapalı) rastgele bir porta bağlanıyoruz. İşletim sistemi anında reddetmeli.
                self.root.after(0, ekrana_yazdir, "[*] Senaryo 2: Connection Refused Testi (127.0.0.1:54321)...")
                soket_refused = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    soket_refused.connect(('127.0.0.1', 54321))
                except ConnectionRefusedError:
                    self.root.after(0, ekrana_yazdir, "[!] HATA YAKALANDI (Connection Refused): Port kapalı.\n")
                except Exception as e:
                    self.root.after(0, ekrana_yazdir, f"[!] HATA: {e}\n")
                finally:
                    soket_refused.close()

                # Senaryo 3: Non-blocking açıkken bir yere anında bağlanmaya çalışırsak, işlem arka planda sürdüğü için hata fırlatır.
                self.root.after(0, ekrana_yazdir, "[*] Senaryo 3: Non-blocking Mod Testi...")
                soket_nonblock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soket_nonblock.setblocking(False)
                try:
                    soket_nonblock.connect(('8.8.8.8', 80))
                except BlockingIOError:
                    self.root.after(0, ekrana_yazdir, "[!] HATA YAKALANDI (BlockingIOError): Beklemesiz mod, işlemin bitmesini beklemedi.\n")
                except Exception as e:
                    self.root.after(0, ekrana_yazdir, f"[!] HATA YAKALANDI: {e}\n")
                finally:
                    soket_nonblock.close()

                self.root.after(0, self.log_system, "Modül E testleri başarıyla tamamlandı.")
            except Exception as e:
                self.root.after(0, ekrana_yazdir, f"Sistem hatası: {e}")

        def apply_settings():
            # Arayüzdeki (Entry) kutularından metinleri alıp matematiksel formata dönüştürüyoruz
            try:
                t_val = float(timeout_ent.get())
                s_val = int(sndbuf_ent.get())
                r_val = int(rcvbuf_ent.get())
            except ValueError:
                settings_text.delete(1.0, tk.END)
                settings_text.insert(tk.END, "Hata: Lütfen geçerli sayısal değerler girin.")
                return

            settings_text.delete(1.0, tk.END)
            self.log_system("Soket ayarları uygulandı, testler başlıyor...")
            
            # Bağlantı hataları ve timeout süreleri boyunca programın donmaması için bu ağır testleri arka plana atıyoruz.
            threading.Thread(target=arka_planda_test_et, args=(t_val, s_val, r_val), daemon=True).start()

        ttk.Button(form_frame, text="Apply Changes & Run Tests", command=apply_settings).grid(row=3, column=1, pady=10)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MODÜL F (LOGS) ARAYÜZÜ (Kayıt Ekranı)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_logs_page(self):
        card = tk.Frame(self.page_frame, bg=self.card_bg)
        card.pack(fill="both", expand=True, padx=20, pady=10)
        
        btn_frame = tk.Frame(card, bg=self.card_bg)
        btn_frame.pack(fill="x", padx=20, pady=(15, 0))

        logs_box = tk.Text(card, bg=self.log_bg, fg=self.log_fg, font=("Consolas", 10), bd=0)
        logs_box.pack(fill="both", expand=True, padx=20, pady=15)

        def refresh_logs():
            logs_box.config(state="normal")
            logs_box.delete(1.0, tk.END)
            
            # Uygulamanın en altında duran siyah log barından (self.log_text) tüm birikmiş yazıları çekiyoruz.
            mevcut_loglar = self.log_text.get(1.0, tk.END)
            
            if mevcut_loglar.strip() == "":
                logs_box.insert(tk.END, "Henüz kaydedilmiş bir sistem logu bulunmuyor.\n")
            else:
                logs_box.insert(tk.END, mevcut_loglar)
                
            logs_box.see(tk.END) 
            logs_box.config(state="disabled")

        def clear_logs():
            # Hem alttaki barın hafızasını hem de bu büyük ekranı tamamen siliyoruz (Sıfırlama).
            self.log_text.config(state="normal")
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state="disabled")
            
            refresh_logs()
            self.log_system("Log kayıtları temizlendi.")
            refresh_logs() # "Temizlendi" bilgisini de ekrana yansıtmak için listeyi son kez güncelliyoruz.

        # Sayfaya tıklandığı an güncel logları ekrana dök.
        refresh_logs()

        ttk.Button(btn_frame, text="🔄 Refresh Logs", command=refresh_logs).pack(side="left", padx=(0, 10))
        ttk.Button(btn_frame, text="🗑 Clear Logs", command=clear_logs).pack(side="left")

# UYGULAMA BAŞLANGIÇ NOKTASI
# Program direkt olarak çalıştırılırsa bu blok tetiklenir ve Tkinter mainloopu sonsuza kadar dinlemeye başlar.
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkToolApp(root)
    root.mainloop()
