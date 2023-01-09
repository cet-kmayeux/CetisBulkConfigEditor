#!/usr/bin/env python3

#This tool is an attempt to combine all of the Cetis Configuration File Utilities into an AIO program.

import glob
import time
import tkinter.messagebox
import os, os.path
import progressbar
import PIL.Image
from re import match
from PIL import ImageTk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from sys import platform

class ConfigEditor():
    def __init__(self, master=None):
        # Create the GUI window
        self.ConfigEditor = Tk()
        self.ConfigEditor.title("Cetis Bulk Configuration Editor")
    
        # Create a dictionary to store the values to change
        self.values_to_change = {}
    
        # Create a drop down menu
        self.dropdown = ttk.Combobox(self.ConfigEditor, values=[])
    
        # Create an input box
        self.input_box = Entry(self.ConfigEditor)
    
        # Create a button to select the folder
        self.folder_button = Button(self.ConfigEditor, text='Select Folder', command=self.select_folder)
    
        # Create a button to insert the value
        self.insert_button = Button(self.ConfigEditor, text='Insert', command=self.insert_value)
    
        # Create a button to indicate that all values have been entered
        self.done_button = Button(self.ConfigEditor, text='DONE', command=self.done)
    
        # Place the GUI elements in the window
        self.dropdown.pack()
        self.input_box.pack()
        self.folder_button.pack()
        self.insert_button.pack()
        self.done_button.pack()

        self.mainwindow = self.ConfigEditor

    # This function will be called when the "Select Folder" button is clicked
    def select_folder(self):
        global files
        # Ask the user to select a directory
        cwd = os.getcwd()
        folder_path = askdirectory(initialdir=cwd)
    
        # Search for files in the selected directory
        files = glob.glob(folder_path + '/*')
    
        # Scan the first file and find all values delimited by an equals sign "="
        with open(files[0], 'r') as f:
            lines = f.readlines()
    
        values = []
        for line in lines:
            # Split the line at the equals sign and store the left part in the list of values
            parts = line.split('=')
            values.append(parts[0].strip())
    
        # Populate the drop down menu with the values from the first file
        for value in values:
            self.dropdown['values'] = values
    
        # Set the default value for the drop down menu
        self.dropdown.current(0)
    
    # This function will be called when the "Insert" button or the Enter key is pressed
    def insert_value(self):
        # Get the selected value from the drop down menu
        selected_value = self.dropdown.get()
    
        # Get the value from the input box
        input_value = self.input_box.get()
    
        # Store the input value in the dictionary of values to change
        self.values_to_change[selected_value] = input_value
    
        # Clear the input box
        self.input_box.delete(0, 'end')
    
        # Show a message box with the old and new key-value pairs
        old_value = selected_value + ' = ' + self.values_to_change[selected_value]
        new_value = selected_value + ' = ' + input_value
        tkinter.messagebox.showinfo('Change Documented:\n', 'Old key-value pair:\n' + old_value + '\nNew key-value pair:\n' + new_value)
    
    # This function will be called when the "DONE" button is pressed
    def done(self):
        # Record the start time
        start_time = time.time()
    
        # Create a counter to keep track of the number of files changed
        counter = 0
    
        # Go through each file in the selected directory
        for file in files:
            counter += 1
            # Read the file
            with open(file, 'r') as f:
                lines = f.readlines()
    
            # Go through each line in the file
            for i in range(len(lines)):
                for key, value in self.values_to_change.items():
                    # If the line contains the key, replace it with the key and the new value
                    if key in lines[i]:
                        lines[i] = key + '=' + value + '\n'
    
            # Write the modified lines back to the file
            with open(file, 'w') as f:
                f.writelines(lines)
    
        # Calculate the total time taken
        total_time = time.time() - start_time
    
        # Round the total time to the nearest hundreth
        total_time = round(total_time, 2)
    
        # Show a pop-up window with the message "Changes Complete!" and the time taken
        tkinter.messagebox.showinfo('Changes Complete!', 'The changes have been applied to all ' + str(counter) + ' of the files.\n\nTotal time taken: ' + str(total_time) + ' seconds')

    def run(self):
        self.mainwindow.mainloop()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Converter():
    def __init__(self):
        self.folder_name = ''
        self.file_name = ''
        self.input_file = []
        self.output_file = []
        self.input_dict = {}
        self.config_version = 3.1001
        self.file_count = 0
        self.root = Tk()
        self.root.title("Cetis Config File Converter")
        self.root.config(bg='white')
        self.root.minsize(350,150)
        self.root.iconbitmap(resource_path('Converter logo.ico'))
        self.frame = Frame(self.root)
        self.version_number = "1.0"
        self.img = ImageTk.PhotoImage(PIL.Image.open(resource_path('cetis_black.jpg')))

    def get_input_from_file(self):
        try:
            with open(f'{self.folder_name}/{self.file_name}') as input:
                for line in input.readlines():
                    if match('^[a-zA-Z]', line):
                        self.input_file.append(line.strip('\n'))
            self.create_dict_from_list()
        except OSError:
            print('Can not open file\n', f'{self.folder_name}/{self.file_name}')
                
    def create_dict_from_list(self):
        for item in self.input_file:
            self.input_dict[item.split(':')[0].strip()] = item.split(':')[1]
        
    def write_to_file(self):
        try:
            if not os.path.isdir(f'{self.folder_name}/3GENFiles'):
                os.makedirs(self.folder_name + '/3GENFiles')
        except OSError:
            print('Can not create directory\n', f'{self.folder_name}/3GENFiles')
        try:
            with open(f'{self.folder_name}/3GENFiles/{self.file_name.split(".")[0]}.cetis.cfg','w') as output:
                for item in self.output_file:
                    output.write("{}".format(item))
        except OSError:
            print('Can not open file\n', f'{self.folder_name}/3GENFiles/{self.file_name.split(".")[0]}.cetis.cfg')
                
    def translate_gen1_gen3(self):
        self.generate_wan()
        self.generate_lan()
        self.generate_qos()
        self.generate_logging()
        self.generate_digital_map()
        self.generate_call_feature()
        self.generate_audio_config()
        self.generate_time_config()
        self.generate_primary_register()
        self.generate_advanced_config()
        self.generate_security_web()
        self.generate_block_list()
        self.generate_multicast_page()
        self.generate_provisioning()

    def generate_wan(self):
        self.output_file.append(f'\n<<VOIP CONFIG FILE>>Version:{self.config_version}\n#Converted\n\n[WAN_Config]\n#0:DHCP; 1:Static; 2:PPPoE\n')
        if self.input_dict['DHCP Mode'] == '1':
            self.output_file.append('NetworkMode=0\n')
        elif self.input_dict['Pppoe Mode'] == '1':
            self.output_file.append('NetworkMode=2\n')
        else:
            self.output_file.append('NetworkMode=1\n')
        self.output_file.append('#0:AUTO; 1:10baseT/Half; 2:10baseT/Full; 3:100baseT/Half; 4:100baseT/Full\nWLinkMode=0\n')
        self.output_file.append(f'PrimaryDNS={self.input_dict["Primary DNS"]}\nSecondaryDNS={self.input_dict["Alter DNS"]}\n')
        if self.input_dict['Static IP'] == '':
            self.output_file.append('StaticIP=192.168.1.100\n')
        else:
            self.output_file.append(f'StaticIP={self.input_dict["Static IP"]}\n')
        if self.input_dict['Static NetMask'] == '':
            self.output_file.append('SubnetMask=255.255.255.0\n')
        else:
            self.output_file.append(f'SubnetMask={self.input_dict["Static NetMask"]}\n')
        if self.input_dict['Static GateWay'] == '':
            self.output_file.append('DefaultGateway=192.168.1.1\n')
        else:
            self.output_file.append(f'DefaultGateway={self.input_dict["Static GateWay"]}\n')
        self.output_file.append(f'PPPoEAccount={self.input_dict["Pppoe User"]}\nPPPoEPassword={self.input_dict["Pppoe Password"]}\n')
        if 'Xsup DevUnit' and 'Xsup User' and 'Xsup Password' in self.input_dict:
            self.output_file.append(f'IEEE8021xEnable={self.input_dict["Xsup DevUnit"]}\nIEEE8021xUserName={self.input_dict["Xsup Password"]}\nIEEE8021xPassword={self.input_dict["Xsup Password"]}\n')
        else:
            self.output_file.append('IEEE8021xEnable=0\nIEEE8021xUserName=\nIEEE8021xPassword=\n')
        self.output_file.append('IEEE8021xType=0\nLLDPEnable=1\nLLDPInterval=120\n')
    
    def generate_lan(self):
        self.output_file.append('\n[LAN_Config]\n#0:AUTO; 1:10baseT/Half; 2:10baseT/Full; 3:100baseT/Half; 4:100baseT/Full\n')
        self.output_file.append('LLinkMode=0\nWAN2LAN_enable=0\n#0:NAT; 1:Bridge; 2:Disable\n')
        if self.input_dict['Bridge Mode'] == '1':
            self.output_file.append('LAN_disable=1\n')
        elif self.input_dict['Enable Nat'] == '1':
            self.output_file.append('Lan_disable=0\n')
        else:
            self.output_file.append('LAN_disable=2\n')
        self.output_file.append(f'LanPortIP={self.input_dict["Lan Ip"]}\nLanPortSubnet={self.input_dict["Lan NetMask"]}\n')
        self.output_file.append(f'Dhcpd_Enable={self.input_dict["Enable DHCP Server"]}\n')
        self.output_file.append('LanIPStart=192.168.10.10\nLanIPEnd=192.168.10.100\nMaxLeases=10\nDNS_Relay=1\n')
    
    def generate_qos(self):
        self.output_file.append('\n[Qos_Config]\n')
        self.output_file.append(f'Vlan_enable={self.input_dict["Enable VLAN"]}\n')
        self.output_file.append(f'VlanID_Voice={self.input_dict["VLAN ID"]}\nVlanPri_Voice={self.input_dict["DiffServ Value"]}\n')
        self.output_file.append(f'Data_Vlan_enable={self.input_dict["Enable VLAN"]}\n')
        self.output_file.append(f'VlanID_Data={self.input_dict["Data VLAN ID"]}\nVlanPri_Data={self.input_dict["Enable PVID"]}\n')
        self.output_file.append('VoiceQoS=40\nSIPQoS=40\n')
        
    def generate_logging(self):
        self.output_file.append('\n[Logging_Server]\n')
        self.output_file.append(f'EnableLogging={self.input_dict["Enable Syslog"]}\nLogserver={self.input_dict["Syslog address"]}\n')
        self.output_file.append(f'LogPort={self.input_dict["Syslog port"]}\nLogint=0\n')

    def generate_digital_map(self):
        self.output_file.append('\n[Digital_Map]\n')
        for i in range(1,11):
            if f'Item{i} rule' in self.input_dict:
                self.output_file.append(f'Item{i}_Prefixstring={self.input_dict["Item"+str(i) + " rule"]}\n')
            else:
                self.output_file.append(f'Item{i}_Prefixstring=\n')
        self.output_file.append(f'EndPound={self.input_dict["Dial End With #"]}\nDelRedialTimeout=60\n')
        self.output_file.append(f'AutoDialEnable=1\nAutoDialTimeout={self.input_dict["Dial Timeout value"]}\n')
    
    def generate_call_feature(self):
        self.output_file.append('\n[Call_Feature]\n')
        for i in range(1,11):
            if f'Memory Key {i}' in self.input_dict:
                self.output_file.append(f'Item{i}_Func=0\nItem{i}_Number={self.input_dict["Memory Key "+str(i)]}\n')
            else:
                self.output_file.append(f'Item{i}_Func=0\nItem{i}_Number=')
        self.output_file.append(f'MWI_Number={self.input_dict["MWI Number"]}\n')
        if 'SIP1 Park Mode' in self.input_dict:
            self.output_file.append(f'ParkMode={self.input_dict["SIP1 Park Mode"]}\n')
        else:
            self.output_file.append('ParkMode=0\n')
        if 'Memory Key HdActive' and 'Memory Key HdIdle' in self.input_dict:
            self.output_file.append(f'Memory_Key_HdActive={self.input_dict["Memory Key HdActive"]}\nMemory_Key_HdIdle={self.input_dict["Memory Key HdIdle"]}\n')
        else:
            self.output_file.append('Memory_Key_HdActive=\nMemory_Key_HdIdle=\n')
        self.output_file.append(f'HotlineNumber={self.input_dict["SIP1 Hotline Number"]}\n')
        if 'P1 Warm Line Time' in self.input_dict:
            self.output_file.append(f'WarmLineTime={self.input_dict["P1 Warm Line Time"]}\n')
        else:
            self.output_file.append('WarmLineTime=4\n')
        self.output_file.append(f'AutoAnswer={self.input_dict["P1 AutoAnswer"]}\nAutoAnswerTime={self.input_dict["P1 AutoAnswer"]}\n')
        self.output_file.append('#0:Disable; 1:All Forward; 2:Busy Forward; 3:No Answer Forward\n')
        self.output_file.append(f'CallForward={self.input_dict["P1 Forward Service"]}\n')
        if 'P1 Extension No.' in self.input_dict:
            self.output_file.append(f'ForwardtoNumber={self.input_dict["P1 Extension No."]}\n')
        else:
            self.output_file.append('ForwardtoNumber=\n')
        if 'P1 Auto HandDown' in self.input_dict:
            self.output_file.append(f'NoAnswerTimeout_Enable={self.input_dict["P1 Auto HandDown"]}\n')
        else:
            self.output_file.append('NoAnswerTimeout_Enable=0\n')
        self.output_file.append(f'NoAnswerTimeout={self.input_dict["P1 No Answer Time"]}\n')
        self.output_file.append(f'CallWaiting={self.input_dict["P1 CallWaiting"]}\nNoDisturb={self.input_dict["P1 No Disturb"]}\n')
        self.output_file.append(f'BanOutgoing=0\nAcceptAnyCall={self.input_dict["Accept Any Call"]}\n')
        self.output_file.append(f'Hide_Display=0\nGreeting_Message={self.input_dict["LCD Logo"]}\n')

    def generate_audio_config(self):
        self.output_file.append('\n[Audio_Config]\n')
        self.output_file.append(f'HandsetVol={self.input_dict["P1 Output Vol"]}\nSpeakerVol={self.input_dict["P1 HandFree Vol"]}\n')
        self.output_file.append(f'RingToneVol={self.input_dict["P1 RingTone Vol"]}\n')
        self.output_file.append('#0:Belgium; 1:China; 2:Germany; 3:Israel; 4:Japan;\n')
        self.output_file.append('#5:Netherlands; 6:Norway; 7:South Korea; 8:Sweden;\n')
        self.output_file.append('#9:Switzerland; 10:Taiwan; 11:United States\n')
        self.output_file.append(f'SignalStandard={self.input_dict["Signal Standard"]}\n')
        self.output_file.append(f'RingerEnable=1\nRingertype={self.input_dict["Ring Type"]}\n')
        self.output_file.append('#0:G.711a; 1:G.711u; 2:G.723; 3:G.729; 4:iLBC; 5:G.722\n')
        list = ['P1 First Codec','P1 Second Codec','P1 Third Codec']
        for item in ['P1 First Codec','P1 Second Codec','P1 Third Codec']:
            if self.input_dict[item] == '15':
                self.output_file.append(f'Codec_{list.index(item)+1}=3\n')
            elif self.input_dict[item] == '1':
                self.output_file.append(f'Codec_{list.index(item)+1}=1\n')
            elif self.input_dict[item] == '17':
                self.output_file.append(f'Codec_{list.index(item)+1}=4\n')
            if item == 'P1 First Codec':
                self.output_file.append('#0:Not Used; 1:G.711a; 2:G.711u; 3:G.723; 4:G.729; 5:iLBC; 6:G.722\n')
        self.output_file.append(f'Codec_4={self.input_dict["P1 Forth Codec"]}\nCodec_5={self.input_dict["P1 Fifth Codec"]}\n')
        self.output_file.append(f'Codec_6=6\nptime=1\niLBC15K2=0\nG72353K=0\nVAD={self.input_dict["VAD"]}\n')
        self.output_file.append(f'CNG=0\nRFC2833ID={self.input_dict["Dtmf Payload Type"]}\n')

    def generate_time_config(self):
        self.output_file.append(f'\n[Time_Config]\nSNTPEnable={self.input_dict["Enable SNTP"]}\n')
        self.output_file.append(f'SNTPServerAddress={self.input_dict["SNTP Server"]}\nTimezone={self.input_dict["Time Zone"]}\n')
        self.output_file.append(f'PollingInterval={self.input_dict["SNTP Time Out"]}\nlocaltime=2011:01:01:00:00\n')
        if f'Display Time' in self.input_dict:
            self.output_file.append(f'TimeDisplay={self.input_dict["Display Time"]}\n')
        else:
            self.output_file.append(f'TimeDisplay=1')

        if f'Time 12hours' in self.input_dict:
            self.output_file.append(f'TimeDisplay24={self.input_dict["Time 12hours"]}\n')
        else:
            self.output_file.append(f'TimeDisplay24=0\n')


        self.output_file.append(f'DayLightSaving={self.input_dict["Enable Daylight"]}\nDayLightOffset={self.input_dict["DayLight Shift Min"]}\n')
        self.output_file.append(f'DayLightStartMon={self.input_dict["DayLight Start Mon"]}\nDayLightStartWeek={self.input_dict["DayLight Start Week"]}\n')
        self.output_file.append(f'DayLightStartWday={self.input_dict["DayLight Start Wday"]}\nDayLightStartHour={self.input_dict["DayLight Start Hour"]}\n')
        self.output_file.append(f'DayLightEndMon={self.input_dict["DayLight End Mon"]}\nDayLightEndWeek={self.input_dict["DayLight End Week"]}\n')
        self.output_file.append(f'DayLightEndWday={self.input_dict["DayLight End Wday"]}\nDayLightEndHour={self.input_dict["DayLight End Hour"]}\n')

    def generate_primary_register(self):
        self.output_file.append('\n[Primary_Register]\n')
        self.output_file.append(f'RegisterEnable={self.input_dict["SIP1 Enable Reg"]}\nDisplayName={self.input_dict["SIP1 Display Name"]}\n')
        self.output_file.append(f'RegisterUserName={self.input_dict["SIP1 Register User"]}\nAuthUserName={self.input_dict["SIP1 Register User"]}\n')
        self.output_file.append(f'RegisterPassword={self.input_dict["SIP1 Register Pwd"]}\nRegisterServerPort={self.input_dict["SIP1 Register Port"]}\n')
        self.output_file.append(f'RegisterServerAddress={self.input_dict["SIP1 Register Addr"]}\nDomainRealm={self.input_dict["SIP1 Local Domain"]}\n')
        self.output_file.append(f'Outbound_proxy={self.input_dict["SIP1 Proxy Addr"]}\nRegisterExpire={self.input_dict["SIP1 Sub Expire"]}\n')
        self.output_file.append('#0:None; 1:Failover; 2:Redundant\nBKType=0\nBKServer=\n')
        self.output_file.append(f'SubscribeEnable={self.input_dict["SIP1 Subscribe"]}\nSubscribeExpire={self.input_dict["SIP1 Sub Expire"]}\n')
        self.output_file.append(f'LocalSIPPort={self.input_dict["SIP  Port"]}\nLocalRTPPort=20000\nSendKeepAlivesPacket=1\nKeepAlivesPeriod=60\n')
        self.output_file.append(f'#0:RFC 2833; 1:Inband; 2:SIP Info\nDTMFMode={self.input_dict["SIP1 DTMF Mode"]}\n')
        self.output_file.append('SIP_INFO101=0\nDNSType=2\nJitterBuffer_max=150\n')
        self.output_file.append('AnonymousCallRejection=0\nsessionswitch=0\nsessiontime=1800\n')
        self.output_file.append(f'PRACKEnable={self.input_dict["SIP1 PRACK"]}\nUpdatemethod=1\nRport=1\n')
        self.output_file.append(f'Transport={self.input_dict["SIP1 Transport"]}\nSipurl=0\nSRTP=0\n')

    def generate_advanced_config(self):
        self.output_file.append(f'\n[Advanced_Config]\nStunEnable={self.input_dict["SIP1 Use Stun"]}\n')
        self.output_file.append(f'StunServerAddress={self.input_dict["Stun Address"]}\nStunServerPort={self.input_dict["Stun Port"]}\n')
    
    def generate_security_web(self):
        self.output_file.append(f'\n[Security_Web]\nKeypadPassword={self.input_dict["Keypad Password"]}\n')
        self.output_file.append(f'AdminName={self.input_dict["Account1 Name"]}\nAdminPassword={self.input_dict["Account1 Pass"]}\n')
        if self.input_dict['Account2 Name'] != '':
            self.output_file.append(f'CetisAdminUser={self.input_dict["Account2 Name"]}\nCetisAdminPassword={self.input_dict["Account2 Pass"]}\n')
        else:
            self.output_file.append(f'CetisAdminUser=admin\nCetisAdminPassword=admin\n')

    def generate_block_list(self):
        self.output_file.append('\n[Block_List]\n')
        for i in range(1,11):
            self.output_file.append(f'BlackList{i}=\n')

    def generate_multicast_page(self):
        self.output_file.append('\n[Multicast_Page]\nPagingBarge=10\nPagingPriorityActive=0\nMulticastPageCodec=0\n')
        for i in range(1,11):
            self.output_file.append(f'Multicast_IP{i}=\nMulticast_Label{i}=\n')

    def generate_provisioning(self):
        self.output_file.append('\n[Provisioning]\n')
        self.output_file.append('DHCPOptionsEnable=1\nCetisRedirectEnable=1\nMacFileEnable=1\n')
        self.output_file.append('ConfigIDRequestEnable=1\nFWUpdateEnable=1\nNotifyAuth=2\n')
        self.output_file.append('Requesttimeoutrestart=1\n#0:Disable; 1:tftp; 2:ftp; 3:http; 4:https\n')
        if 'Download Server IP' != '':
            self.output_file.append(f'ProvisioningServerType=0\nProvisioningServer={self.input_dict["Download Server IP"]}\n')
            self.output_file.append(f'ProvisioningUserName={self.input_dict["Download Username"]}\nProvisioningPassword={self.input_dict["Download password"]}\n')
        else:
            self.output_file.append(f'ProvisioningServerType=0\nProvisioningServer=0.0.0.0\nProvisioningUserName=user\ProvisioningPassword=pass\nn')
        self.output_file.append(f'ConfigId={self.file_name.split(".")[0]}\n#0-24 1-24 hour,random 0-60minutes.\nConfigIDUpdateTime=0\n#0-24 1-24 hour,random 0-60minutes.\n')
        self.output_file.append(f'FWUpdateTime=0\nConfig_Version={self.config_version}')

    def convert_files(self):
        start_time = time()
        try:
            for file in os.listdir(self.folder_name):
                if file.endswith('3300IP.txt'):
                    self.file_name = file
                    self.get_input_from_file()
                    self.translate_gen1_gen3()
                    self.write_to_file()
                    self.reset()
                    self.file_count += 1
        except OSError:
            print('Can not open specified path',self.folder_name)
        end_time = time()
        messagebox.showinfo('Files Converted',f"Converted {self.file_count} Files\n Files located in {self.folder_name}/3GENFiles\n Total Time Elapsed: {round(end_time-start_time,4)} secs")

    def reset(self):
        self.input_file = []
        self.output_file = []
        self.input_dict = {}

    def create_ui(self):
        cetis_logo = Label(self.root, image=self.img, bg='white').pack(side=TOP,expand=YES)
        start_text = Label(text="Please put all config files in an accessible folder",bg='white', fg='black').pack(side=TOP,expand=YES)
        browse_button = Button(self.root, text="Select Folder To Convert Files", command=self.browse_for_starting_folder, bg='white',fg='black').pack(side=TOP,expand=YES)
        convert_button = Button(self.root, text='Convert Files', command=self.convert_files, bg='white',fg='black').pack(side=TOP,expand=YES)
        version_number = Label(text=f"Version: {self.version_number}", bg='white', fg='black').pack(side=TOP,expand=YES)

    def browse_for_starting_folder(self):
        open_file_dialog = filedialog.askdirectory()
        self.folder_name = open_file_dialog

    def run(self):
        self.create_ui()
        self.root.mainloop()

class CetisMCU():
    # define the name of the directory to be created
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        path = os.getcwd() + "/GeneratedConfigs"
    elif platform == "win32" or platform == "win64":
        path = os.getcwd() + "\GeneratedConfigs"

    try:
        os.mkdir(path)
    except OSError:
        print ("%s present, continue.." % path)
    else:
        print ("Successfully created the directory %s " % path)
    
    #######################################################################
    def yes_or_no(question):
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        else:
            return yes_or_no("Uhhhh... please enter ")
    
    try:
        input("Read the instructions, press Enter to continue. ")
    except SyntaxError:
        pass
    #######################################################################
    
    number_of_files = input('How many files would you like to create? ')
    ext = input('What is the first Extension? ')
    sipserver = input('What is the SIP server IP? ')
    
    extensionpassword = yes_or_no('Default extension password is same as extension number, would you like to change this to use the same password for all? ')
    if extensionpassword == True:
    	extensionpassword = input('What is the universal extension password? ')
    	extensionpassword_selector = 0
    if extensionpassword == False:
    	extensionpassword = ext
    	extensionpassword_selector = 1
    
    Domain_Realm = yes_or_no('Do you use a domain realm? ')
    if Domain_Realm == True:
    	Domain_Realm = input('Enter domain realm ')
    if Domain_Realm == False:
    	Domain_Realm = ''
    
    Proxy = yes_or_no('Is outbound proxy required? ')
    if Proxy == True:
    	Proxy = input('What is the outbound proxy? ')
    if Proxy == False:
    	Proxy == ''
    
    #Set options to use DHCP or Static IP addressing
    Static = yes_or_no('Static IP?' )
    if Static == True:
    	Network_Mode = 1
    	Static_IP = input('What is the starting IP Address? ')
    	Static_Netmask = input('What is the Netmask? ')
    	Static_Gateway = input('What is the Gateway? ')
    if Static == False:
    	Network_Mode = 0
    	Static_IP = ''
    	Static_Netmask = ''
    	Static_Gateway = ''
    	
    #Set VLAN options
    VLAN = yes_or_no('VLAN? ')
    if VLAN == True:
    	VLAN_enable = 1
    	VLAN_Voice = input('What is the VLAN ID? ')
    if VLAN == False:
    	VLAN_enable = 0
    	VLAN_Voice = ''
    
    #Set memory keys
    
    Memory = yes_or_no('Would you like to add memory keys? ')
    if Memory == True:
    	mem_1 = input('Enter Memory Key 1: ')
    	mem_2 = input('Enter Memory Key 2: ')
    	mem_3 = input('Enter Memory Key 3: ')
    	mem_4 = input('Enter Memory Key 4: ')
    	mem_5 = input('Enter Memory Key 5: ')
    	mem_6 = input('Enter Memory Key 6: ')
    	mem_7 = input('Enter Memory Key 7: ')
    	mem_8 = input('Enter Memory Key 8: ')
    	mem_9 = input('Enter Memory Key 9: ')
    	mem_10 = input('Enter Memory Key 10: ')
    if Memory == False:
    	mem_1 = ''
    	mem_2 = ''
    	mem_3 = ''
    	mem_4 = ''
    	mem_5 = ''
    	mem_6 = ''
    	mem_7 = ''
    	mem_8 = ''
    	mem_9 = ''
    	mem_10 = ''
    	
    mwi = yes_or_no('Do you have a voicemail number(MWI)? ')
    if mwi == True:
    	mwi = input('Enter number: ')
    if mwi == False:
    	mwi = ''
    	
    #Set Logging options	
    Logging = yes_or_no('Enable Logging? ')
    if Logging == True:
    	Enable_logging = 1
    	Loggingserver = input('What is the Logging Server IP? ')
    if Logging == False:
    	Enable_logging = 0
    	Loggingserver = ''
    
    #Set NTP options
    NTP = yes_or_no('Do you use an custom NTP server? Default is pool.ntp.org ')
    if NTP == True:
    	ntp_enable = 1
    	ntp_server = input('What is the NTP server IP address? ')
    	Timezone = input('Input your timezone code: ')
    if NTP == False:
    	ntp_enable = 1
    	ntp_server = 'pool.ntp.org'
    	Timezone = input('Input your timezone code: ')
    
    
    	
    #Security Settings
    KeypadPassword = yes_or_no('Default Keypad password is 123, do you want to change it? ')
    
    if KeypadPassword == True:
    	Keypad_Password = input('Enter new numberical password ')
    else:
    	Keypad_Password = '123'
    Admin_User = yes_or_no('Default Web Interface Username is admin, do you want to change it? ')
    
    if Admin_User == True:
    	Admin_User = input('Enter your new username ')
    else:
    	Admin_User = 'admin'
    
    Admin_Password = yes_or_no('Default Web Interface password is admin, do you want to change it? ')
    
    if Admin_Password == True:
    	Admin_Password = input('Enter your new password ')
    else:
    	Admin_Password = 'admin'
    
    #Provisioning
    print('0 = Disabled, 1 = TFTP, 2 = FTP, 3 = HTTP, 4 = HTTPS ')
    Provisioning_Server_Type = eval(input('Which provisioning server type? Enter the number from above: '))
    if Provisioning_Server_Type == 0:
    	Provisioning_Type = 0
    	Provisioning_URL = ''
    	Provisioning_User = ''
    	Provisioning_Password = ''
    if Provisioning_Server_Type == 1:
    	Provisioning_Type = 1
    	Provisioning_URL = input('Enter the IP address: ')
    	Provisioning_User = ''
    	Provisioning_Password = ''
    if Provisioning_Server_Type == 2:
    	Provisioning_Type = 2
    	Provisioning_URL = input('Enter the IP address: ')
    	Provisioning_User = ''
    	Provisioning_Password = ''
    
    if Provisioning_Server_Type == 3:
    	Provisioning_Type = 3
    	Provisioning_URL = input('Enter the IP address: ')
    	Provisioning_User = ''
    	Provisioning_Password = ''
    if Provisioning_Server_Type == 4:
    	Provisioning_Type = 4
    	Provisioning_URL = input('Enter the IP address: ')
    	Provisioning_User = ''
    	Provisioning_Password = ''
    
    if Provisioning_Server_Type == 3:
    	Auth = yes_or_no('Is authentication required? ')
    	if Auth == True:
    		Provisioning_User = input('Enter Username: ')
    		Provisioning_Password = input('Enter  Password: ')
    	if Auth == False:
    		Provisioning_User = ''
    		Provisioning_Password = ''
    		
    if Provisioning_Server_Type == 4:
    	Auth = yes_or_no('Is authentication required? ')
    	if Auth == True:
    		Provisioning_User = input('Enter Username: ')
    		Provisioning_Password = input('Enter  Password: ')
    	if Auth == False:
    		Provisioning_User = ''
    		Provisioning_Password = ''
    
    Config_ID = str(ext)
    LAN_disable = 2
    
    #######################################################################
    
    
    
    config = """
    <<VOIP CONFIG FILE>>Version:3.1005
    
    [WAN_Config]
    #0:DHCP; 1:Static; 2:PPPoE
    NetworkMode={Network_Mode}
    #0:AUTO; 1:10baseT/Half; 2:10baseT/Full; 3:100baseT/Half; 4:100baseT/Full
    WLinkMode=0
    PrimaryDNS=8.8.8.8
    SecondaryDNS=8.8.4.4
    StaticIP={Static_IP}
    SubnetMask={Static_Netmask}
    DefaultGateway={Static_Gateway}
    PPPoEAccount=
    PPPoEPassword=
    IEEE8021xEnable=0
    IEEE8021xUserName=
    IEEE8021xPassword=
    IEEE8021xType=0
    LLDPEnable=1
    LLDPInterval=120
    
    [LAN_Config]
    #0:AUTO; 1:10baseT/Half; 2:10baseT/Full; 3:100baseT/Half; 4:100baseT/Full
    LLinkMode=0
    WAN2LAN_enable=0
    #0:NAT; 1:Bridge; 2:Disable
    LAN_disable={LAN_disable}
    LanPortIP=192.168.10.1
    LanPortSubnet=255.255.255.0
    Dhcpd_Enable=1
    LanIPStart=192.168.10.10
    LanIPEnd=192.168.10.100
    MaxLeases=10
    DNS_Relay=1
    
    [Qos_Config]
    Vlan_enable={VLAN_enable}
    VlanID_Voice={VLAN_Voice}
    VlanPri_Voice=0
    Data_Vlan_enable=0
    VlanID_Data=137
    VlanPri_Data=0
    VoiceQoS=40
    SIPQoS=40
    
    [Logging_Server]
    EnableLogging={Enable_logging}
    Logserver={Loggingserver}
    LogPort=49494
    Logint=30
    
    [Digital_Map]
    Item1_Prefixstring=
    Item2_Prefixstring=
    Item3_Prefixstring=
    Item4_Prefixstring=
    Item5_Prefixstring=
    Item6_Prefixstring=
    Item7_Prefixstring=
    Item8_Prefixstring=
    Item9_Prefixstring=
    Item10_Prefixstring=
    EndPound=1
    DelRedialTimeout=60
    AutoDialEnable=1
    AutoDialTimeout=5
    
    [Call_Feature]
    Item1_Func=0
    Item1_Number={mem_1}
    Item2_Func=0
    Item2_Number={mem_2}
    Item3_Func=0
    Item3_Number={mem_3}
    Item4_Func=0
    Item4_Number={mem_4}
    Item5_Func=0
    Item5_Number={mem_5}
    Item6_Func=0
    Item6_Number={mem_6}
    Item7_Func=0
    Item7_Number={mem_7}
    Item8_Func=0
    Item8_Number={mem_8}
    Item9_Func=0
    Item9_Number={mem_9}
    Item10_Func=0
    Item10_Number={mem_10}
    MWI_Number={mwi}
    ParkMode=0
    Memory_Key_HdActive=
    Memory_Key_HdIdle=
    HotlineNumber=
    WarmLineTime=4
    AutoAnswer=0
    AutoAnswerTime=5
    #0:Disable; 1:All Forward; 2:Busy Forward; 3:No Answer Forward
    CallForward=0
    ForwardtoNumber=
    NoAnswerTimeout_Enable=1
    NoAnswerTimeout=20
    CallWaiting=1
    NoDisturb=0
    BanOutgoing=0
    AcceptAnyCall=1
    LCD_Contrast=3
    Greeting_Message=
    
    [Audio_Config]
    HandsetVol=7
    SpeakerVol=5
    RingToneVol=5
    #0:Belgium; 1:China; 2:Bermany; 3:Isreal; 4:Japan;
    #5:Netherlands; 6:Norway; 7:South Korea; 8:Sweden;
    #9:Switzerland; 10:TaiWan; 11:United States
    SignalStandard=11
    RingerEnable=1
    Ringertype=0
    #0:G.711a; 1:G.711u; 2:G.723; 3:G.729; 4:iLBC; 5:G.722
    Codec_1=1
    #0:Not Used; 1:G.711a; 2:G.711u; 3:G.723; 4:G.729; 5:iLBC; 6:G.722
    Codec_2=3
    Codec_3=4
    Codec_4=1
    Codec_5=5
    Codec_6=6
    ptime=1
    iLBC15K2=0
    G72353K=0
    VAD=0
    CNG=0
    RFC2833ID=101
    
    [Time_Config]
    SNTPEnable={ntp_enable}
    SNTPServerAddress={ntp_server}
    Timezone={Timezone}
    PollingInterval=21600
    localtime=2011:01:01:00:00
    TimeDisplay=1
    TimeDisplay24=1
    DayLightSaving=1
    DayLightOffset=60
    DayLightStartMon=2
    DayLightStartWeek=1
    DayLightStartWday=0
    DayLightStartHour=2
    DayLightEndMon=10
    DayLightEndWeek=1
    DayLightEndWday=0
    DayLightEndHour=2
    
    [Primary_Register]
    RegisterEnable=1
    DisplayName={extension}
    RegisterUserName={extension}
    AuthUserName={extension}
    RegisterPassword={extensionpassword}
    RegisterServerPort=5060
    RegisterServerAddress={sipserver}
    DomainRealm={Domain_Realm}
    Outbound_proxy={Proxy}
    RegisterExpire=300
    #0:None; 1:Failover; 2:Redundant
    BKType=0
    BKServer=
    SubscribeEnable=1
    SubscribeExpire=300
    LocalSIPPort=5060
    LocalRTPPort=20000
    SendKeepAlivesPacket=1
    KeepAlivesPeriod=60
    #0:RFC 2833; 1:Inband; 2:SIP Info
    DTMFMode=0
    SIP_INFO101=0
    DNSType=2
    JitterBuffer_max=150
    AnonymousCallRejection=0
    sessionswitch=0
    sessiontime=1800
    PRACKEnable=0
    Updatemethod=0
    Rport=1
    Transport=0
    Sipurl=0
    SRTP=0
    
    [Advanced_Config]
    StunEnable=0
    StunServerAddress=
    StunServerPort=3478
    
    [Security_Web]
    KeypadPassword={Keypad_Password}
    AdminName={Admin_User}
    AdminPassword={Admin_Password}
    CetisAdminUser=admin
    CetisAdminPassword=admin
    
    [Block_List]
    BlackList1=
    BlackList2=
    BlackList3=
    BlackList4=
    BlackList5=
    BlackList6=
    BlackList7=
    BlackList8=
    BlackList9=
    BlackList10=
    
    [Multicast_Page]
    PagingBarge=10
    PagingPriorityActive=0
    MulticastPageCodec=0
    Multicast_IP1=
    Multicast_Label1=
    Multicast_IP2=
    Multicast_Label2=
    Multicast_IP3=
    Multicast_Label3=
    Multicast_IP4=
    Multicast_Label4=
    Multicast_IP5=
    Multicast_Label5=
    Multicast_IP6=
    Multicast_Label6=
    Multicast_IP7=
    Multicast_Label7=
    Multicast_IP8=
    Multicast_Label8=
    Multicast_IP9=
    Multicast_Label9=
    Multicast_IP10=
    Multicast_Label10=
    
    [Provisioning]
    DHCPOptionsEnable=1
    CetisRedirectEnable=1
    GlobalConfigEnable=1
    MacFileEnable=1
    ConfigIDRequestEnable=1
    PartialConfigEnable=1
    FWUpdateEnable=1
    NotifyAuth=2
    Requesttimeoutrestart=1
    ProvisioningServerType={Provisioning_Type}
    ProvisioningServer={Provisioning_URL}
    ProvisioningUserName={Provisioning_User}
    ProvisioningPassword={Provisioning_Password}
    ConfigId={Config_ID}
    #0-24 1-24 hour,random 0-60minutes.
    ConfigIDUpdateTime=0
    #0-24 1-24 hour,random 0-60minutes.
    FWUpdateTime=0
    Config_Version=3.1000
    RegisterPasswordExport=0
    Savesystemlogs=0
    
    [SystemActions]
    AutoRebootEnable=1
    AutoRebootExpire=7
    Rebootoffsettime=5
    
    [Phonebook_Table]
    Phbook_Name1=
    Phbook_Number1=
    Phbook_Name2=
    Phbook_Number2=
    Phbook_Name3=
    Phbook_Number3=
    Phbook_Name4=
    Phbook_Number4=
    Phbook_Name5=
    Phbook_Number5=
    Phbook_Name6=
    Phbook_Number6=
    Phbook_Name7=
    Phbook_Number7=
    Phbook_Name8=
    Phbook_Number8=
    Phbook_Name9=
    Phbook_Number9=
    Phbook_Name10=
    Phbook_Number10=
    Phbook_Name11=
    Phbook_Number11=
    Phbook_Name12=
    Phbook_Number12=
    Phbook_Name13=
    Phbook_Number13=
    Phbook_Name14=
    Phbook_Number14=
    Phbook_Name15=
    Phbook_Number15=
    Phbook_Name16=
    Phbook_Number16=
    Phbook_Name17=
    Phbook_Number17=
    Phbook_Name18=
    Phbook_Number18=
    Phbook_Name19=
    Phbook_Number19=
    Phbook_Name20=
    Phbook_Number20=
    
    """
    
    y = int(number_of_files)
    i = 0
    print('Creating files now... ')
    
    start_time = time.time()
    for i in range(y):
    	 if i < y:
    		 Config_ID = str(ext)
    		 if not Proxy:
    			 Proxy = ''
    		 d = { 'extension': ext , 'extensionpassword' : extensionpassword , 'sipserver' : sipserver , 'Network_Mode' : Network_Mode , 'VLAN_enable' : VLAN_enable , 'VLAN_Voice' : VLAN_Voice ,
    		 'Enable_logging' : Enable_logging , 'Loggingserver' : Loggingserver , 'ntp_enable' : ntp_enable , 'ntp_server' : ntp_server , 'Config_ID' : Config_ID , 'Static_IP' : Static_IP , 
    		 'Static_Netmask' : Static_Netmask , 'Static_Gateway' : Static_Gateway , 'LAN_disable' : LAN_disable , 'Loggingserver' : Loggingserver , 'ntp_enable' : ntp_enable , 'ntp_server' : ntp_server ,
    		 'Keypad_Password' : Keypad_Password , 'Admin_User' : Admin_User , 'Admin_Password' : Admin_Password , 'Provisioning_Type' : Provisioning_Type , 'Provisioning_URL' : Provisioning_URL , 
    		 'Provisioning_User' : Provisioning_User , 'Provisioning_Password' : Provisioning_Password , 'Domain_Realm' : Domain_Realm , 'Proxy' : Proxy , 'Timezone' : Timezone , 'mwi' : mwi ,
    		 'mem_1' : mem_1 , 'mem_2' : mem_2 , 'mem_3' : mem_3 , 'mem_4' : mem_4 , 'mem_5' : mem_5 , 'mem_6' : mem_6 , 'mem_7' : mem_7 , 'mem_8' : mem_8 , 'mem_9' : mem_9 , 'mem_10' : mem_10}
    
    
    		 save_path = path
    
    		 name_of_file = Config_ID
    
    		 completeName = os.path.join(save_path, name_of_file+".cetis.cfg")         
    
    		 file1 = open(completeName, "w")
    
    		 toFile = (config.format(**d))
    
    		 file1.write(toFile)
    
    		 file1.close()
    	 
    		 
    		 
    		 i += i
    		 ext = int(ext)
    		 ext += 1
    		 ext = str(ext)
    		 
    		 if extensionpassword_selector == 1:
    			 extensionpassword = int(extensionpassword)
    			 extensionpassword += 1
    			 extensionpassword = str(extensionpassword)
    				
    
    
    		 if not Static_IP:
    			 continue
    		 else:
    			 ipaddy = Static_IP
    			 first, second, third, fourth = str(ipaddy).split('.')
    			 last_octet = int(fourth)
    			 change_ip = last_octet + 1
    			 change_ip = str(change_ip)
    			 if int(fourth) > 253:
    				 third = int(third) + 1
    				 third = str(third)
    				 fourth = 2
    				 change_ip = str(fourth)
    	
    			 Static_IP = first +'.'+ second +'.'+ third +'.'+ change_ip
    
    
    
    time_to_complete =  str(round(time.time() - start_time, 2))
    
    print('Successfully created ' + number_of_files + ' files' + ' in ' + time_to_complete + ' seconds')
    input('Your new files can be found at ' +  path + ', press enter to exit..')
    
    
    
if __name__ == "__main__":
    app = Converter()
    app.run()
