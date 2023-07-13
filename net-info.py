import subprocess
from tabulate import tabulate

'''
Using the subprocess module the function returns the STDOUT of the console for any Console Command.
'''
def console(paras):
    return subprocess.Popen(paras, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE ,shell=True).communicate()

# Run the ipconfig /all command and store the output
infosystem_output = console(['systeminfo'])[0].decode('IBM866',errors='ignore')

# Split the infosystem output into a list of lines
infosystem_lines = infosystem_output.split('\n')

# Initialize a list to store the common NIC names
common_names = []

# Loop through the lines of the infosystem output
for infosystem_line in infosystem_lines:
  # Check if the line contains the word "Name"
  if 'Connection Name' in infosystem_line:
    # Split the line into words and get the second word (the NIC name)
    common_names.append(infosystem_line.split(':')[1].strip())
    
# Run the ipconfig /all command and store the output
ipconfig_output = console(['ipconfig', '/all'])[0].decode('IBM866',errors='ignore')

# Create a list of lists containing the information we want to include in the table
rows = []
headers = ['Name', 'State', 'MAC address', 'DHCP','IPv4 address']
nic_info = []
#Flag for checking if the name of the adapter is valid
valid_adapter = True

for line in ipconfig_output.split('\n'):
    #Checks for a new adapter also crosschecks with the systemifno information 
    if 'Ethernet adapter' in line or 'Wireless LAN adapter' in line or 'adapter' in line:
        # This is the beginning of a new NIC, so save the information from the previous NIC
        if nic_info:
            #Save only if adapter is valid 
            if valid_adapter:
                rows.append(nic_info)
        #Check if the new adapter is valid
        if line.split(':')[0].split('adapter')[1].strip() in common_names:
            valid_adapter = True
        else:
            valid_adapter = False
        
        #Reset nic_info 
        nic_info = []
        
        # Extract the name of the NIC
        nic_info.append(line.split(':')[0].split('adapter')[1].strip().replace('?',''))
        #Default value Connected, if Media State is not present the State is Connected
        nic_info.append('Connected')

    elif 'Media State' in line:
        # If Media State present assume not connected 
        if line.split(':')[1].strip() == 'Media disconnected':
            nic_info[1] = ('Not connected')
    elif 'Physical Address' in line:
        # Extract the MAC address of the NIC
        nic_info.append(line.split(':')[1].strip())
    elif 'DHCP Enabled' in line:
    # Extract the DHCP status of the NIC
        nic_info.append(line.split(':')[1].strip())
    elif 'IPv4 Address' in line:
    # Extract the IPv4 address of the NIC
        nic_info.append(line.split(':')[1].split('(')[0].strip())

# Add the final NIC information to the list
rows.append(nic_info)

# Print the table using the tabulate module
print('computer information: NICs')
print('**************************')
print(tabulate(rows, headers=headers, tablefmt='fancy_grid'))

# Find the line containing the IPv4 address
ipv4_lines = [line for line in ipconfig_output.split('\n') if 'IPv4 Address' in line]

# Extract the IPv4 addresses from the line
ipv4_addresses = ', '.join([ipv4_line.split(':')[1].split('(')[0].strip() for ipv4_line in ipv4_lines])
# Find the line containing the Gateway address
gateway_lines = [line for line in ipconfig_output.split('\n') if 'Default Gateway' in line]

# Extract the Gateway address from the line
gateway = ', '.join(set([gateway_line.split(':',1)[1].strip() for gateway_line in gateway_lines]))

# Find the line containing the HostName
hostname_line = [line for line in ipconfig_output.split('\n') if 'Host Name' in line][0]

# Extract the HostName from the line
hostname = hostname_line.split(':')[1].strip()

#Crosschecks hostname with the systeminfo information
if not hostname.lower() == infosystem_lines[1].split(":")[1].strip().lower():
    hostname = 'not working'

# Find the line containing the TimeZone and extract the TimeZone
time_zone = [line for line in infosystem_output.split('\n') if 'Time Zone:' in line][0].split(':',1)[1].strip()

# Find the line containing the os_name and extract the os_name
os_name =  [line for line in infosystem_output.split('\n') if 'OS Name:' in line][0].split(':',1)[1].strip()

# Find the line containing the registered owner and extract the owner name
registered_owner = [line for line in infosystem_output.split('\n') if 'Registered Owner:' in line][0].split(':',1)[1].strip()

# Print the IPv4 addresses, Gateway, Time Zone, OS name,Registered Owner, and HostName information
print('General computer information')
print('****************************')
print(f'IPv4 Addresses: {ipv4_addresses}')
print(f'Gateway Address: {gateway}')
print(f'HostName: {hostname} (was cross-checked)')
print(f'Time Zone: {time_zone}')
print(f'OS Name: {os_name}')
print(f'Registered Owner: {registered_owner}')