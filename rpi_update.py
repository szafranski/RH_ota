import os
import glob
from pathlib import Path
from time import sleep
from conf_wizard_rh import conf_rh
from modules import clear_the_screen, Bcolors, triangle_image_show, internet_check, load_ota_sys_markers, \
    write_ota_sys_markers, load_config, server_start


def check_preferred_rh_version(config):

    stable_release_name = '2.3.2'  # declare last stable release name here

    beta_release_name = '2.3.0-beta.3'  # declare last beta release name here

    if config.rh_version == 'stable':
        server_version = stable_release_name
    elif config.rh_version == 'beta':
        server_version = beta_release_name
    elif config.rh_version == 'master':
        server_version = 'master'
    else:  # in case of 'custom' version selected in wizard
        server_version = config.rh_version

    return server_version


# TODO I would like to move th tags out of being hard-coded here.
# Maybe get a list of tags and ask user to select from list
# or automatically figure out the newest non-beta tag?


def get_rotorhazard_server_version(config):
    server_py = Path(f"/home/{config.user}/RotorHazard/src/server/server.py")
    server_version_name = ''
    server_installed_flag = False
    if server_py.exists():
        with open(server_py, 'r') as open_file:
            for line in open_file:
                if line.startswith('RELEASE_VERSION'):
                    # RELEASE_VERSION = "2.2.0 (dev 1)" # Public release version code
                    server_version_name = line.strip().split('=')[1].strip()
                    server_version_name = server_version_name.strip().split('#')[0].replace('"', '')
                    colored_server_version_name = f"{Bcolors.GREEN}{server_version_name}{Bcolors.ENDC} "
                    server_installed_flag = True
                    break
    else:
        server_version_name = f'{Bcolors.YELLOW}{Bcolors.UNDERLINE}installation not found{Bcolors.ENDC}'
        server_installed_flag = False
    return server_installed_flag, server_version_name, colored_server_version_name


def check_rotorhazard_config_status(config):
    if os.path.exists(f"/home/{config.user}/RotorHazard/src/server/config.json"):
        config_soft = f"{Bcolors.GREEN}configured{Bcolors.ENDC} 👍"
        config_flag = True
    else:
        config_soft = f"{Bcolors.YELLOW}{Bcolors.UNDERLINE}not configured{Bcolors.ENDC} 👎👎👎"
        config_flag = False
    return config_soft, config_flag


def show_update_completed():
    update_completed = """\n\n
        #################################################
        ##                                             ##
        ##{bold}{green}Update completed! {thumbs}{endc}##
        ##                                             ##
        #################################################
                """.format(thumbs="👍👍👍  ", bold=Bcolors.BOLD_S,
                           endc=Bcolors.ENDC_S, green=Bcolors.GREEN_S)
    return update_completed


def end_update(config, server_configured_flag, server_installed_flag):
    if not server_configured_flag and server_installed_flag:
        configure = f"{Bcolors.GREEN}c - Configure RotorHazard now{Bcolors.ENDC}"
    else:
        configure = "c - Reconfigure RotorHazard server"
    while True:
        print(show_update_completed())
        clearing_color = ''
        old_installations_were_found = False
        old_rh_directories_found = glob.glob('.././RotorHazard_*')
        if old_rh_directories_found:
            clearing_color = Bcolors.GREEN
            old_installations_were_found = True
        print(f"""
                {configure}
    
                r - Reboot - recommended, not a must
                
                s - Start RH server now {clearing_color}
                
                o - Clear old RotorHazard installations{Bcolors.YELLOW}
                
                e - Exit now{Bcolors.ENDC}""")
        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        elif selection == 's':
            os.chdir(f"/home/{config.user}/RH-ota")
            server_start()
        elif selection == 'o':
            os.system("rm -rf ~/RotorHazard_*")
            if old_installations_were_found:
                print("\n\t\t -- old RH installations cleaned --")
            else:
                print("\n\t\t -- no more old RH installations --")
            sleep(2)
            clear_the_screen()
        elif selection == 'c':
            conf_rh()
        elif selection == 'e':
            return


def end_installation(config):
    while True:
        print(f"""
    
            {Bcolors.GREEN}
            c - Configure RH server now - recommended {Bcolors.ENDC}
            
            r - Reboot - recommended after configuring
            
            s - Start RH server now{Bcolors.YELLOW}
            
            e - Exit now{Bcolors.ENDC}""")

        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        elif selection == 'e':
            return
        elif selection == 'c':
            conf_rh()
            break
        elif selection == 's':
            clear_the_screen()
            os.chdir(f"/home/{config.user}/RH-ota")
            os.system("./scripts/server_start.sh")


def installation(conf_allowed, config):
    ota_config = load_ota_sys_markers(config.user)
    os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &") if not config.debug_mode else None
    clear_the_screen()
    internet_flag = internet_check()
    if not internet_flag:
        print(f"\n\t{Bcolors.RED}Looks like you don't have internet connection. Installation canceled.{Bcolors.ENDC}")
        sleep(2)
    else:
        print(f"\n\t\t\t{Bcolors.GREEN}Internet connection - OK{Bcolors.ENDC}")
        sleep(2)
        clear_the_screen()
        print(f"\n\n\t{Bcolors.BOLD}Installation process has been started - please wait...{Bcolors.ENDC}\n\n")
        installation_completed = """
        
        
            ######################################################
            ##                                                  ##
            ##{bold}{green}Installation completed {thumbs}{endc}##
            ##                                                  ##
            ######################################################


        After rebooting please check by typing 'sudo raspi-config' 
        if I2C, SPI and SSH protocols are active.
                    """.format(thumbs="👍👍👍  ", bold=Bcolors.BOLD_S,
                               endc=Bcolors.ENDC_S, green=Bcolors.GREEN_S)

        os.system("./scripts/sys_conf.sh all") if conf_allowed else None
        ota_config.sys_config_done = True
        os.system("./scripts/sys_conf.sh uart") if not ota_config.uart_support_added else None
        ota_config.uart_support_added = True
        # UART enabling added here so user won't have to reboot Pi again after doing it in Features Menu
        write_ota_sys_markers(ota_config, config.user)
        os.system(f"./scripts/install_rh.sh {config.user} {check_preferred_rh_version(config)}")
        input("press Enter to continue.")
        clear_the_screen()
        print(installation_completed)
        os.system("sudo chmod 777 -R ~/RotorHazard")
        end_installation(config.user)


def update(config):
    os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &") if not config.debug_mode else None
    internet_flag = internet_check()
    if not internet_flag:
        print(f"\n\t{Bcolors.RED}Looks like you don't have internet connection. Update canceled.{Bcolors.ENDC}")
        sleep(2)
    else:
        print(f"\n\t\t\t{Bcolors.GREEN}Internet connection - OK{Bcolors.ENDC}")
        sleep(2)
        clear_the_screen()
        if not os.path.exists(f"/home/{config.user}/RotorHazard"):
            print(f"""{Bcolors.BOLD}

    Looks like you don't have RotorHazard server software installed for now. 

    If so please install your server software first or you won't be able to use the timer.{Bcolors.ENDC}{Bcolors.GREEN} 
          
        
        i - Install the software - recommended{Bcolors.ENDC}

        a - Abort both  {Bcolors.ENDC}

""")
            selection = input()
            if selection == 'i':
                conf_allowed = True
                installation(conf_allowed, config)
            elif selection == 'a':
                clear_the_screen()
                return
            else:
                return
        else:
            clear_the_screen()
            print(f"\n\n\t{Bcolors.BOLD}Updating existing installation - please wait...{Bcolors.ENDC}\n\n")
            os.system(f"./scripts/update_rh.sh {config.user} {check_preferred_rh_version(config)}")
            config_flag, config_soft = check_rotorhazard_config_status(config)
            server_installed_flag, server_version_name = get_rotorhazard_server_version(config)
            os.system("sudo chmod -R 777 ~/RotorHazard")
            end_update(config, config_flag, server_installed_flag)


def main_window(config):
    while True:
        rh_config_text, rh_config_flag = check_rotorhazard_config_status(config)
        clear_the_screen()
        server_installed_flag, server_version_name, colored_server_version_name = get_rotorhazard_server_version(config)
        ota_config = load_ota_sys_markers(config.user)
        sys_configured_flag = ota_config.sys_config_done
        sleep(0.1)
        welcome_text = """
        \n\n{red} {bold}
        AUTOMATIC UPDATE AND INSTALLATION OF ROTORHAZARD RACING TIMER SOFTWARE
            {endc}{bold}
        You can automatically install and update RotorHazard timing software. 
        Additional dependencies and libraries also will be installed or updated.
        Current database, configs and custom bitmaps will stay on their place.
        Source of the software is set to {underline}{blue}{server_version}{endc}{bold} version from the official 
        RotorHazard repository.
         
        Please update this (OTA) software, before updating RotorHazard server.
        Also make sure that you are logged as user {underline}{blue}{user}{endc}{bold} and that you don't have 
        other terminal windows opened - especially in RotorHazard directory.
        
        You can change those in configuration wizard in Main Menu.
        
        Server installed right now: {server} {bold}
        
        RotorHazard configuration state: {config_soft}
            
            """.format(bold=Bcolors.BOLD, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC, blue=Bcolors.BLUE,
                       yellow=Bcolors.YELLOW, red=Bcolors.RED, orange=Bcolors.ORANGE, server_version=config.rh_version,
                       user=config.user, config_soft=rh_config_text, server=colored_server_version_name)
        print(welcome_text)
        if not rh_config_flag and server_installed_flag:
            configure = f"{Bcolors.GREEN}c - Configure RotorHazard server{Bcolors.ENDC}"
        elif not rh_config_flag and not server_installed_flag:
            configure = "c - Reconfigure RotorHazard server"
        else:
            configure = "c - Configure RotorHazard server"
        if not server_installed_flag:
            install = f"{Bcolors.GREEN}i - Install software from scratch{Bcolors.ENDC}"
        else:
            install = "i - Install software from scratch"
        print("""
                    {install}
                    
                    {configure}
                    
                    u - Update existing installation 
                    
                    s - Start RotorHazard server now{yellow}
                        
                    e - Exit to Main Menu{endc}
                    
                """.format(yellow=Bcolors.YELLOW, endc=Bcolors.ENDC, configure=configure, install=install))
        selection = input()
        if selection == 'c':
            if server_installed_flag:
                conf_rh()
            else:
                print("Please install RH server before configuring.")
                sleep(2)
        elif selection == 's':
            if server_installed_flag:
                server_start()
            else:
                print("Please install the RotorHazard server first")
                sleep(2)
        elif selection == 'i':
            # rh_found_flag = os.path.exists(f"/home/{config.user}/RotorHazard")
            if sys_configured_flag:
                clear_the_screen()
                already_installed_prompt = """{bold}
                
        Looks like you already have your system configured.{endc}{bold}
        
        If so, please perform installation without sys. config.
                
                            
     {green}i - Force installation without sys. config. {endc}{bold}
            
            c - Force installation and system config. {yellow}
            
            a - Abort both {endc}
            """.format(bold=Bcolors.BOLD, endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE,
                       yellow=Bcolors.YELLOW, green=Bcolors.GREEN_S)
                print(already_installed_prompt)
                selection = input()
                if selection == 'i':
                    conf_allowed = False
                    installation(conf_allowed, config)
                elif selection == 'c':
                    confirm_valid_options = ['y', 'yes', 'n', 'no', 'abort', 'a']
                    while True:
                        confirm = input("\n\t\tAre you sure? [yes/abort]\t").strip()
                        if confirm in confirm_valid_options:
                            break
                        else:
                            print("\ntoo big fingers :( wrong command. try again! :)")
                    if confirm == 'y' or confirm == 'yes':
                        conf_allowed = True
                        installation(conf_allowed, config)
                    elif confirm in ['n', 'no', 'abort', 'a']:
                        pass
                elif selection == 'a':
                    clear_the_screen()
                    triangle_image_show()
                    sleep(0.5)
                    break
            else:
                conf_allowed = True
                installation(conf_allowed, config)
        elif selection == 'u':
            update(config)
        elif selection == 'e':
            clear_the_screen()
            os.chdir(f"/home/{config.user}/RH-ota")
            triangle_image_show()
            sleep(0.3)
            break


def main():
    config = load_config()
    main_window(config)


if __name__ == "__main__":
    main()
