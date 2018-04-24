#! /usr/bin/env python3

# PFx Brick python API

import hid
from pfx import *
from pfxconfig import PFxConfig
from pfxaction import PFxAction
from pfxmsg import *
from pfxhelpers import *


class PFxBrick:
    """
    Top level PFx Brick object class.
    
    This class is used to initialize and maintain a communication session
    with a USB connected PFx Brick.
    """
    def __init__(self):
        self.product_id = ""
        self.serial_no = ""
        self.product_desc = ""
        self.firmware_ver = ""
        self.firmware_build = ""
        self.status = 0
        self.error = 0
        self.hid = ''
        self.usb_vid = PFX_USB_VENDOR_ID
        self.usb_pid = PFX_USB_PRODUCT_ID
        self.usb_manu_str = ''
        self.usb_prod_str = ''
        self.usb_serno_str = ''
        self.is_open = False    
        self.name = ''
        
        self.config = PFxConfig()
        
    def open(self):
        """
        Opens a USB communication session with a PFx Brick.
        """
        if not self.is_open:
            self.hid = hid.device()
            self.hid.open(PFX_USB_VENDOR_ID, PFX_USB_PRODUCT_ID)
            self.usb_manu_str = self.hid.get_manufacturer_string()
            self.usb_prod_str = self.hid.get_product_string()
            self.usb_serno_str = self.hid.get_serial_number_string()
            self.is_open = True
            
    def close(self):
        """
        Closes a USB communication session with a PFx Brick.
        """
        if self.is_open:
            self.hid.close()
        
    def get_status(self):
        """
        Requests the top level operational status of the PFx Brick
        using the CMD_PFX_GET_STATUS ICD message.  The resulting
        status data is stored in this class and can be queried
        with typical class member access methods or the print_status method.
        """
        res = cmd_get_status(self.hid)
        if res:
            self.status = res[1]
            self.error = res[2]
            self.product_id = uint16_tostr(res[7], res[8])
            self.serial_no = uint32_tostr(res[9], res[10], res[11], res[12])
            self.product_desc = bytes(res[13:37]).decode("utf-8")
            self.firmware_ver = uint16_tostr(res[37], res[38])
            self.firmware_build = uint16_tostr(res[39], res[40])
                     
    def print_status(self):
        """
        Prints the top level operational status information retrieved
        by a previous call to the get_status method.
        """
        print("USB vendor ID        : %04X" % (self.usb_vid))
        print("USB product ID       : %04X" % (self.usb_pid))
        print("USB product desc     : %s" % (self.usb_prod_str))
        print("USB manufacturer     : %s" % (self.usb_manu_str))
        print("PFx Brick product ID : %s, %s" %(self.product_id, self.product_desc))
        print("Serial number        : %s" % (self.serial_no))
        print("Firmware version     : %s build %s" % (self.firmware_ver, self.firmware_build))
        print("Status : %02X %s" %(self.status, get_status_str(self.status)))
        print("Errors : %02X %s" %(self.error, get_error_str(self.error)))    
        
    def get_config(self):
        """
        Retrieves configuration settings from the PFx Brick using 
        the PFX_CMD_GET_CONFIG ICD message. The configuration data
        is stored in the PFxConfig class member variable config.
        """
        res = cmd_get_config(self.hid)
        if res:
            self.config.read_from_brick(res)
    
    def print_config(self):
        """
        Prints a summary representation of the PFx Brick configuration
        settings which were retrieved by a previous call to get_config.
        """
        print(str(self.config))
        
    def get_name(self):
        """
        Retrieves the user defined name of the PFx Brick using 
        the PFX_CMD_GET_NAME ICD message. The name is stored in
        the name class variable as a UTF-8 string.
        """
        res = cmd_get_name(self.hid)
        if res:
            self.name = bytes(res[1:25]).decode("utf-8")
            
    def set_name(self, name):
        """
        Sets the user defined name of the PFx Brick using the
        PFX_CMD_SET_NAME ICD message.
        
        :param str name: new name to set
        """
        res = cmd_set_name(self.hid, name)
            
    def get_action(self, evtID, ch):
        """
        Retrieves the stored action associated with a particular
        [eventID / IR] channel event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:
        
        Address[5:2] = event ID
        Address[1:0] = channel
        
        :param int evtID: event ID LUT address component (0 - 0x20)
        :param int channel: channel index LUT address component (0 - 3)
        :returns: a PFxAction class filled with retrieved LUT data
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            print("Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch))
            return None
        else:
            res = cmd_get_event_action(self.hid, evtID, ch)
            action = PFxAction()
            if res:
                action.read_from_brick(res)
            return action
        
    