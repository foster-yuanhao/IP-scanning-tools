from wakeonlan import send_magic_packet
def wakeOn(device_name, mac_address):
    print("Wake on Device: ", device_name)
    send_magic_packet(mac_address)
