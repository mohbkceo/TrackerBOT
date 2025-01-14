import json
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from telegram import Update
from telegram.ext import Application, CommandHandler

# Telegram bot token (replace with your bot token)
TOKEN = 'YOUR_BOT_TOKEN'

async def ip_track(update: Update, context):
    chat_id = update.message.chat_id
    ip = ' '.join(context.args)  
    if not ip:
        await update.message.reply_text("Please provide an IP address like this: /iptrack 8.8.8.8")
        return

    try:
        req_api = requests.get(f"http://ipwho.is/{ip}")
        ip_data = json.loads(req_api.text)
        
        result = (
            f"IP: {ip}\n"
            f"Type: {ip_data['type']}\n"
            f"Country: {ip_data['country']}\n"
            f"City: {ip_data['city']}\n"
            f"Latitude: {ip_data['latitude']}\n"
            f"Longitude: {ip_data['longitude']}\n"
            f"ISP: {ip_data['connection']['isp']}\n"
            f"Timezone: {ip_data['timezone']['id']}\n"
            f"Google Maps: https://www.google.com/maps/@{ip_data['latitude']},{ip_data['longitude']},8z"
        )
        
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Error retrieving IP info: {e}")


async def phone_track(update: Update, context):
    phone_number = ' '.join(context.args) 
    if not phone_number:
        await update.message.reply_text("Please provide a phone number like this: /phonetrack +1234567890")
        return
    
    try:
        parsed_number = phonenumbers.parse(phone_number)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        provider = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "en")
        timezones = timezone.time_zones_for_number(parsed_number)
        
        # Formatting the result
        result = (
            f"Phone Number: {phone_number}\n"
            f"Location: {location}\n"
            f"Region Code: {region_code}\n"
            f"Provider: {provider}\n"
            f"Timezones: {', '.join(timezones)}\n"
        )
        
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Error retrieving phone info: {e}")

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Use /iptrack <IP> or /phonetrack <PhoneNumber> to track info.")

# Main function to start the bot
async def main():
    # Create the Application instance
    application = Application.builder().token(TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("iptrack", ip_track))
    application.add_handler(CommandHandler("phonetrack", phone_track))
    
    # Start the bot using run_polling
    await application.run_polling()

if __name__ == '__main__':
    # Run the main function (Telegram bot will handle the event loop)
    Update.run(main())
