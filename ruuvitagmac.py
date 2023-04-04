from ruuvitag_sensor.ruuvi import RuuviTagSensor

def handle_data(found_data):
    mac = found_data[0]
    print(f"MAC address: {mac}")

RuuviTagSensor.get_data(handle_data)
