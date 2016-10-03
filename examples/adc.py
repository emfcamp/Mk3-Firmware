#This example shows how to use the ADC, and how to 
# measure the internal reference to get a more accurate
# ADC reading
import pyb

# set adc resolution to 12 bits
adca = pyb.ADCAll(12)

# channel 17 is the internal 1.21V reference
ref_reading = adca.read_channel(17)  

# channel 0 (PA0) is the Vbus/2 connection
usb_reading = adca.read_channel(0)   

# Use the internal reference to calculate the supply voltage
# The supply voltage is used as the ADC reference and is not exactly 3.3V
supply_voltage = 4095/ref_reading*1.21 

print("supply voltage: " + str(supply_voltage) + "\n")

# now calculate the USB voltage
usb_voltage = usb_reading/4095*supply_voltage*2

print("usb_voltage: " + str(usb_voltage) + "\n")
