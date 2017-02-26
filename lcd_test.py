# _____ _____ _____ __ __ _____ _____
#|     |   __|     |  |  |     |     |
#|  |  |__   |  |  |_   _|  |  |  |  |
#|_____|_____|_____| |_| |_____|_____|
#
# Project Tutorial Url:http://osoyoo.com/?p=1031
#
import smbus
import time
import pyrebase
from collections import OrderedDict


# Add Firebase Info to script
config = {
  "apiKey": "AIzaSyCskxqP_KZuFwl6CtcPCXFlEuqwFNnSdI8",
  "authDomain": "west-score-keeper.firebaseapp.com",
  "databaseURL": "https://west-score-keeper.firebaseio.com",
  "storageBucket": "west-score-keeper.appspot.com",
  "messagingSenderId": "436613032037"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
  # Main program block

  # Test database
  #pi_game = db.child("currentGames").order_by_child("pi").equal_to(True).get() # this get the only game with true

  #pi_game_ordered_dict = pi_game.val()

  #pi_game_dict = dict(pi_game_ordered_dict)

  #print(pi_game_dict)

  #pi_game_key = list(pi_game_dict.keys())
  #print(pi_game_key[0])

  #print(pi_game_dict[pi_game_key[0]])

  #print(pi_game_dict[pi_game_key[0]]['team1Name'])
  #print(pi_game_dict[pi_game_key[0]]['team2Name'])

  # Store team names

  #team1Name = pi_game_dict[pi_game_key[0]]['team1Name']
  #team2Name = pi_game_dict[pi_game_key[0]]['team2Name']

  # var to store game info
  #game = ""

  def stream_handler(message):
	  print(message["event"])
	  print(message["path"])
    print(message["data"])

	  global game
    global current_state = db.child("currentGames").order_by_child("pi").equal_to(True).get()

	  game = message["data"]

	  print(game)

	  #game_info += 1

	  #print(game_info)


	  #print("function", cool_data)
	  #cool_data = message["data"]

	  #cool_data = "stuff test"
	  #print("cool_data ", cool_data)

	  #stream_data = message["data"]

	  #data = message["data"]
	  #get_keys = list(message["data"].keys())
	  #keys = list(message["data"].keys())
	  #key = get_keys[0]
	  #print(key)
	  #print(data[keys[0]]['team1Name'])
	  #print(data[keys[0]]['team2Name'])


  #team1Name = ""
  #team2Name = ""
  #game_info = 0



  pi_game = db.child("currentGames").order_by_child("pi").equal_to(True).stream(stream_handler)

  # Initialise display
  lcd_init()

  while True:

    #cool_data = "what"
    #print("test cool data", cool_data)

    # Send some test
    #lcd_string("Created by         <",LCD_LINE_1)
    #lcd_string("Osoyoo.com        <",LCD_LINE_2)

    #time.sleep(3)

    # Send some more text
    #lcd_string("> Tutorial Url:",LCD_LINE_1)
    #lcd_string("> http://osoyoo.com",LCD_LINE_2)

    #time.sleep(3)

    #lcd_string("Hey         <",LCD_LINE_1)
    #lcd_string("Test        <",LCD_LINE_2)

    #lcd_string(cool_data + "Hey         <", LCD_LINE_1)
    #lcd_string(cool_data, LCD_LINE_2)

    time.sleep(10)

    print("game_info", game)
    print("state", current_state)

    time.sleep(2)



if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
