import discord
from discord.ext import tasks
import time
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# === WISPBYTE / RENDER KANDIRMA SİSTEMİ (Keep-Alive) ===
class BasitSunucu(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot 7/24 Aktif!")
    def log_message(self, format, *args):
        pass

def web_sunucusu_baslat():
    try:
        port = int(os.environ.get('PORT', 8080)) # Render otomatik PORT verir, burası hayati önem taşıyor
        server = HTTPServer(('0.0.0.0', port), BasitSunucu)
        server.serve_forever()
    except Exception as e:
        pass

threading.Thread(target=web_sunucusu_baslat, daemon=True).start()
# ===============================================

# === SENİN AYARLARIN ===
TOKEN = """MTQ3NzUwNDE3ODEzNzA3MTY3Ng.GEShna.lvXzjn6FJvLETgVkWggkiIkDGhLt1l6alwNX24""".strip()

KANAL_ID = 1532840274580078612 # Ticaret mesajı atılacak metin kanalı
SES_KANALI_ID = 1525192508185903125 # 7/24 oturacağı ses kanalı

BEKLEME_SURESI_DAKIKA = 3
RPC_YAZISI = "TRADER" 

MESAJ = """**:moneybag: BUYING STEAL A BRAINROT (SAB) :moneybag:
Boppin Bunny / Jolly Sahur / Festive 67 / Capitano / Popcuro / Clover Ketu / Pegasus / Burguro — $1.00 Each
Garama                                                              — $0.50 Each　　　　
Cerberus / Reinito / Spooky / Cookie     — $1.30 Each
Foxini / Dug Dug Dug / Rico Dinero          — $4.50 Each　
Venuspino                                                          — $6.00 Each
La Casa                                                               — $6.50 Each　　　　　　　　　             　
Dragon Cannelloni                                          — $12.00 Each
Hydra Dragon                                                   — $16.00 Each
:white_check_mark: Buying ALL Brainrots at Good Prices — DM Me and Send Your Price. **"""
# =======================

class OtoMesajci(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_ready(self):
        print(f'Giris yapildi: {self.user} | Hesap Artik Aktif!')
        
        oyun = discord.Activity(type=discord.ActivityType.playing, name=RPC_YAZISI)
        await self.change_presence(status=discord.Status.online, activity=oyun)
        
        try:
            ses_kanali = self.get_channel(SES_KANALI_ID)
            if ses_kanali:
                await ses_kanali.guild.change_voice_state(channel=ses_kanali, self_mute=True, self_deaf=True)
                print(f"7/24 Sese basariyla oturuldu: {ses_kanali.name}")
            else:
                print("HATA: Ses kanali bulunamadi!")
        except Exception as e:
            print(f"Sese girerken hata: {e}")

        if not self.mesaj_gonder.is_running():
            self.mesaj_gonder.start()

    @tasks.loop(minutes=BEKLEME_SURESI_DAKIKA)
    async def mesaj_gonder(self):
        try:
            kanal = self.get_channel(KANAL_ID)
            if kanal:
                await kanal.send(MESAJ)
                print("Basarili! Yeni mesaj gonderildi. 3 dakika bekleniyor...")
        except Exception as e:
            print(f"Mesaj atarken hata: {e}")

    @mesaj_gonder.before_loop
    async def before_mesaj_gonder(self):
        await self.wait_until_ready()

client = OtoMesajci()

try:
    client.run(TOKEN)
except Exception as e:
    print(f"Baglanti koptu: {e}")
finally:
    print("Sistem durdu! 5 saniye icinde otomatik olarak kendini baştan baslatiyor...")
    time.sleep(5)
    os.execv(sys.executable, ['python'] + sys.argv)
