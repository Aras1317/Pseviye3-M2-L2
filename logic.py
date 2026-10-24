import random
import aiohttp
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    
    def __init__(self, sahip: str):
        self.sahip = sahip
        # 1 ile 898 arasındaki orijinal Pokémonlardan rastgele bir ID seç:
        self.pokemon_id = random.randint(1, 898)
        self.isim = ""
        self.resim_url = ""
        self.agirlik = 0
        self.deneyim = 0
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        self.max_hp = self.hp
        self.last_feed_time = datetime.now()

        Pokemon.pokemons[sahip] = self

    # Temel feed() Metodu:
    async def feed(self, feed_interval=60, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"**{self.isim}** beslendi! (+{hp_increase} HP) Yeni Can: **{self.hp}**"
        else:
            kalan = int((self.last_feed_time + delta_time - current_time).total_seconds())
            return f"Pokémon henüz aç değil! **{kalan}** saniye sonra besleyebilirsin."

    async def bilgi_getir(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_id}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.isim = data["name"].capitalize()
                        self.resim_url = data["sprites"]["front_default"]
                        self.agirlik = data.get("weight", 0)
                        self.deneyim = data.get("base_experience", 0)
                        return self.isim, self.resim_url
                    else:
                        print(f"PokeAPI hatası: HTTP {response.status}")
                        return "Bilinmeyen Pokémon", None
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            return "Bağlantı Hatası", None

    async def show_img(self):
        if not self.resim_url:
            await self.bilgi_getir()
        return self.resim_url

    async def attack(self, enemy: 'Pokemon'):
        if isinstance(enemy, Wizard) and random.randint(1, 5) == 1:
            return f"**{enemy.sahip}** adlı kullanıcının Sihirbaz Pokémonu sihirli bir kalkan açtı ve hiç hasar almadı!"

        if enemy.hp > self.power:  # Rakibin canı saldırı gücünden fazlaysa
            enemy.hp -= self.power  # Rakibin canını saldırı gücü kadar azaltır
            return (
                f"**{self.sahip}**, **{enemy.sahip}**'e saldırdı!\n"
                f"Verilen Hasar: **{self.power}**\n"
                f"**{enemy.sahip}** Kalan Can: **{enemy.hp}**"
            )
        else:  # Rakibin canı saldırı gücüne eşit veya daha azsa
            enemy.hp = 0  # Rakibin canını sıfırlayarak bayıltır
            return f"**{self.sahip}**, **{enemy.sahip}**'in Pokémonunu YENDİ! (K.O.)"


# 2. Sihirbaz: +20 HP Büyülü Şifa
class Wizard(Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=20)


# 3. Dövüşçü: 10 Saniyede Bir Hızlı Beslenme ve Özel Saldırı
class Fighter(Pokemon):
    async def feed(self):
        return await super().feed(feed_interval=10)

    async def attack(self, enemy: 'Pokemon'):
        super_power = random.randint(15, 30)
        self.power += super_power  # Saldırı gücüne süper güç ekle
        result = await super().attack(enemy)
        self.power -= super_power
        return result