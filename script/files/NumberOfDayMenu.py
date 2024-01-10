import ConfigFile

def days_choice(auto=0):

    config_dict = ConfigFile.load_config()

    day_param = int(config_dict['day_param'])

    if auto == 1:
        return day_param

    while True:

        choice = ""
        print("Please provide number of days from now for DB import: (1-251) default: 1 ")

        choice = input()
        if choice == "":
            break
        else:
            choice = int(choice)

        if 1 <= choice <= 251:
            day_param = choice
            break


    return day_param
