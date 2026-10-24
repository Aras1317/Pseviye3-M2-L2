import random
import discord
from discord.ext import commands
from config import TOKEN, PREFIX
from logic import Pokemon, Wizard, Fighter

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Kullanıcı giriş yaptı: {bot.user}")
    
@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        # Rastgele bir Pokémon sınıfı seçiyoruz (Normal, Sihirbaz veya Savaşçı)
        pokemon_type = random.choice([Pokemon, Wizard, Fighter])
        pokemon = pokemon_type(author)
        
        await pokemon.bilgi_getir()
        
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed(title=f"{pokemon.isim} ({pokemon.__class__.__name__})", color=discord.Color.green())
            embed.set_image(url=image_url)
            embed.add_field(name="Can (HP)", value=str(pokemon.hp), inline=True)
            embed.add_field(name="Saldırı Gücü", value=str(pokemon.power), inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémon'un görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémon'unuzu oluşturdunuz!")

@bot.command(name="info")
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        embed = discord.Embed(title=f"{pokemon.sahip} Adlı Oyuncunun Pokémon Bilgileri", color=discord.Color.blue())
        embed.add_field(name="Pokémon Adı", value=pokemon.isim if pokemon.isim else "Bilinmiyor", inline=False)
        embed.add_field(name="Sınıfı", value=pokemon.__class__.__name__, inline=True)
        embed.add_field(name="Can (HP)", value=f"{pokemon.hp} / {pokemon.max_hp}", inline=True)
        embed.add_field(name="Saldırı Gücü", value=str(pokemon.power), inline=True)
        embed.add_field(name="Ağırlık", value=str(pokemon.agirlik), inline=True)
        embed.add_field(name="Deneyim", value=str(pokemon.deneyim), inline=True)
        
        if pokemon.resim_url:
            embed.set_thumbnail(url=pokemon.resim_url)
            
        await ctx.send(embed=embed)
    else:
        await ctx.send("Henüz bir Pokémon'un yok! `!go` komutu ile bir Pokémon oluşturabilirsin.")

@bot.command(name="feed")
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        if pokemon.hp <= 0:
            await ctx.send("Pokémon'un bayılmış durumda! Besleyemezsin.")
            return
        result = await pokemon.feed()
        await ctx.send(result)
    else:
        await ctx.send("Henüz bir Pokémon'un yok! `!go` komutu ile bir Pokémon oluşturabilirsin.")

@bot.command(name="attack")
async def attack(ctx, target: discord.Member):
    if ctx.author.name in Pokemon.pokemons and target.name in Pokemon.pokemons:
        attacker = Pokemon.pokemons[ctx.author.name]
        defender = Pokemon.pokemons[target.name]  
        
        if attacker.hp <= 0:
            await ctx.send("Pokémon'un bayılmış durumda! Saldırı yapamazsın.")
            return 
            
        if defender.hp <= 0:
            await ctx.send(f"{target.name}'in Pokémon'u zaten bayıldı! Saldırı yapılamaz.")
            return
        
        result = await attacker.attack(defender)
        await ctx.send(result)
    else:
        await ctx.send("Saldırı yapabilmek için her iki oyuncunun da birer Pokémon'u olmalı!")

bot.run(TOKEN)