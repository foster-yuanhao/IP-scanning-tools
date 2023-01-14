from wakeonlan import send_magic_packet
#Wake on device in the LAN
def wakeOn(device_name, mac_address):
    print("Wake on Device: ", device_name)
    send_magic_packet(mac_address)  #send magic packet to the device by using its mac address
