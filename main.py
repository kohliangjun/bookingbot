from telethon import TelegramClient, events
import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot credentials 
TOKEN = '6683920879:AAExvQONXXukjqhqNPMWLtwgJN_SGHrA12E'
BOT_USERNAME = '@car_bookingbot'
API_id = '20980864'
API_hash = 'd56e104d5aabeb4fd7f24412c934d859'

# Start the bot session 
client = TelegramClient('test one', API_id, API_hash).start(bot_token=TOKEN)
















# Booking command
async def booking_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get text after the "/insert" command and converting it to a list (splitting by space " " symbol)
        list_of_words = update.message.text.split(" ")
        date = list_of_words[1] # the second text (1) = name of which is making the booking   
        name = list_of_words[2] # the third text (2) = type of car that the person is booking  
        car_type = list_of_words[3] # using datetime library to get the date (in DD/MM/YYYY format)

        #
        params = (date, name, car_type)
        sql_command = "INSERT INTO bookings VALUES (NULL, ?, ?, ?);" #
        c.execute(sql_command, params) #
        conn.commit() # commit the changes 
        
        # error handling for booking command
        if c.rowcount < 1: 
            text = "Something went wrong, try again."
            await update.message.reply_text(text)
        else: 
            text = 'Booking made successfully! Please check with /check command.'
            await update.message.reply_text(text)

        # logging for booking command
        message_type: str = update.message.chat.type
        text: str = update.message.text
        
        print(f'User (@{update.message.chat.id}) in {message_type}: "{text}"')

        if message_type == 'group':
            if BOT_USERNAME in text: 
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response(new_text)
            else:
                return
        else: 
            response: str = handle_response(text)

        print('BOT:', response)
        await update.message.reply_text(response)
   
    except Exception as e:
        print(e)
        await update.message.reply_text("😓 Sorry you might have missed out some details in your booking. Please enter your booking in this format ⬇️ :\n\n\n/booking *SPACE* DD/MM(Duration) *SPACE* Name *SPACE* Car Colour\n\n\nℹ️ <b>EXAMPLE</b>\n<em>'/booking   01/01(8am-12pm)   lj   black'</em>", parse_mode='html')
    return      
















# Check Command
def create_message_select_query(ans): # Function that creates a message the contains a list of all the bookings
    text = ""
    current_date = datetime.now().strftime("%d/%m/%Y")
    for i in ans:
        id = i[0]
        usage_date = i[1]
        name = i[2]
        car_type = i[3]
        text += "{:<2} | {} | {:<10} | {}\n".format(id, usage_date, name, car_type)
    message = "Car bookings as of: <u><b>{}</b></u>\n".format(current_date) + "\n" + "-"*38 + "\n" + "id | Date(Duration)      | Name | Car" + "\n" + "-"*38 + "\n" + text        
    return message


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Execute the query and get all (*) the oders
        c.execute("SELECT * FROM bookings")
        res = c.fetchall() # fetch all the results

        # If there is at least 1 row selected, print a message with the list of all the orders
        # The message is created using the function defined above
        if(res):
            text_to_message = create_message_select_query(res) 
            await update.message.reply_text(text_to_message, parse_mode='html')
        # Otherwhise, print a default text
        else:
            text = "No bookings made. You can make a booking with /booking command."
            await update.message.reply_text(text)


        # logging for check command
        message_type: str = update.message.chat.type
        text: str = update.message.text
        
        print(f'User (@{update.message.chat.id}) in {message_type}: "{text}"')

        if message_type == 'group':
            if BOT_USERNAME in text: 
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response(new_text)
            else:
                return
        else: 
            response: str = handle_response(text)

        print('BOT:', response)
        await update.message.reply_text(response)

    except Exception as e: 
        print(e)
        text = "Error Occured: {}".format(e)
        await update.message.reply_text(text, parse_mode='html')
        return



















# Update command
async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get the text of the user AFTER the /update command and convert it to a list (we are splitting by the SPACE " " simbol)
        list_of_words = update.message.text.split(" ")
        id = list_of_words[1] # second (1) item is the id
        usage_date = list_of_words[2] # We get the new date
        name = list_of_words[3] # third (2) item is the name
        car_type = list_of_words[4] # fourth (3) item is the car type
        

        # create the tuple with all the params interted by the user
        params = (id, usage_date, name, car_type, id)

        # Create the UPDATE query, we are updating the product with a specific id so we must put the WHERE clause
        sql_command = "UPDATE bookings SET id=?, date=? , name=?, car_type=? WHERE id =?"
        c.execute(sql_command, params) # Execute the query
        conn.commit() # Commit the changes

        # If at least 1 row is affected by the query we send a specific message
        if c.rowcount < 1:
            text = "Booking  <u><b>{}</b></u>  is not present ❌".format(id)
            await update.message.reply_text(text, parse_mode='html')
        else:
            text = "Booking  <u><b>{}</b></u>  correctly updated ✅".format(id)
            await update.message.reply_text(text, parse_mode='html')

    except Exception as e: 
        print(e)
        await update.message.reply_text("<b>Error Occured:</b> {}".format(e), parse_mode='html')
        await update.message.reply_text("😓 Sorry you might have done something incorrectly. Please update your booking in this format ⬇️ :\n\n/update <b>*SPACE*</b> id <b>*SPACE*</b> DD/MM(Duration) <b>*SPACE*</b> Name <b>*SPACE*</b> Car Colour\n\n\n\nℹ️ <b>NOTE</b>\n- you have to re-enter the correct details, and only change the details you'd like to update\n- booking id MUST be entered after '/update' for me to identify the booking you are editing\n\nℹ️ <b>EXAMPLE</b>\n<em>I want to only change my car colour from black to white\n➡️ '/update   1   01/01(8am-12pm)   lj   white'</em>", parse_mode='html')
        return














# delete Command
async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # get list of words inserted by the user
        list_of_words = update.message.text.split(" ")
        id = list_of_words[1] # The second (1) element is the id

        # Crete the DELETE query passing the is as a parameter
        sql_command = "DELETE FROM bookings WHERE id = (?);"
        ans = c.execute(sql_command, (id,))
        conn.commit()
        
        # If at least 1 row is affected by the query we send a specific message
        if ans.rowcount < 1:
            text = "Booking  <u><b>{}</b></u>  is not present in the database".format(id)
            await update.message.reply_text(text, parse_mode='html')
        else:
            # reset sequence for 'id' column
            sql_reset_seq_command = "DELETE FROM sqlite_sequence WHERE name = 'bookings';" 
            reset_seq = c.execute(sql_reset_seq_command)
            conn.commit()

            text = "Booking  <u><b>{}</b></u>  correctly deleted ✅\n\nTable sequence reset!".format(id)
            await update.message.reply_text(text, parse_mode='html')

    except Exception as e: 
        print(e)
        await update.message.reply_text("<b>Error Occured:</b> {}".format(e), parse_mode='html')
        return
        








########################################################################################################################
############################################### Start Developer Zone ###################################################
########################################################################################################################






# reset database 
async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Checking number of rows
        sql_row_count_command = "SELECT COUNT(*) FROM bookings" 
        ans = c.execute(sql_row_count_command)
        row_count = c.fetchone()[0]

        # delete all database records
        sql_del_all_command = "DELETE FROM bookings;"  
        del_all = c.execute(sql_del_all_command)
        conn.commit()

        # reset sequence for 'id' column in table
        sql_reset_seq_command = "DELETE FROM sqlite_sequence WHERE name = 'bookings';"
        reset_seq = c.execute(sql_reset_seq_command)
        conn.commit()

        await update.message.reply_text("Number of rows deleted: {}.\n\nTable sequence has been reset!".format(row_count))

    except Exception as e:
        print(e)
        await update.message.reply_text("<b>Something went wrong:</b>\n\n{}".format(e))
        return











# handle group messages
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hi, are you looking to make a car booking? Use /booking to start booking!'
    
    return 'Bot is responding correctly!'

# Logging 
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User (@{update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text: 
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else: 
        response: str = handle_response(text)

    print('BOT:', response)
    await update.message.reply_text(response)
        


# Insert rows for testing purposes 
async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sql_command = """INSERT INTO bookings (date, name, car_type) VALUES 
        ('01/01(8am-12pm)', 'lj', 'black'),
        ('02/01(8am-12pm)', 'tt', 'white'),
        ('03/01(8am-12pm)', 'jw', 'red');"""
        ans = c.execute(sql_command)
        conn.commit()

        await update.message.reply_text("Test rows inserted into 'bookings' table!")

    except Exception as e:
        print(e)
        await update.message.reply_text("Something when wrong. ERROR:{}".format(e))
        return






########################################################################################################################
################################################# End Developer Zone ###################################################
########################################################################################################################















# *** the lines of code below must be at the bottom in order for bot to work ***
if __name__ == '__main__':
    try: 
        

        print("Initializing Car-Booking Database")
        db_name = 'carbookingdb.db' 
        conn = sqlite3.connect(db_name, check_same_thread=False) # connecting to sqlite database
        c = conn.cursor() # to start using sqlite commands
        print("Connected to Car-Booking Database")

        sql_command = """CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date VARCHAR(200),
            name VARCHAR(200),
            car_type VARCHAR(200));"""
        c.execute(sql_command)
        print("All tables are ready")

        app = Application.builder().token(TOKEN).build() # telegram lib
        print("Bot Started!")

        # to enable commands (the text -> will trigger a command)
        app.add_handler(CommandHandler('test',test_command)) # can comment it out when all is working well 
        app.add_handler(CommandHandler('booking',booking_command))
        app.add_handler(CommandHandler('check',check_command))
        app.add_handler(CommandHandler('update',update_command))
        app.add_handler(CommandHandler('delete',delete_command))
        app.add_handler(CommandHandler('reset',reset_command))



        app.add_handler(MessageHandler(filters.TEXT, handle_message)) # telegram lib (to handle messages that bot is tagged in)
        print("Polling...")
        app.run_polling(poll_interval=1)

        client.run_until_disconnected()

    except Exception as error:
        print('Cause: {}'.format(error))