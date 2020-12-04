# Make 

Development scripts for shellhub. 

## Installation

In shellhub root folder clone the repo:

```bash
git clone https://github.com/noreng-jg/make.git

```

## Add many users

```
python3 make/manyusers.py
```

## Add many items to list

This script will add many devices, sessions, firewall rules and public keys, according to numbers defined.

```
python3 make/many_insert_list.py <tenant> <number_devices> <number_sessions> <number_firewall_rules> <number_public_keys>
```

## Add multiple users and cascading namespaces with items 

This script will create multiple users with multiple namespaces according to values of choice, also lists defined in `make/many_insert_list.py` will be asked to be entered iteratively.

```
python3 make/cascade_insertion.py <hashed_password>
```

if you don't have a `<hashed_password>` you can run:

```
./make/cascade_insertion.sh <password>
```

All the users generated will have the same password defined.

The script might take a while to run and when it's finished a scenario file containing the iterative captured input will be generated inside the `scenarios/` folder for future insertion reference, according to the quantity of users and namespaces inserted. 

To run a specific scenario you can procced as follows:

```
./make/load_scenario.sh
```

There will be asked to define a password and then to choose one of the captured files, hit `<TAB>` to find them.


## Remove snapshots from ui unit tests

Enter the `ui` folder and run the following:

```bash
../make/unit-test/ui_remove_snaps.sh
```
