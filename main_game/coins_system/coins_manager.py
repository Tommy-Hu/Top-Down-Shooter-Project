import os

# Controls the coins. IO.

coins_count = 0
if os.path.exists("coins.dat"):
    file = open("coins.dat", "rb")  # rb stands for Read Binary(So that you(players) cannot understand it)
    coins_count = int(file.read())
    file.close()


def write_to_file():
    file = open("coins.dat", "wb")  # wb stands for Write Binary(So that you(players) cannot understand it)
    file.write(str(coins_count))
    file.close()
