#!/usr/bin/python
import discord
import psutil
import asyncio
from gpustat.core import GPUStatCollection, GPUStat


# Your bot token
TOKEN = open("token.txt").read()

intents = discord.Intents.default()

# Discord client
client = discord.Client(intents=intents)

# Function to get GPU usage
def get_gpu_stats() -> GPUStat:
    # This is a placeholder function to simulate getting GPU usage
    # You may need to use a library like pynvml for Nvidia GPUs or similar for AMD
    stats = GPUStatCollection.new_query()
    gpu0_stats = stats[0]

    return gpu0_stats

# Function to get memory usage
def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

# Get CPU utiliation
def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return cpu_percent

# Function to update bot's status
async def update_status():
    while True:
        mem_percent = get_memory_usage()
        cpu_percent = get_cpu_usage()
        # unused because discord won't display multiple lines of `state`

        gpu_stats = get_gpu_stats()

        vram_used_gb = gpu_stats.memory_used/1000
        vram_total_gb = gpu_stats.memory_total/1000

        if vram_used_gb > 5:
            name = "the mAP go up 📈"
        else:
            name = "dust collect on the fans"


        details = f'''
        GPU: {gpu_stats.utilization}% | {vram_used_gb:.1f}/{vram_total_gb:.1f} GB
        '''

        # Update bot's status with GPU and memory usage
        await client.change_presence(activity=discord.Activity(
            type = discord.ActivityType.watching,
            name = name,
            state = details,
            assets = {},
            party = {},
            buttons = []
        ))
        
        # Wait for 5 seconds before updating again
        await asyncio.sleep(5)

# Event: Bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # Start updating bot's status
    client.loop.create_task(update_status())

# Run the bot
client.run(TOKEN)