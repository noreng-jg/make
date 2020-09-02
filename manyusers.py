import subprocess
import string
import random

rw = lambda n:''.join(random.choice(string.ascii_lowercase) for l in range(n))

def enterUsers(number):
    for i in range(number):
        cmd='./bin/add-user {name} senha {e1}@{e2}.com'.format(name=rw(8), e1=rw(5), e2=rw(4)) 
        execute=subprocess.call(cmd, shell=True)

def main():
    nusers= input('How many users?:')
    try:
        number = int(nusers)
        enterUsers(number)
    except ValueError:
        print("\nYou should enter a value\n")


if __name__ == "__main__":
    main()
