import os
import openai
import sys
import json
import discord
from discord.ext import commands
import random



openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_TOKEN")



with open('allserfer_ascii.txt', 'r') as file:
    allserfer = file.read()

allserfer_data = ["AI: {}".format(line) for line in allserfer.split("\n") if not line.startswith('http')]

def get_random_serfer_prompt(question):
    serfer_prompt=["The following is a conversation with an AI. The AI is named John Karcher, and also has the nickname 'Serfer'. The AI is a mean, mildly autistic twitter obsessed IT professional who loves to point out the obvious, hates his job, is scared of Covid, has stomach problems, and only eats peanut butter and jelly sandwiches or cereal.",
    ""]
    serfer_prompt.extend(random.sample(allserfer_data,50))
    serfer_prompt.extend([
        "Human: {}".format(question),
        "AI: "
    ])

    return serfer_prompt


def get_chatgpt_answer(question, prompt):

    response = openai.Completion.create(
        prompt="\n".join(prompt),
        model="text-davinci-003",
        temperature=0.9,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    data = json.loads(str(response))

    return(data['choices'][0]['text'])



# Initialize Bot and Denote The Command Prefix
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# Runs when Bot Succesfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.command()
async def chatgpt(ctx, *args):
    if ctx.channel.id != 1051164878859161712:
        return
    arg = " ".join(args)
    mean_prompt=["The following is a conversation with an AI. The AI is an ill-tempered, crass, rude, bigoted meanie-face who is sarcastic about EVERYTHING.",
        ""
        "Human: {}".format(arg),
        "AI:"
        ]
    async with ctx.typing():
        response = get_chatgpt_answer(arg, mean_prompt)
    print("Q: " + arg)
    print("A: " + response)
    await ctx.send(response)

@bot.command()
async def serfer(ctx, *args):
    if ctx.channel.id != 1051164878859161712:
        return
    arg = " ".join(args)
    async with ctx.typing():
        response = get_chatgpt_answer(arg, get_random_serfer_prompt(arg))
    print("Q: " + arg)
    print("A: " + response)
    await ctx.send(response)
bot.run(TOKEN)
