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

## Remove snapshots from ui unit tests

Enter the `ui` folder and run the following:

```bash
../make/unit-test/ui_remove_snaps.sh
```
