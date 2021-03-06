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
./make/cascade_insertion.sh
```

All the users generated will have the same password `senha`.

The script might take a while to run and when it's finished a scenario file containing the iterative captured input will be generated inside the `scenarios/` folder for future insertion reference, according to the quantity of users and namespaces inserted. 

To run a specific scenario you can procced as follows:

```
./make/load_scenario.sh
```

You may also generate a random scenario by specifying the numbers of users and namespaces:

```
python3 make/random_scenario.py
```

Choose one of the captured files by hitting `<TAB>`


## Remove snapshots from ui unit tests

Enter the `ui` folder and run the following:

```bash
../make/unit-test/ui_remove_snaps.sh
```
