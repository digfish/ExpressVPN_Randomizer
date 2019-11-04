#!/usr/bin/env python3

import subprocess, re, random, datetime
PROC_EXEC = 'expressvpn'
MAX_MINUTES = 59


def proc_execoutput(options):
    express_proc = subprocess.Popen([PROC_EXEC] + options, stdout=subprocess.PIPE)
    express_output = express_proc.communicate()
    return express_output

def statusCheck():
    """
    This function will run a status check on your expressvpn service to see if you are already connected.  You must be disconnected for this program to work. 
    """
    express_output = proc_execoutput(['status'])
    status = express_output[0].decode("utf-8").strip()

    print("status",status)

    if status == "Not connected":
        return True
    else:
        disconnect = input("You are currently connected to expressvpn already.  Would you like to disconnect and continue? [y/n]: ").lower()
        
        if disconnect == "y":
            subprocess.call([PROC_EXEC, "disconnect"])
            return True
        
        elif disconnect == "n":
            print("You have chosen not to disconnect from your current expressvpn session.  Exiting program...")
            exit()

def getCountries():
    """
    This function will return a list of the current countries with available servers for your expressvpn account.
    """
    express_output = proc_execoutput(['list','all'])
    countries = re.split("\n", express_output[0].decode("utf-8"))
    country_codes = []
    for country in countries:
        countries_tokens = re.split("\\s+",country)
        if (countries_tokens[0] == ''):
         continue
        country_codes.append(countries_tokens[0])

    country_codes = country_codes[2:]
    return country_codes

def chooseRandom(country_list):
    """
    This function will randomly choose a country out of the available countries list.
    """
    return country_list[random.randrange(0, len(country_list))]

def logIn(random_country):
    """
    This function will take the randomly chosen country and attempt to log in to expressvpn using that country.
    """
    print("{} has been selected as the random country.".format(random_country))
    
    subprocess.call([PROC_EXEC, "connect", random_country])

def main():
    try:
        continuous_mode = input("Would you like to have this script continuously run and log in to random servers at random time intervals? [y/n]: ").lower()
        if continuous_mode == "y":
            try:
                randomized_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randrange(1,MAX_MINUTES))
                while True:
                    if datetime.datetime.now() >= randomized_time:
                        express_output = proc_execoutput(['status'])
                        status = express_output[0].decode("utf-8").strip()
                        print ("Status",status)
                        if status != "Not connected":
                            subprocess.call([PROC_EXEC, "disconnect"])

                        logIn(chooseRandom(getCountries()))
                        randomized_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randrange(1,59))
            
            except Exception as error:
                print("Error: {}".format(str(error)))

        elif continuous_mode == "n":
            print("This script will only run this one time.  If you want to choose another server at random then you will need to run the script again.")
            
            if statusCheck():
                logIn(chooseRandom(getCountries()))

    except Exception as error:
        print("Error: {}".format(str(error)))

if __name__ == "__main__":
    main()




