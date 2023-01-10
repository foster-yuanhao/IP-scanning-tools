from wakeonlan import send_magic_packet
def wakeOn(device_name, ip_address, mac_address):
    print("Wake on Device: ", device_name)
    send_magic_packet(mac_address, ip_address)