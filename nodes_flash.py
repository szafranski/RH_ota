from time import sleep
import os
import sys
from nodes_flash_common import main, disable_serial_on_the_node, com_init
from modules import clear_the_screen, Bcolors, logo_top, load_config
from nodes_update_old import main as old_flash_gpio


def nodes_addresses():
    """nodes I2C addresses - below: conversion to hex numbers required by SMBus module"""
    #  node    addr
    node1addr = 8
    node2addr = 10
    node3addr = 12
    node4addr = 14
    node5addr = 16
    node6addr = 18
    node7addr = 20
    node8addr = 22

    addr_list_int = (node1addr, node2addr, node3addr, node4addr,
                     node5addr, node6addr, node7addr, node8addr)

    addr_list_hex = [hex(item) for item in addr_list_int]

    addr_list = [str(item) for item in addr_list_hex]  # return addresses list as a tuple

    return addr_list


def reset_mate_node(smbus_import, addr, i2c_data, calculate_checksum):
    on, off, bus, sleep_amt = smbus_import

    reset_mate_node_command = i2c_data
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on sent")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, off)
    print("off sent")
    print("node reset in progress")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on sent")
    sleep(0.2)


def flash_blink(config):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i")


def flash_firmware(config):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/{config.firmware_version}/node_0.hex:i")


try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(config.gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)
    # ensures nothing is being reset during program's start
except ModuleNotFoundError:
    print("GPIO import - failed")
    sleep(2)


def logo_update(nodes_number):
    print("""
    #######################################################################
    #                                                                     #
    #{bold}{s}Flashing firmware onto {nodes_number} nodes - DONE{endc}{s}#
    #                                                                     #
    #              {bold}         Thank you!        {endc}                #
    #                                                                     #
    #######################################################################\n\n
    """.format(nodes_number=nodes_number, bold=Bcolors.BOLD_S, endc=Bcolors.ENDC_S, s=10 * ' '))


def disable_serial_on_the_node(addr, *i2c_data, calculate_checksum):
    disable_serial_data, disable_serial_on_the_node_command, bus = i2c_data
    disable_serial_data.append(calculate_checksum(disable_serial_data))
    bus.write_i2c_block_data(addr, disable_serial_on_the_node_command, disable_serial_data)


'''commands needed for interaction with nodes using GPIO pins '''


def gpio_reset_pin_low(gpio_reset_pin):
    GPIO.output(gpio_reset_pin, GPIO.LOW)
    sleep(0.1)


def gpio_reset_pin_high(gpio_reset_pin):
    GPIO.output(gpio_reset_pin, GPIO.HIGH)
    sleep(0.1)


def reset_gpio_pin(config):
    gpio_reset_pin_high(config.gpio_reset_pin)
    gpio_reset_pin_low(config.gpio_reset_pin)
    gpio_reset_pin_high(config.gpio_reset_pin)


def reset_mate_node(i2c_data, addr, calculate_checksum):
    on, off, sleep_amt, reset, bus = i2c_data()
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node, on)
    print("pin at default state - sent\n")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node, off)
    print("RESET command - sent")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node, on)
    print("pin at default state - sent\n")
    sleep(0.2)


def flash_firmware_onto_all_nodes_with_auto_addr(config, user, nodes_number):
    i = 1
    for i in range(1, nodes_number):
        disable_serial_on_all_nodes(config.nodes_number)
        reset_mate_node(config.gpio_reset_pin)
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{user}/RH-ota/firmware/i2c/{config.RH_version}/node_0.hex:i")
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{user}/RH-ota/firmware/i2c/{config.RH_version}/node_{i}.hex:i")
    print(f"\n\n\t\t\t\t{Bcolors.BOLD}Node {i} - flashed{Bcolors.ENDC}\n\n")
    sleep(1)


def flash_blink_onto_all_gnd_nodes(config, nodes_number):
    i = 1
    for i in range(1, nodes_number):
        disable_serial_on_all_nodes(nodes_number)
        reset_mate_node(config.gpio_reset_pin)
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/{config.user}\
        /RH-ota/firmware/blink.hex:i")
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i ")
    print(f"\n\n\t\t\t\t{Bcolors.BOLD}Node {i} - flashed{Bcolors.ENDC}\n\n")


def disable_serial_on_all_nodes(addr_list, nodes_number):
    for addr in addr_list:
        disable_serial_on_the_node(addr, bus=com_init())
        sleep(2)
        if addr_list.index(addr) == nodes_number:
            break


def flash_nodes_individually():
    def node_selection_menu(config):
        clear_the_screen()
        logo_top(config.linux_testing)
        sleep(0.05)
        flash_node_menu = """
                            {red}{bold}NODES MENU{endc}
                        {bold}
                1 - Flash node 1        5 - Flash node 5

                2 - Flash node 2        6 - Flash node 6

                3 - Flash node 3        7 - Flash node 7

                4 - Flash node 4        8 - Flash node 8
                        {yellow}
                    'e'- Exit to main menu{endc}
        """.format(bold=Bcolors.BOLD, red=Bcolors.RED, yellow=Bcolors.YELLOW, endc=Bcolors.ENDC)
        print(flash_node_menu)
        selection = input("""
                {bold}Which node do you want to program:{endc} """.format(bold=Bcolors.BOLD, endc=Bcolors.ENDC))
        if int(selection) in range(8):
            selected_node_number = selection
            return selected_node_number
        if selection == 'e':
            main()
        else:
            node_selection_menu(config)

    def specific_node_menu(config, selected_node_number):
        while True:
            print(f"""
            {Bcolors.BOLD}\n\t\t\tNode {str(selected_node_number)}  selected{Bcolors.ENDC}
                    Choose flashing type:\n{Bcolors.ENDC}
            1 - {Bcolors.GREEN}Node ground-auto selection firmware - recommended{Bcolors.ENDC}{Bcolors.BOLD}
            2 - Flashes 'Blink' on the node - only for test purposes
            a - Abort{Bcolors.ENDC}""")
            selection = input()
            if selection == '1':
                flashing_steps()
                print(f"{Bcolors.BOLD}\n\t Node {str(selected_node_number)} flashed\n{Bcolors.ENDC}")
                sleep(1.5)
                return
            if selection == '2':
                flashing_steps()
                print(f"{Bcolors.BOLD}\n\t Node {str(selected_node_number)} flashed\n{Bcolors.ENDC}")
                sleep(1.5)
                return
            if selection == 'a':
                specific_node_menu(config, selected_node_number)
            else:
                break


def first_flashing(config, nodes_number):
    def flash(port):
        for i in range(nodes_number):
            input("Hit any key and push reset key of next node after 1 second")
            sleep(0.2)
            disable_serial_on_all_nodes(nodes_number=config.nodes_number, addr_list=nodes_addresses()[1])
            os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/tty{port} -b 57600 -U \
                    flash:w:/home/{config.user}/RH-ota/firmware/{config.firmware_version}/node_0.hex:i")

    while True:
        port_sel = input("UART or USB flashing [default: UART]")
        if port_sel.lower() == 'uart':
            port_sel = 'S0'
            flash(port_sel)
        if port_sel.lower() == 'usb':
            port_sel = 'USB0'
            flash(port_sel)
        else:
            print("Type: 'UART' or 'USB' ")


def reset_gpio_state(config):
    clear_the_screen()
    logo_top(config.debug_mode)
    print("\n\n\n")
    os.system(f"echo {config.gpio_reset_pin} > /sys/class/GPIO/unexport")
    print("\n\n\t\t\tDONE\n\n")
    sleep(0.5)


def connection_test(config, nodes_num):
    for i in range(nodes_num):
        disable_serial_on_all_nodes(nodes_addresses()[1], config.nodes_number)
        os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
        sleep(0.2)


def flashing_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        sleep(0.05)
        node_menu = """\n
                            {bold}{underline}CHOOSE FLASHING TYPE:{endc}
    
                    {green}{bold}1 - Flash each node automatically - rec.{endc}
    
                    2 - Flash each node individually
    
                    3 - Flash first time
    
                    4 - Show I2C connected devices
    
                    5 - Flash using GPIO reset pins - obsolete
    
                    6 - Fix GPIO pin state
    
                    {yellow}e - Exit to main menu{endc}
            """.format(bold=Bcolors.BOLD, green=Bcolors.GREEN, yellow=Bcolors.YELLOW,
                       endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE)
        print(node_menu)
        sleep(0.1)
        selection = input()
        if selection == '1':
            flash_firmware_onto_all_nodes_with_auto_addr(config, nodes_addresses()[2])
            logo_update(config.nodes_number)
        if selection == '2':
            flash_nodes_individually()
            logo_update(config.nodes_number)
        if selection == '3':
            first_flashing(config, nodes_number=config.nodes_number)
            logo_update(nodes_number=config.nodes_number)
        if selection == '4':
            logo_top(config.debug_mode)
            os.system("i2cdetect - y 1")
        if selection == '5':
            old_flash_gpio()
        if selection == '6':
            reset_gpio_state(config.gpio_reset_pin)
        if selection == 'e':
            sys.exit()
        else:
            break


def main():
    com_init()
    config = load_config()
    flashing_menu(config)


if __name__ == "__main__":
    main()
