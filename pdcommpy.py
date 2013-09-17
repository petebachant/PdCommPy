# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 17:16:04 2013

@author: Pete
"""
import win32com.client as _wc
import numpy as np

class PdEvents:
    def __init__(self):
        global velocity
        velocity = None
    def OnNewData(self, hType=1):
        global velocity
        velocity = _pdcommx.GetVel(1,1)

#_pdcommx = _wc.DispatchWithEvents('PdCommATL.PdCommX.1', PdEvents)
_pdcommx = _wc.Dispatch('PdCommATL.PdCommX.1')

# Set up event handling
Events = _wc.getevents("PdCommATL.PdCommX.1")

# Maybe this class belongs in the user application?
# Subclass this in the user application and redefine OnNewData?
class EventHandler(Events):
    def initvectors(self):
        self.velvector = np.array([])
        self.snrvector = np.array([])
    def init_data(self, datadict):
        self.data = datadict
    def append_data(self):
        try:
            self.data["u"] = np.append(self.data["u"], self.u)
            self.data["v"] = np.append(self.data["v"], self.v)
            self.data["w"] = np.append(self.data["w"], self.w)
            self.data["w2"] = np.append(self.data["w2"], self.w2)
            self.data["snr"] = np.append(self.data["snr"], self.snr)
        except NameError:
            pass
    def OnNewData(self, hType=1):
        print "New data"
        self.snr = get_snr(1)
        self.u = get_vel(1,1)
        self.v = get_vel(1,2)
        self.w = get_vel(1,3)
        self.w2 = get_vel(1,4)
        self.snr_u = self.snr[0]
        self.snr_v = self.snr[1]
        self.snr_w = self.snr[3]
        self.snr_w2 = self.snr[4]
        self.corr_u = get_corr(1,1)
        self.corr_v = get_corr(1,2)
        self.corr_w = get_corr(1,3)
        self.corr_w2 = get_corr(1,4)
        self.append_data()


# Device states dict
states = {0 : "Firmware upgrade mode",
          1 : "Measurement mode",
          2 : "Command mode",
          4 : "Data retrieval mode",
          5 : "Confirmation mode",
          -1: "Not connected"}

# Instruments dict
instruments = {0 : "Aquadopp",
               1 : "Vector",
               2 : "Aquapro",
               3 : "AWAC",
               4 : "EasyQ",
               5 : "Continental",
               6 : "Vectrino"}

# Functions
def connect():
    """Connects to the instrument and checks its status."""
    _pdcommx.Connect()
    
def set_serial_port(port):
    """Sets serial port (input as a string)."""
    _pdcommx.SerialPort = port

def get_serial_port():
    """Get current serial port."""
    return str(_pdcommx.SerialPort)

def list_serial_ports():
    """List serial ports on current machine."""
    import os
    import serial
    from serial.tools import list_ports
    # Windows
    if os.name == 'nt':
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append('COM'+str(i + 1))
                s.close()
            except serial.SerialException:
                pass
        return available
    else:
        # Mac / Linux
        return [port[0] for port in list_ports.comports()]

def get_firmware_version():
    """Returns the firmware version. Must be called after connect(), which 
    reads the hardware and software configuration from the instrument."""
    return _pdcommx.GetFirmwareVersion()

def get_head_serialno():
    """Returns the head serial number."""
    return _pdcommx.GetHeadSerialNo()

def set_start_on_synch(choice):
    _pdcommx.StartOnSynch = int(choice)
    
def set_sample_on_synch(choice):
    """Sets sample on synch parameter, meaning device will sample at each
    pulse received."""
    _pdcommx.SampleOnSynch = int(choice)

def set_synch_master(choice):
    """Set the device as a synch master."""
    _pdcommx.SynchMaster = int(choice)

def set_sampling_rate(rate):
    """Set sample rate in Hz"""
    _pdcommx.SamplingRate = rate

def is_connected():
    """Returns a bool indicating connection status."""
    return bool(_pdcommx.IsConnected())

def set_vel_range(velrange):
    """Sets instrument velocity range."""
    _pdcommx.VelRange = int(velrange)    

def set_config():
    """Writes the configuration (properties) to the instrument.
    Note that for most of the property settings to take effect, the SETCONFIG
    method must be called prior to Start command. See also CONNECT."""
    _pdcommx.SetConfig()    

def start(brecorder=False):
    """Starts online measurements based on the current configuration
    of the instrument. If :code:`brecorder = True` data is stored to 
    a new file in the recorder."""
    _pdcommx.Start(brecorder)
    
def start_disk_recording(filename, autoname=False):
    """Starts data recording to disk. Specify the filename without extension. 
    If autoname = True a new file will be opened for data recording each time 
    the specified time interval has elapsed. The current date and time is then 
    automatically added to the filename."""
    _pdcommx.StartDiskRecording(filename, autoname)

def stop_disk_recording():
    """Stops data recording to disk."""
    _pdcommx.StopDiskRecording()

def disconnect():
    """Disconnects device."""
    _pdcommx.Disconnect()

def stop():
    """Stops data collection."""
    _pdcommx.Stop()    

def get_prod_conf():
    """Returns the hardware configuration structure as a VARIANT array. 
    See the Paradopp system integrators manual for a description of the 
    binary data structures."""
    return _pdcommx.GetProdConf()

def get_vel(cell, beam):
    """Gets the most recent velocity data for the specified cell and beam
    (m/s). Cell and beam numbering start at 1."""
    return _pdcommx.GetVel(cell, beam)

def get_velocity(cell):
    """Gets the most recent velocity data for the specified cell number.
    Cell numbering starts at 1."""
    return _pdcommx.GetVelocity(cell)
    
def get_var_velocity():
    """Gets the most recent velocity data as a variant type array."""
    return _pdcommx.GetVarVelocity
    
def get_snr(cell):
    """Gets the most recent SNR data for the specified cell number."""
    return _pdcommx.GetSNR(cell)
    
def get_sampling_volume_value(nSVIndex, nTLIndex):
    """Returns the Sampling Volume corresponding to the Sampling Volume and 
    Transmit Length indices."""
    return _pdcommx.GetSamplingVolumeValue(nSVIndex, nTLIndex)

def get_clock():
    """Returns the current date and time of the RTC in the instrument."""
    return _pdcommx.GetClock()
       
def get_corr(cell, beam):
    """Returns the most recent correlation data for the specified cell 
    and beam number. Cell and beam numbering start at 1."""
    return _pdcommx.GetCorr(cell, beam)
    
def get_instrument(as_string=True):
    """Returns the instrument type."""
    if as_string:
        return instruments[_pdcommx.GetInstrument()]
    else:
        return _pdcommx.GetInstrument()

def get_data_block(hType=1):
    """Returns the most recent measurement data structure as a VARIANT array. 
    See the Paradopp system integrators manual for a description of the 
    binary data structures."""
    return _pdcommx.GetDataBlock(hType)
    
def get_vertical_vel_prec():
    """Returns the vertical velocity precision."""
    return _pdcommx.GetVerticalVelPrec()

def get_horizontal_vel_prec():
    """Returns the horizontal velocity precision."""
    return _pdcommx.GetHorizontalVelPrec()
    
def get_error_message():
    """Gets the most recent error message."""
    return _pdcommx.GetErrorMessage()

def start_distance_check():
    """Starts distance measurements."""
    _pdcommx.StartDistanceCheck()

def validate_config():
    """Returns True if the instrument configuration is valid."""
    return bool(_pdcommx.ValidateConfig())

def inquire_state(as_string=True):
    """Returns the device state. If as_string is false, returns an int."""
    if as_string:
        return states[_pdcommx.InquireState()]
    else:
        return _pdcommx.InquireState()
        
    
class PdControl(object):
    """A PdComm control object."""
    def __init__(self):
        global velocity
        self.velocity = velocity
        
