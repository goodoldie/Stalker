import subprocess

interface = input("Enter the Interface > ")
new_mac = input("Enter the New MAC > ")
print("Changing MAC address for " + interface + " to " + new_mac)

subprocess.run(["sudo", "ifconfig", interface, "down"])
subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
subprocess.run(["sudo", "ifconfig", interface, "up"])

print("******* MAC address successfully changed *******")
subprocess.run("sudo ifconfig " + interface, shell=True)
