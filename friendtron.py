#!/usr/bin/env python
# coding: utf8
"""
Created on Tue Jul 20 15:51:57 2021

@author: naika-local
"""

import discord
import gpt_2_simple as gpt2
import asyncio
import random
import re
import emoji
import speech_recognition as sr
import pyttsx3
from discord import FFmpegOpusAudio
from discord.ext import commands
from namegen import pick_name, pick_townname

#CONFIG VARIABLES
#-----------------------------
#Enables autonomous emoji responses. 
TAG_SYS = True

#Rate between 0 and 1 for how frequently Friendtron will speak 
#in their designated channel, and in private messages.
BOT_CHANNEL_ACTIVATION_RATE = 0.65

#Rate between 0 and 1 for how frequently Friendtron will speak everywhere else.
COMMON_ACTIVATION_RATE = 0.07

#Index of the microphone to be used for speech recognition: 
#use speech_recognition's Microphone.list_microphone_names to choose an index.
MICROPHONE_INDEX = 4


#-----------------------------


sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='take2') # The name of your checkpoint

client = commands.Bot(command_prefix='!')

#When a user adds a reaction to a message, Friendtron might might upvote the reaction.
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    if (not channel or type(channel) == 'NoneType' or payload.user_id == client.user.id):
        return
    message = await channel.fetch_message(payload.message_id)
    #reaction = discord.utils.get(message.reactions, emoji=payload.emoji)
    emoji = payload.emoji
    
    copy_reaction_chance = 0.27
    if (random.random() < copy_reaction_chance):
        print('Copying reaction!')
        await message.add_reaction(emoji)
    else:
        print('Reaction detected: ignoring')
        
#This will find and return the emoji IF it exists in the current server.
#In: the guild from which the bot exists
#In: the emoji text surrounded in colons
#Out: The emoji in a printable format if it exists, the input emoji_name text otherwise.
def get_emoji(emoji_name):
    
    target = emoji_name.strip(":")
    
    for emj in client.emojis:
        if emj.name == target:
            return str(emj)
    
    #If not found, just return the input
    return emoji_name

#Use regexp to replace emoji names with 
def replace_emoji(text):
    
    found_emoji = set(re.findall(":[a-zA-Z0-9_]*:", text))
    new_text = text
    
    for emj in found_emoji:
        new_text = new_text.replace(emj, get_emoji(emj))

    return new_text

async def add_reactions(message, emoji_names):
    random_max_pool = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 4]
    random_max = random.choice(random_max_pool)
    react_activation = 0.75
    corpus = message.content.split()
    
    random_spontaneous_chance = 0.105
    if (random.random() < random_spontaneous_chance):
        await message.add_reaction(get_emoji(random.choice(tuple(emoji_names))))
    
    num_reactions = 0
    
    thinking_phrases = ['thinking', 'hmm', 'uh', 'uhh', 'wtf']
    
    for token in corpus:
        if num_reactions > random_max:
            return
        if (token in thinking_phrases):
            await message.add_reaction(emoji.emojize(':thinking_face:'))
        elif (token in emoji_names):
            if random.random() < react_activation:    
                await message.add_reaction(get_emoji(token))
                num_reactions += 1
        else:
            if random.random() < react_activation and token not in ['soon', 'back'] and len(token) > 3:    
                emj = emoji.emojize(':'+token+':', use_aliases = True)
                if len(emj) == 1:
                    await message.add_reaction(emj)
                    num_reactions += 1



#Discord voice generation: Friendtron will join voice, listen, and say what they feel like
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #Set activity here
    activity = discord.Activity(name='mind games', type=discord.ActivityType.playing)
    await client.change_presence(status=discord.Status.online, activity=activity)
    
    #Collect and update scores
    
    rps_file = open('rps_savedata.sav', 'r')
    save_data = rps_file.read()
    rps_file.close()
    
    whitelist_file = open('whitelist.sav', 'r')
    whitelist = whitelist_file.read()
    whitelist_file.close()
    
    blacklist_file = open('blacklist.sav', 'r')
    blacklist = blacklist_file.read()
    blacklist_file.close()
    
    global rps_scores
    global bot_channels
    global banned_channels
    global emoji_names
    emoji_names = set()
    
    rps_scores = eval(save_data)
    bot_channels = eval(whitelist)
    banned_channels = eval(blacklist)
    
    #Collect pool of available emojis
    if (TAG_SYS):
        for emj in client.emojis:
            emoji_names.add(emj.name)
    
def mtn(id):
    return '<@!' + str(id) + '>'

def save_whitelist():
    whitelist = open('whitelist.sav', 'w')
    whitelist.write(str(bot_channels))
    whitelist.close()
    return
    
def save_blacklist():
    blacklist = open('blacklist.sav', 'w')
    blacklist.write(str(banned_channels))
    blacklist.close()
    return

def replace_mentions(message):
    
    nessie_id = 194198497082212352;
    max_id = 194197793684848640;
    will_id = 501949000170340377;
    lex_id= 194198434230566912;
    kole_id = 166698028579684353;
    j_id = 194198358816980992;
    paltron_id = 877685197817126972;
    
    message = message.replace('@party lads', '<@&746513580974669846>')
    message = message.replace('@Nessie', mtn(nessie_id))
    message = message.replace('@Maxfield', mtn(max_id))
    message = message.replace('@Лекс Кроу', mtn(lex_id))
    message = message.replace('@Chuubifrog', mtn(kole_id))
    message = message.replace('@ArchWill33', mtn(will_id))
    message = message.replace('@Friendtron', mtn(paltron_id))
    message = message.replace('@J2', mtn(j_id))
    
    return message

async def play_rps(move, message):
    
    curr_score = rps_scores.get(message.author.id, 0)
    bot_score = rps_scores.get(client.user.id, 0) #client.user = the bot
    
    options = ['Rock', 'Paper', 'Scissors']
    bot_choice = random.choice(options)
    c = bot_choice.lower()
    bot_choice = bot_choice + '!'
    
    await message.channel.send(bot_choice)
    
    result = ""
    
    #tie
    if (c == move):
        result = 'We tied! Your score is still ' + str(curr_score)
    #player wins
    elif (c == 'rock' and move == 'paper') or (c == 'paper' and move == 'scissors') or (c == 'scissors' and move == 'rock'):
        curr_score += 1
        rps_scores[message.author.id] = curr_score
        result = 'You win! Your score is now ' + str(curr_score)

    elif (c == 'rock' and move == 'scissors') or (c == 'scissors' and move == 'paper') or (c == 'paper' and move == 'rock'):
        bot_score += 1
        rps_scores[client.user.id] = bot_score
        result = 'I win! My score is now ' + str(bot_score)

    else:
        result = 'Something went wrong. Your move: ' + move + ', My move: ' + c

    await message.channel.send(result)
    savescores = open('rps_savedata.sav', 'w')
    savescores.write(str(rps_scores))
    savescores.close()
    
async def joinvoice(ctx):
    """
    Handles joining the voice call, initializes a speech recognizer
    (via Google) and text vocalizer (pyttsx3), and calls the respond_voice
    function.
    

    Parameters
    ----------
    ctx : 
        Current bot context as detailed in discord.py and its extensions

    """
    
    
    channel = ctx.message.author.voice.channel
    await channel.connect()
    
        #Text to speech recognizer: one initialization is enough
    r = sr.Recognizer()
    vocalizer = pyttsx3.init() 
    
    #Disable to use default voice
    #vocalizer.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_HARUKA_11.0')
    #client.loop.create_task(respond_voice(ctx, r, vocalizer))
    await respond_voice(ctx, r, vocalizer)


async def respond_voice(ctx, r, vocalizer):

    vc = ctx.guild.voice_client
    end_phrases = ['quit', 'you can stop now', "that's enough", 'go home', 'go to bed']

    while(vc.is_connected()):
        audio_text = ''
        
        with sr.Microphone(device_index = MICROPHONE_INDEX) as source:
            r.adjust_for_ambient_noise(source)
            print("Listening:")
            audio_text = r.listen(source)
            print("Listening complete")
    
        try:
            input_text = r.recognize_google(audio_text)
            print('I heard: ' + input_text)
            
            #If the received phrase is in the list of end phrases, disconnect
            if input_text in end_phrases:
                await ctx.guild.voice_client.disconnect()
                return
            
            #input text into gpt to get a response
            results = gpt2.generate(sess, run_name='take2', temperature=0.7, nsamples=1, batch_size=1, prefix=input_text+'\n', length=150, return_as_list=True, include_prefix=False, truncate="\n")
            output = results[0].split('\n')[0].encode('ascii', 'ignore').decode('ascii')
            output = output.replace('Friendtron', 'Paltron')
            output = output.replace('friendtron', 'paltron')
            print(output)
            vocalizer.save_to_file(output, 'foutput.mp3') #Here we save the output as a voice
            vocalizer.runAndWait()
            
            #FFmpegPCMAudio reads in a mp3 file to be played by discord
            #The options hopefully reconnect instead of failing outright
            voiceline = FFmpegOpusAudio('foutput.mp3')
            vc.play(voiceline)
            while(vc.is_playing()):
                await asyncio.sleep(0.1)
        
        except Exception as e: 
            print("Issue with speech parsing: ")
            print(e)
            vocalizer.stop()
    
    return
    
    
@client.event
async def on_message(message):
    
    #Command handling
    #----------------------------------
    
    
        #Channel commands (highest priority, so they're listed here)
    #-------------------
    if ('!friendtronchannel' in message.content and '!dni' not in message.content):
    
        if (message.channel.id in bot_channels):
            await message.channel.send('This channel is already a home channel!')
            return
        
        #Add the channel to the set, and save to file
        bot_channels.add(message.channel.id)
        save_whitelist()
        
        #Ensure that the blacklist does not contain the channel
        if (message.channel.id in banned_channels):
            banned_channels.remove(message.channel.id)
            save_blacklist()
            await message.channel.send('Unbanned this channel, and made it a home channel!')
            return
        
        #Feedback message for making it a home channel, if not in blacklist
        await message.channel.send('This channel is now a home channel!')
        return
    
    if ('!friendtronblacklist' in message.content and '!dni' not in message.content):
        
        if (message.channel.id in banned_channels):
            await message.channel.send('This channel is already banned, goodbye')
            return
        
        banned_channels.add(message.channel.id)
        save_blacklist()
        
        #Remove from whitelist if we're blacklisting
        if (message.channel.id in bot_channels):
            bot_channels.remove(message.channel.id)
            save_whitelist()
            await message.channel.send('This channel is no longer a home, and is instead banned :(')
            return
        await message.channel.send("I won't message here anymore :(")
        return 
    
    if ('!friendtronresetchannel' in message.content and '!dni' not in message.content):
        
        if message.channel.id not in bot_channels and message.channel.id not in banned_channels:
            await message.channel.send("I already treat this channel like normal")
            return
        
        bot_channels.discard(message.channel.id)
        save_whitelist()
        banned_channels.discard(message.channel.id)
        save_blacklist()
        await message.channel.send("Channel preferences reset! I'll treat this channel like normal now.")
        return
    #-------------------
    
    #Quit specifically if we use the DNI command, or the channel is banned
    if ('!dni' in message.content or '!DNI' in message.content or message.channel.id in banned_channels):
        return
    
    
    if ('!friendtronhelp' in message.content):
        help_file = open("helpcmd.txt", "r")
        cmds = help_file.read()
        help_file.close()
        await message.channel.send(cmds)
        return
    
    #Rock Paper Scissors commands
    #----------------------
    if ('!rock' in message.content):
        await play_rps('rock', message)
        return
    
    if ('!paper' in message.content):
        await play_rps('paper', message)
        return
    
    if ('!scissors' in message.content):
        await play_rps('scissors', message)
        return
    
    if ('!score' in message.content):
        #get all scores and display them
        msg = 'Scores for rock paper scissors: '
        print(rps_scores)
        for player, score in rps_scores.items():
            user = await client.fetch_user(player)
            if (user):    
                msg = msg + '\n' + user.display_name + ": " + str(score)
        
        await message.channel.send(msg)
        return
    #--------------------
    
    
    if ('!pick' in message.content):
        msg = message.content.replace('!pick ','')
        msg = msg.replace(' or ', ' ')
        options = msg.split(', ')
        print(options)
        options.sort()
        options = tuple(options)
        random.seed(hash(options))
        choice = random.choice(options)
        await message.channel.send('I choose ' + choice)
        return
    
    #nfsw for cursing :(
    if ('!fmk' in message.content):
        msg = message.content.replace('!fmk ','')
        msg = msg.replace(' or ', ' ')
        options = msg.split(', ')
        options.sort()
        random.seed(hash(tuple(options)))
        if (len(options) >= 3):
            op_f = random.choice(options)
            options.remove(op_f)
            op_marry = random.choice(options)
            options.remove(op_marry)
            op_kill = random.choice(options)
            
            fmk_response = "Fuck: " + op_f +", Marry: " + op_marry + ", Kill: " + op_kill
            await message.channel.send(fmk_response)
        else:
            await message.channel.send('Not enough options for FMK :(')
            
        return
    
    if ('!roll' in message.content):
        number = message.content.split()[1]
        try:
            msg = 'You rolled ' + str(random.randint(1, int(number)))
            await message.channel.send(msg)
        except Exception as e:
            print(e)
        finally:
            return
        
    if ('!nametown' in message.content):
        args = message.content.split()
        if (len(args) > 1):
            try:
                nameoptions = pick_townname(int(args[1]))
            except Exception as e:
                print(e)
        else:
            nameoptions = pick_townname()
        shownames = ""
        for name in nameoptions:
            shownames = shownames + name + "\n"
            
        await message.channel.send(shownames)
        return
        
    if ('!name' in message.content):
        args = message.content.split()
        if (len(args) > 1):
            try:
                nameoptions = pick_name(int(args[1]))
            except Exception as e:
                print(e)
        else:
            nameoptions = pick_name()
        shownames = ""
        for name in nameoptions:
            shownames = shownames + name + "\n"
        
        await message.channel.send(shownames)
        return
    
    if ('!joinvoice' in message.content):
        ctx = await client.get_context(message)
        await joinvoice(ctx)
        return
    
    #-------------------------------------------------------
    
    #If the tag system is enabled, attempt to add reactions to the message
    if (TAG_SYS):
        await add_reactions(message, emoji_names)
    
    
    if (message.channel.id in bot_channels) or (message.channel.type == discord.ChannelType.private):
        #print('Correct channel for spontaneous messaging')
        random_activate_threshold = BOT_CHANNEL_ACTIVATION_RATE
    else:
        random_activate_threshold = COMMON_ACTIVATION_RATE
    
    random_activate = (random.random() < random_activate_threshold)
    #print(random_activate)
    
    if random_activate or (client.user.mention in message.content.replace('<@!', '<@')):
        
        if message.author == client.user:
            return
        else:
            
            if client.is_ready:
                async with message.channel.typing():
                    if "makequery" in message.content:
                        if "makequery " in message.content:
                            msgtext = message.content.split('makequery ')[1] + '\n'
                        else:
                            msgtext = message.content.split('makequery')[1] + '\n'
                        print("Making query: " + msgtext)
                        results = gpt2.generate(sess, run_name='take2', temperature=0.9, nsamples=1, batch_size=1, prefix=msgtext, length=350, include_prefix=True, return_as_list=True)
                        await message.channel.send("```\n" + str('=' * 20).join(results) + "\n```")
                        
                    else:
                        prefix = ""
                        last_author = ""
                        old = await message.channel.history(limit=3).flatten()
                        old.reverse()
                        old_content = []
                        for msg in old:
                            old_content.append(msg.content.strip())
                            if last_author == msg.author.name:
                                prefix = prefix + msg.content + "\n"
                            else:
                                last_author = msg.author.name
                                prefix = prefix
                        while True:
                            
                            results = gpt2.generate(sess, run_name='take2', temperature=0.7, nsamples=1, batch_size=1, prefix=prefix, length=150, return_as_list=True, include_prefix=False, truncate="\n\n")
                            res_split = random.choice(results).split('\n')
                            ok = []
                            res_allowed_length = random.randint(1,2)
                            res_added = 0

                            for r in res_split:
                                if (r.strip() not in old_content) and ('Steam Workshop' not in r):
                                    r.encode('utf8').decode('utf8')
                                    new_txt = replace_emoji(r)
                                    new_txt = replace_mentions(new_txt)
                                    new_txt = new_txt.replace('Tim ', 'Paltron ')
                                    new_txt = new_txt.replace(' tim ', ' Paltron ')
                                    ok.append(new_txt)
                                    res_added += 1
                                    if (res_added >= res_allowed_length):
                                        break
                            if len(ok) > 0:
                                break
                        for i, msg in enumerate(ok):
                            
                            if i == (len(ok) -1):
                                await asyncio.sleep(random.randint(0,1))
                                await message.channel.send(msg)
                            else:
                                async with message.channel.typing():
                                    await message.channel.send(msg)
                                    await asyncio.sleep(random.randint(3, 5))                   
            else:
                return
            

client.run('ODY1MzQ1MDY1MjQ0Mjk1MjA4.YPCpZA.ZgEuzd_8_QHcDO-rAfTd8G-D7M8')


    
                
    
    
    