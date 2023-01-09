#!/usr/bin/env python3

#This tool is an attempt to combine all of the Cetis Configuration File Utilities into an AIO program.

import glob
import time
import tkinter.messagebox
import os, os.path
import progressbar
from re import match
from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

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


if __name__ == "__main__":
    app = Converter()
    app.run()
