# Write your code here
from random import randint
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


# cur.execute("create table card("
#           "id integer PRIMARY KEY,"
#         "'number' text,"
#         "pin text,"
#         "balance Integer default 0);")


def start():
    print('''1. Create an account
2. Log into account
0. Exit''')
    i = int(input())
    if i == 0:
        print()
        print('Bye!')
        # cur.execute("drop table card")
        # conn.commit()
        exit()
    elif i == 1:
        create_acc()
    elif i == 2:
        acc_log()


def create_acc():
    iin = '400000'
    pin = ''
    count = 0
    for z in range(9):
        iin += str(randint(0, 9))
    for z in range(4):
        pin += str(randint(0, 9))
    res = 0
    co = 1
    for i in iin:
        if co % 2 != 0:
            i = int(i) * 2
            if i > 9:
                i -= 9
        res += int(i)
        co += 1
    while res % 10 != 0:
        res += 1
        count += 1
    iin += str(count)
    print()
    print('''Your card has been created
Your card number:''')
    print(iin)
    print("Your card PIN:")
    print(pin)
    print()
    cur.execute("Insert into card(number, pin) values({0}, {1});".format(iin, pin))
    conn.commit()
    start()


def auth(iin):
    print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
    i = int(input())
    bal = int(cur.execute('select balance from card where number = {0}'.format(iin)).fetchone()[0])
    if i == 5:
        print()
        print('You have successfully logged out!')
        print()
        start()
    elif i == 0:
        print()
        print('Bye!')
        # cur.execute("drop table card")
        # conn.commit()
        exit()
    elif i == 1:
        print()
        print("Balance: {0}".format(bal))
        print()
        auth(iin)
    elif i == 2:
        print()
        print('Enter income:')
        income = int(input())
        bal += income
        cur.execute("update card set balance = {0} where number = {1}".format(bal, str(iin)))
        conn.commit()
        print("Income was added!")
        auth(iin)
    elif i == 3:
        print('Enter card number:')
        card = input()
        if card == iin:
            print("You can't transfer money to the same account!")
            print()
            auth(iin)
        co = 1
        res = 0
        for i in card:
            if co % 2 != 0:
                i = int(i) * 2
                if i > 9:
                    i -= 9
            res += int(i)
            co += 1
        if res % 10 != 0:
            print('Probably you made a mistake in the card number. Please try again!')
            auth(iin)
        chech = cur.execute("select balance from card where number = {0}"
                            .format(card)).fetchone()
        if chech is not None:
            print('Enter how much money you want to transfer:')
            transfer = int(input())
            if transfer > bal:
                print('Not enough money!')
                print()
                auth(iin)
            else:
                print('Success!')
                print()
                cur.execute("update card set balance = {0} where number = {1}".format(bal - transfer, str(iin)))
                cur.execute(
                    "update card set balance = {0} where number = {1}".format(int(chech[0]) + transfer, str(card)))
                conn.commit()
        else:
            print("Such a card does not exist.")
            auth(iin)
    elif i == 4:
        print()
        print('The account has been closed!')
        print()
        cur.execute('Delete from card where number = {0}'.format(str(iin)))
        conn.commit()
        start()


def acc_log():
    print()
    print('Enter your card number:')
    card = input()
    print('Enter your PIN:')
    pin = input()
    pina = cur.execute("select pin from card where number = {0}"
                       .format(card)).fetchone()
    if pina is not None and pin == pina[0]:
        print()
        print("You have successfully logged in!")
        print()
        auth(card)
    else:
        print()
        print('Wrong card number or PIN!')
        print()
        start()


start()
