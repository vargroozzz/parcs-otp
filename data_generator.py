import random
import string
import sys

if __name__ == '__main__':
    file = open("data_sample" + str(sys.argv[1]), "at")
    letters = string.ascii_letters
    file.write('0x76b061aa1bdb0d006a745579e9f26c5e\n')

    for i in range(int(sys.argv[1])):
        file.write(''.join(random.choice(letters)))

    file.close()
