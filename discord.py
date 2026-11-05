import asyncio
import logging
import logging.handlers
import os
import random

import discord
from discord.ext import commands
from aiohttp import ClientSession, ClientTimeout


# ==============================
# CONFIGURACIÓN
# ==============================

intents = discord.Intents.default()
intents.message_content = True

PREFIX = "$"


# ==============================
# CLASE PERSONALIZADA DEL BOT
# ==============================

class CustomBot(commands.Bot):

    def __init__(self, web_client, **kwargs):
        super().__init__(**kwargs)
        self.web_client = web_client

    async def setup_hook(self):
        print("El bot está preparando sus funciones...")


# ==============================
# COMANDOS
# ==============================

async def register_commands(bot):

    @bot.event
    async def on_ready():
        print(f"Conectado como {bot.user}")
        print("El bot está listo para funcionar.")

    @bot.command()
    async def hello(ctx):
        await ctx.send(f"Hola, soy un bot {bot.user}!")

    @bot.command()
    async def heh(ctx, count_heh: int = 5):
        if count_heh < 1 or count_heh > 100:
            await ctx.send("El número debe estar entre 1 y 100.")
            return

        await ctx.send("he" * count_heh)

    @bot.command()
    async def python(ctx):
        await ctx.send("¡El mejor grupo es el 13325!")

    @bot.command()
    async def dado(ctx):
        numero = random.randint(1, 6)

        await ctx.send(
            f"He rodado el dado, EL DESTINO HA HABLADO, "
            f"el número que salió fue.... {numero} !"
        )

    @bot.command()
    async def suma(ctx, num1: int, num2: int):
        await ctx.send(
            f"La suma de {num1} y {num2} es {num1 + num2}"
        )

    @bot.command()
    async def manualidad(ctx):
        await ctx.send(
            "📦 Cartón: organizador para lápices.\n"
            "Consigue una caja pequeña de cartón.\n"
            "Corta la parte superior si es necesario.\n"
            "Forra o decora la caja con papel usado.\n"
            "Puedes dividirla con pequeños trozos de cartón.\n"
            "Úsala para guardar lápices, marcadores "
            "o materiales escolares."
        )

    @bot.command()
    async def dato(ctx):
        await ctx.send(
            "¿Sabías que una botella de plástico puede "
            "tardar cientos de años en degradarse? "
            "En vez de dejar que nuestros residuos "
            "contaminen el planeta durante generaciones, "
            "podemos convertirlos en algo útil. "
            "Reciclar toma minutos; contaminar puede durar siglos."
        )

    @bot.command()
    async def meme(ctx):

        probabilidad = random.randint(1, 100)

        if probabilidad <= 5:
            imagen = "meme4.jpeg"
            await ctx.send("Te tocó el más raro")

        elif probabilidad <= 20:
            imagen = "meme3.jpeg"

        elif probabilidad <= 50:
            imagen = "meme2.jpeg"

        else:
            imagen = "meme1.jpeg"

        ruta = os.path.join("images", imagen)

        if not os.path.isfile(ruta):
            await ctx.send(f"No encuentro la imagen {imagen}.")
            return

        await ctx.send(file=discord.File(ruta))

    @bot.command()
    async def aburrido(ctx):
        await ctx.send(
            "Oh, ¿estás aburrido? Te voy a recomendar "
            "juegos de Roblox.\n"
            "No hay uno mejor que el otro, son gustos.\n"
            "Primero: Robar un huevo.\n"
            "2: Hospital de animales.\n"
            "3: Recoger hojas.\n"
            "4: Encuentra la aguja en un pajar.\n"
            "5: Talla madera.\n"
            "Esas son mis 5 recomendaciones para ti :)"
        )

    # ==============================
    # IMÁGENES DE PERROS
    # ==============================

    @bot.command()
    async def dog(ctx):

        url = "https://random.dog/woof.json"

        try:
            async with bot.web_client.get(url) as response:

                if response.status != 200:
                    await ctx.send("No pude conseguir una imagen de perro.")
                    return

                data = await response.json()
                image_url = data["url"]

                await ctx.send(image_url)

        except Exception as e:
            print(f"Error en dog: {e}")
            await ctx.send("Hubo un error al buscar el perro.")

    # ==============================
    # IMÁGENES DE PATOS
    # ==============================

    @bot.command()
    async def duck(ctx):

        url = "https://random-d.uk/api/random"

        try:
            async with bot.web_client.get(url) as response:

                if response.status != 200:
                    await ctx.send("No pude conseguir una imagen de pato.")
                    return

                data = await response.json()
                image_url = data["url"]

                await ctx.send(image_url)

        except Exception as e:
            print(f"Error en duck: {e}")
            await ctx.send("Hubo un error al buscar el pato.")


# ==============================
# EJECUCIÓN PRINCIPAL
# ==============================

async def main():

    # Configuración de logs

    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,
        backupCount=5
    )

    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}",
        "%Y-%m-%d %H:%M:%S",
        style="{"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Cliente HTTP asíncrono

    timeout = ClientTimeout(total=15)

    async with ClientSession(timeout=timeout) as web_client:

        async with CustomBot(
            web_client=web_client,
            command_prefix=PREFIX,
            intents=intents
        ) as bot:

            await register_commands(bot)

            token = os.getenv("TOKEN")

            if not token:
                raise RuntimeError(
                    "No se encontró el TOKEN. "
                    "Configúralo como variable de entorno."
                )

            await bot.start(token)


# ==============================
# INICIAR BOT
# ==============================

if __name__ == "__main__":
    asyncio.run(main())


    
bot.run("")
