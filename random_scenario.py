import subprocess
import argparse
import sys
import random
from aux.random_generator import *

def main(n_users, n_namespaces):
  fake_input = [n_users, n_namespaces]

  for ns in range(n_namespaces):
    random_list_data = [int(rn(2, 100)) for i in range(4)]
    fake_input.extend(random_list_data)
    owner = int(rn(1, n_users))
    fake_input.append(owner)
    possible_members = [usr for usr in range(1, n_users+1) if usr != owner]
    random_choice_number = random.randint(1, len(possible_members))
    members = random.sample(possible_members, random_choice_number)
    fake_input.extend(members)    
    fake_input.append('x')

  with open(f"make/scenarios/{n_users}_users&{n_namespaces}_nss", 'w') as f:
    for fi in fake_input:
      f.writelines(str(fi)+ "\n")
  f.close()

if __name__ == "__main__":
  usage = "Usage <number_users> <number_namespaces>"
  if len(sys.argv) != 3:
    print(usage)
    sys.exit()
  
  parser= argparse.ArgumentParser()

  parser.add_argument("users", type=int)
  parser.add_argument("namespaces", type=int)

  args = parser.parse_args()

  main(args.users, args.namespaces)
