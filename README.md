# BADGE ASSIGNER PROJECT
- [BADGE ASSIGNER PROJECT](#badge-assigner-project)
  - [Purpose](#purpose)
  - [Settings](#settings)
  - [CLI Interaction](#cli-interaction)

## Purpose
Assigning badges on Bagdr platform can be tedious and time consuming. The aim of this project is to proportion a CLI to try to make it easier.

## Settings

1. Create a folder in `data` with the name of the intake
2. Create a json file inside with the following structure 
```
                        {"mail1": "name1",
                        "mail2": "name2,
                        ...}
```
3. Create `config.py` from `config_template.py`

## CLI Interaction

1. Run `main.py`
2. Introduce your password (according to the account in `config.py`)
3. Filter badges by name (Case Insensitive)
4. Insert badge ID to select one
5. You can select more than one and you can see the names of the badges in list
6. Choose which users are you sending the badge to
    
    - Option A: Insert emails one by one until you type "Q". CAUTION: If the email is not in the list it will raise an error
    - Option B: Select all the users in the list

7. The badges are sent