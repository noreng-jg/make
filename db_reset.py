import subprocess
import re
from os import system

def delete_many_mongo(collections):
    try:
        for collection_name in collections:
            cmd='docker-compose exec -T mongo mongo main --quiet --eval \"db.{cn}.deleteMany({json})\"'.format(json='{}', cn=collection_name)
            print(cmd)
            sub = subprocess.call(cmd, shell=True)
    except:
        print("Error deleting collections")

def reset_database():
    cmd="docker-compose exec -T mongo mongo main --quiet --eval \"db.getCollectionNames()\""
    sub = subprocess.Popen(cmd, shell=True, stdout= subprocess.PIPE)
    stdout, _ = sub.communicate() 
    try:
        if stdout != b'':
            collections = [re.compile(r'\w+').search(s).group(0) for s in str(stdout.decode('ascii'))[3: -3].split(',')]
            collections.remove('migrations')
            delete_many_mongo(collections)
            print(collections)
    except:
        print("Error reseting")

if __name__ == "__main__":
    reset_database()
    system("clear")
