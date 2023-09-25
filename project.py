import psycopg2
import time
import pygame


# Database parameters
db_params={

    'host':'localhost',
    'dbname':'inventory',
    'user':'postgres',
    'password':'Admin',

}

# Initialize total bill
total_bill=0

# connect to the postgresql database
conn= None
try:
    print('Connecting to the Postgresql database...')
    conn= psycopg2.connect(**db_params)

    # create a cursor
    cur = conn.cursor()

    # execute a statement 
    # print('Postgresql database version: ')
    # cur.execute('SELECT version()')

    # display the Postgresql database server version
    # db_version = cur.fetchone()
    # print(db_version)
    while True:
        # SImulate RFID scanning(Replace with actual RFID READING CODE)
        scanned_tag =input('Enter the RFID UID code(or "q" to quit): ').strip()

        # check if the user wants to quit
        if scanned_tag.lower() =='q':
            break
        
        # check if the scanned_tag is in the database
        cur.execute(f'SELECT items, price FROM {scanned_tag}')
        item =cur.fetchone()

        if item:
            items, price =item 

            # initialize pygame
            pygame.init

            # TFT screen dimensions
            screen_width=500
            screen_height=500

            # create a pygame screen
            screen= pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Bill Display")

            # colors
            white =(255,255,255)
            black=(0,0,0)
            
            # Fonts
            font=pygame.font.Font(None, 36)
            
            running=True
            while running:
                for event in pygame.event.get():
                    if event.ype ==pygame.QUIT:
                        running=False
                # clear the screen
                screen.fill(white)
    # close the communication with the database
    cur.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(f'Please be patient as we check our {error}')

finally:

    if conn is not None:
        conn.close()
        print('Database connection terminated')
    
   
    