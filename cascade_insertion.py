import subprocess
import sys
import string
import random
import re
from aux.random_generator import *
from aux.ext_bytes import extract_ids_from_bytes_stdout 
from os import system
import json
import copy
import argparse

captured_input=[]

def run_many_insert(tenant, list_sizes):
    cmd='python3 make/many_insert_list.py {ten} {0} {1} {2} {3}'.format(*list_sizes, ten=tenant)
    sub = subprocess.call(cmd, shell=True)

def insert_many_mongo_output(formated_array, collection_name):
    cmd='docker-compose exec -T mongo mongo main --quiet --eval \'db.{cn}.insertMany({json_arr})\''.format(json_arr=formated_array, cn=collection_name)
    sub = subprocess.Popen(cmd, shell=True, stdout= subprocess.PIPE)
    stdout, _ = sub.communicate() 
    try:
        if stdout != b'':
            print(stdout)
            return extract_ids_from_bytes_stdout(stdout.decode('ascii'))
        else:
            return []
    except:
        print("Error inserting")

def insert_many_mongo(formated_array, collection_name):
    cmd='docker-compose exec -T mongo mongo main --quiet --eval \'db.{cn}.insertMany({json_arr})\''.format(json_arr=formated_array, cn=collection_name)
    sub = subprocess.call(cmd, shell=True)

def enter_namespaces(number_nss, users, users_ids):
    namespaces = []
    list_items = []
    tenants = []
    for i in range(number_nss):
        current_members = []
        current_member_ids = []
        max_members_length = len(users) - 1
        system('clear')
        print(f'For namespace number {i+1}: ')
        while (True):
            print('Enter quantity of items to this namespace: ')
            devices= input('Devices: ')
            sessions = input('Sessions: ')
            firewall = input('Firewall Rules: ')
            pub_keys = input('Pub Keys: ')
            items = [devices, sessions, firewall, pub_keys]
            captured_input.extend(items)
            try:
                items = [int(item) for item in items]
                print('The items quantities were inserted: ')
                break
            except ValueError:
                print('\nYou should enter number for the field\n')
        #input
        print(f'Namespace: {i+1} -> : Enter the owner of this namespace: ')
        #same line in tuple format
        members = users.copy()
        tenant = rt() 
        tenants.append(tenant)
        while (True):
            usernames = []
            user_ids = []
            for j in range(len(users)):
                usernames.append(users[j]['username'])
                user_ids.append(users_ids[j])

            print('Users available -> ' + list_format(usernames))
            owner = input('Owner name : ')
            captured_input.append(owner)
            if (owner.isnumeric()):
                owner = 'user'+owner
            print(owner)
            print(usernames)
            try:
                index_owner = usernames.index(owner)
                owner_id= user_ids[index_owner]
                current_member_ids.append(owner_id)
                usernames.remove(owner)
                user_ids.remove(owner_id)
                break
            except ValueError:
                print('Invalid user, try again')

        while (True):
            if (max_members_length > 0) :
                system('clear')
                print(f'Namespace: {i+1} -> Enter new member ')
                print('\n---- Or x to stop adding members ----\n')
                print('Current members: ', current_members)
                print('Owner: ', owner)
                print('Members available -> ' + list_format(usernames))
                new_member = input('[number or username] Member name: ')
                captured_input.append(new_member)
                if (new_member == 'x'):
                    break
                elif (new_member.isnumeric()):
                    new_member = 'user'+new_member
                    print(max_members_length)
                    print('deu certo')
                try:
                    ##add ns
                    print('User added to namespace')

                    index_member=usernames.index(new_member)
                    usernames.remove(new_member)
                    current_members.append(new_member)
                    current_member_ids.append(user_ids[index_member])
                    user_ids.remove(user_ids[index_member])
                    print(user_ids)
                    print(current_member_ids)
                    print(index_member)
                except:
                    print('Error, couldn\'t find the user')
                max_members_length -= 1
            else:
                break
        namespaces.append({"name": f"namespace{i+1}", "owner": owner_id, "tenant_id": tenant, "members": current_member_ids, "settings": {"session_record": True}})
        list_items.append(items)
        print(namespaces, list_items)
    insert_many_mongo(json.dumps(namespaces), 'namespaces')
    print(tenants)
    for i in range(len(namespaces)):
        run_many_insert(tenants[i], list_items[i])
        print(i, len(namespaces))
    print(namespaces)

def enterUsers(number, password):
    users= []
    user_names= []
    for i in range(number):
        users.append({"name": f"user{i+1}", "username": f"user{i+1}", "password": password, "email": f"user{i+1}@email.com"})
        user_names.append(f"user{i+1}")
    user_ids = insert_many_mongo_output(json.dumps(users), 'users')
    return users, user_ids 

list_format = lambda list : ' [ ' + ' '.join([item for item in list]) + ' ] '

def main(password):
    try:
        nusers= input('How many users?: ')
        captured_input.append(nusers)
        numberusers = int(nusers)
        users, user_ids = enterUsers(numberusers, password)
        print('The users added')

        while (True):
            try:
                system('clear')
                n_namespaces = input('How many namespaces? :')
                captured_input.append(n_namespaces)
                number_namespaces = int(n_namespaces)
                namespaces = enter_namespaces(number_namespaces, users, user_ids)
                break
            except ValueError:
                print("\nYou should enter a value\n")
            except KeyboardInterrupt:
                print("\nLeaving ...\n")
                break
    except KeyboardInterrupt:
        print("\nLeaving ...\n")
    except ValueError:
        print("\nYou should enter a value\n")


if __name__ == "__main__":
    usage = 'Usage: <hashed_password>'
    if len(sys.argv) != 2:
        print(usage)
        sys.exit()
    parser = argparse.ArgumentParser()
    parser.add_argument("password", type=str)

    args = parser.parse_args()

    main(args.password)
    try:
        f=open(f"make/scenarios/{captured_input[0]}_users&{captured_input[1]}_nss", 'w')
        f.write("\n".join(captured_input))
        f.close()
    except:
        print('Something wrong happened')
