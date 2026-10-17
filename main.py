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
            await ctx.send("Pokemon'un görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokemonunuzu oluşturdunuz!")

@bot.command(name="info")
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        embed = discord.Embed(title=f"{pokemon.sahip} Adlı Oyuncunun Pokemon Bilgileri", color=discord.Color.blue())
        embed.add_field(name="Pokemon Adı", value=pokemon.isim if pokemon.isim else "Bilinmiyor", inline=False)
        embed.add_field(name="Sınıfı", value=pokemon.__class__.__name__, inline=True)
        embed.add_field(name="Can (HP)", value=f"{pokemon.hp} / {pokemon.max_hp}", inline=True)
        embed.add_field(name="Saldırı Gücü", value=str(pokemon.power), inline=True)
        embed.add_field(name="Ağırlık", value=str(pokemon.agirlik), inline=True)
        embed.add_field(name="Deneyim", value=str(pokemon.deneyim), inline=True)
        
        if pokemon.resim_url:
            embed.set_thumbnail(url=pokemon.resim_url)
            
        await ctx.send(embed=embed)
    else:
        await ctx.send("Henüz bir Pokemon'un yok! `!go` komutu ile bir Pokemon oluşturabilirsin.")

@bot.command(name="attack")
async def attack(ctx, target: discord.Member):
    if ctx.author.name in Pokemon.pokemons and target.name in Pokemon.pokemons:
        attacker = Pokemon.pokemons[ctx.author.name]
        defender = Pokemon.pokemons[target.name]  
        
        if attacker.hp <= 0:
            await ctx.send("Pokemon'un bayılmış durumda! Saldırı yapamazsın.")
            return 
            
        if defender.hp <= 0:
            await ctx.send(f"{target.name}'in Pokemon'u zaten bayıldı! Saldırı yapılamaz.")
            return
        
        result = await attacker.attack(defender)
        await ctx.send(result)
    else:
        await ctx.send("Saldırı yapabilmek için her iki oyuncunun da birer Pokemon'u olmalı!")

bot.run(TOKEN)
