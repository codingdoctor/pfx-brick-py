#! /usr/bin/env python3

# PFx Brick configuration data helpers

from pfxbrick.pfx import *
import pfxbrick.pfxdict as pd


def motor_ch_str(x):
    s = []
    if x & EVT_MOTOR_OUTPUT_MASK:
        s.append('Motor Ch ')
        if x & EVT_MOTOR_OUTPUT_A:
            s.append('A ')
        if x & EVT_MOTOR_OUTPUT_B:
            s.append('B ')
        if x & EVT_MOTOR_OUTPUT_C:
            s.append('C ')
        if x & EVT_MOTOR_OUTPUT_D:
            s.append('D ')
    s = ''.join(s)
    return s

def light_ch_str(x):
    s = []
    if x:
        s.append('Ch')
        for i in range(8):
            m = 1 << i
            if (x & m):
                s.append(str(i+1))
    else:
        s.append('None')
    s = ' '.join(s)
    return s
    

class PFxAction:

    def __init__(self):
        self.command = 0
        self.motorActionId = 0
        self.motorParam1 = 0
        self.motorParam2 = 0
        self.lightFxId = 0
        self.lightOutputMask = 0
        self.lightPFOutputMask = 0
        self.lightParam1 = 0
        self.lightParam2 = 0
        self.lightParam3 = 0
        self.lightParam4 = 0
        self.lightParam5 = 0
        self.soundFxId = 0
        self.soundFileId = 0
        self.soundParam1 = 0
        self.soundParam2 = 0

    def __str__(self):
        sb = []
        sb.append('Command           : [%02X] %s' % (self.command, pd.command_dict[self.command]))
        if self.motorActionId & EVT_MOTOR_OUTPUT_MASK == 0:
            sb.append('Motor Action ID   : [%02X] None' % (self.motorActionId))
        else:
            sb.append('Motor Action ID   : [%02X] %s %s' % (self.motorActionId, pd.motor_action_dict[self.motorActionId & EVT_MOTOR_ACTION_ID_MASK], motor_ch_str(self.motorActionId)))
        sb.append('Motor Param 1     : [%02X]' % (self.motorParam1))
        sb.append('Motor Param 2     : [%02X]' % (self.motorParam1))
        sf = ''
        if self.lightFxId & EVT_LIGHT_COMBO_MASK:
            sf = pd.combo_lightfx_dict[self.lightFxId & EVT_LIGHT_ID_MASK]
        else:
            sf = pd.ind_lightfx_dict[self.lightFxId & EVT_LIGHT_ID_MASK]
        sb.append('Light Fx ID       : [%02X] %s' % (self.lightFxId, sf))
        sb.append('Light Output Mask : [%02X] %s' % (self.lightOutputMask, light_ch_str(self.lightOutputMask)))
        sb.append('Light PF Out Mask : [%02X]' % (self.lightPFOutputMask))
        sb.append('Light Param 1     : [%02X]' % (self.lightParam1))
        sb.append('Light Param 2     : [%02X]' % (self.lightParam2))
        sb.append('Light Param 3     : [%02X]' % (self.lightParam3))
        sb.append('Light Param 4     : [%02X]' % (self.lightParam4))
        sb.append('Light Param 5     : [%02X]' % (self.lightParam5))
        sb.append('Sound Fx ID       : [%02X]' % (self.soundFxId))
        sb.append('Sound File ID     : [%02X]' % (self.soundFileId))
        sb.append('Sound Param 1     : [%02X]' % (self.soundParam1))
        sb.append('Sound Param 2     : [%02X]' % (self.soundParam2))
        s = '\n'.join(sb)
        return s
        
    def read_from_brick(self, msg):
        self.command = msg[1]
        self.motorActionId = msg[2]
        self.motorParam1 = msg[3]
        self.motorParam2 = msg[4]
        self.lightFxId = msg[5]
        self.lightOutputMask = msg[6]
        self.lightPFOutputMask = msg[7]
        self.lightParam1 = msg[8]
        self.lightParam2 = msg[9]
        self.lightParam3 = msg[10]
        self.lightParam4 = msg[11]
        self.lightParam5 = msg[12]
        self.soundFxId = msg[13]
        self.soundFileId = msg[14]
        self.soundParam1 = msg[15]
        self.soundParam2 = msg[16]
        
        