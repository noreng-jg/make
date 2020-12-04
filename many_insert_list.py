from aux.random_generator import *
import argparse
import subprocess
import sys
import json
import copy

global path_skeleton
path_skeleton = 'make/collections_skeleton/'

class ReadFile:
    def __init__(self, filename):
        self.filename = filename

    def read_skeleton(self):
        try:
            with open(path_skeleton + self.filename) as f:
                item_skeleton = json.load(f)
                f.close()
                return item_skeleton 
        except:
            print("Error reading")

class Device(ReadFile):
    def __init__(self, tenant):
       self.filename = 'device.json'
       self.sk=self.read_skeleton()
       self.tenant = tenant 

    def gen_device(self):
        item_device = copy.deepcopy(self.sk)
        item_device["uid"] = rh(64) 
        item_device["name"] = r_name()
        item_device["status"] = rs() 
        item_device["info"]["id"] = ri()
        item_device["info"]["pretty_name"] = ri()
        item_device["identity"]["mac"] = r_mac()
        item_device["tenant_id"]=self.tenant
        return item_device

class Session(ReadFile):
    def __init__(self, tenant, devices_uids):
       self.filename = 'session.json'
       self.sk=self.read_skeleton()
       self.tenant = tenant
       self.devices_uids = devices_uids

    def gen_session(self):
        item_session = copy.deepcopy(self.sk)
        item_session["uid"] =rh(64) 
        item_session["device_uid"] = random.choice(self.devices_uids)
        item_session["tenant_id"] = self.tenant
        item_session["username"] = "user"
        item_session["ip_address"] = rip()
        item_session["started_at"] = rd()
        item_session["last_seen"] = rd()
        item_session["authenticated"] = rb()
        item_session["recorded"] = rb()
        return item_session

class FirewallRule(ReadFile):
    def __init__(self, tenant):
       self.filename = 'firewall.json'
       self.sk=self.read_skeleton()
       self.tenant = tenant

    def gen_firewall_rule(self):
        item_firewall = copy.deepcopy(self.sk)
        item_firewall["tenant_id"] = self.tenant 
        item_firewall["priority"] = rint()
        item_firewall["action"] = random.choice(["allow", "deny"])
        item_firewall["active"] = rb() 
        item_firewall["source_ip"] = rip() 
        item_firewall["username"] = "user" 
        item_firewall["hostname"] = rw(7)
        return item_firewall

class PublicKey(ReadFile):
    def __init__(self, tenant):
       self.filename = 'pub_key.json'
       self.sk=self.read_skeleton()
       self.tenant = tenant

    def gen_pub_key(self):
        item_pub_key = copy.deepcopy(self.sk)
        item_pub_key["data"] = rb64()
        item_pub_key["created_at"] = rd()
        item_pub_key["fingerprint"] = rf()
        item_pub_key["tenant_id"] = self.tenant 
        item_pub_key["name"] = rw(7)
        return item_pub_key

def insert_many_mongo(formated_array, collection_name):
    cmd='docker-compose exec -T mongo mongo main --quiet --eval \'db.{cn}.insertMany({json_arr})\''.format(json_arr=formated_array, cn=collection_name)
    sub = subprocess.call(cmd, shell=True)

def make_skeleton_array(callback, size):
    arr = []
    for i in range(size):
        arr.append(callback())
    print(arr)
    return arr

def format_json_array(arr):
    return json.dumps(arr)

def tenant_exists(tenant):
    cmd = 'docker-compose exec -T mongo mongo main --quiet --eval \'db.namespaces.find({{ "tenant_id" : "{ten}"}})\''.format(ten=tenant)
    sub = subprocess.Popen(cmd, shell=True, stdout= subprocess.PIPE)
    stdout, _ = sub.communicate() 

    try:
        if stdout != b'':
            return True
        else:
            return False
    except:
        print("Error searching tenant")


def main(**kwargs):
   tenant = kwargs['tenant']

   dev = Device(tenant)
   arr_devices=make_skeleton_array(dev.gen_device, kwargs['devices'])
   arr_dev_uids = [dev["uid"] for dev in arr_devices]
   insert_many_mongo(format_json_array(arr_devices), 'devices')

   ses = Session(tenant, arr_dev_uids)
   arr_sessions=make_skeleton_array(ses.gen_session, kwargs['sessions'])
   insert_many_mongo(format_json_array(arr_sessions), 'sessions')

   fr = FirewallRule(tenant)
   arr_fws = make_skeleton_array(fr.gen_firewall_rule, kwargs['firewall_rules'])
   insert_many_mongo(format_json_array(arr_fws), 'firewall_rules')

   pk = PublicKey(tenant)
   array_pks = make_skeleton_array(pk.gen_pub_key, kwargs['public_keys'])
   insert_many_mongo(format_json_array(array_pks), 'public_keys')

if __name__ == "__main__":

    usage = 'Usage: <tenant> <numbers_devices> <number_sessions> <number_firewall_rules> <number_pub_keys>'

    if len(sys.argv) < 5:
        print(usage)
        sys.exit()

    parser = argparse.ArgumentParser() 

    parser.add_argument("tenant", action='store', type=str)
    parser.add_argument("devices", type=int)
    parser.add_argument("sessions", type=int)
    parser.add_argument("firewall_rules", type=int)
    parser.add_argument("public_keys", type=int)

    args = parser.parse_args()

    try:
        if args.devices < 1 and args.sessions > 0:
            print("You need to insert at least one device to insert sessions")
            raise Exception("NoDevice4Session")

        if not tenant_exists(args.tenant):
            print("This tenant doesn\'t exist.")
            raise Exception("InexistantTenant")

        main(**args.__dict__)

    except:
        print("Something went wrong with the argument processing, please, try again")
        sys.exit()                            
