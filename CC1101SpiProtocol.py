
from copy import deepcopy


# Table 43: Configuration Registers Overview
CONFIG_REGISTERS = {
    0x00: {"register": "IOCFG2",                "description": "GDO2 output pin configuration"},
    0x01: {"register": "IOCFG1",                "description": "GDO1 output pin configuration"},
    0x02: {"register": "IOCFG0",                "description": "GDO0 output pin configuration"},
    0x03: {"register": "FIFOTHR",               "description": "RX FIFO and TX FIFO thresholds"},
    0x04: {"register": "SYNC1",                 "description": "Sync word, high byte"},
    0x05: {"register": "SYNC0",                 "description": "Sync word, low byte"},
    0x06: {"register": "PKTLEN",                "description": "Packet length"},
    0x07: {"register": "PKTCTRL1",              "description": "Packet automation control"},
    0x08: {"register": "PKTCTRL0",              "description": "Packet automation control"},
    0x09: {"register": "ADDR",                  "description": "Device address"},
    0x0A: {"register": "CHANNR",                "description": "Channel number"},
    0x0B: {"register": "FSCTRL1",               "description": "Frequency synthesizer control"},
    0x0C: {"register": "FSCTRL0",               "description": "Frequency synthesizer control"},
    0x0D: {"register": "FREQ2",                 "description": "Frequency control word, high byte"},
    0x0E: {"register": "FREQ1",                 "description": "Frequency control word, middle byte"},
    0x0F: {"register": "FREQ0",                 "description": "Frequency control word, low byte"},
    0x10: {"register": "MDMCFG4",               "description": "Modem configuration"},
    0x11: {"register": "MDMCFG3",               "description": "Modem configuration"},
    0x12: {"register": "MDMCFG2",               "description": "Modem configuration"},
    0x13: {"register": "MDMCFG1",               "description": "Modem configuration"},
    0x14: {"register": "MDMCFG0",               "description": "Modem configuration"},
    0x15: {"register": "DEVIATN",               "description": "Modem deviation setting"},
    0x16: {"register": "MCSM2",                 "description": "Main Radio Control State Machine configuration"},
    0x17: {"register": "MCSM1",                 "description": "Main Radio Control State Machine configuration"},
    0x18: {"register": "MCSM0",                 "description": "Main Radio Control State Machine configuration"},
    0x19: {"register": "FOCCFG",                "description": "Frequency Offset Compensation configuration"},
    0x1A: {"register": "BSCFG",                 "description": "Bit Synchronization configuration"},
    0x1B: {"register": "AGCCTRL2",              "description": "AGC control"},
    0x1C: {"register": "AGCCTRL1",              "description": "AGC control"},
    0x1D: {"register": "AGCCTRL0",              "description": "AGC control"},
    0x1E: {"register": "WOREVT1",               "description": "High byte Event 0 timeout"},
    0x1F: {"register": "WOREVT0",               "description": "Low byte Event 0 timeout"},
    0x20: {"register": "WORCTRL",               "description": "Wake On Radio control"},
    0x21: {"register": "FREND1",                "description": "Front end RX configuration"},
    0x22: {"register": "FREND0",                "description": "Front end TX configuration"},
    0x23: {"register": "FSCAL3",                "description": "Frequency synthesizer calibration"},
    0x24: {"register": "FSCAL2",                "description": "Frequency synthesizer calibration"},
    0x25: {"register": "FSCAL1",                "description": "Frequency synthesizer calibration"},
    0x26: {"register": "FSCAL0",                "description": "Frequency synthesizer calibration"},
    0x27: {"register": "RCCTRL1",               "description": "RC oscillator configuration"},
    0x28: {"register": "RCCTRL0",               "description": "RC oscillator configuration"},
    0x29: {"register": "FSTEST",                "description": "Frequency synthesizer calibration control"},
    0x2A: {"register": "PTEST",                 "description": "Production test"},
    0x2B: {"register": "AGCTEST",               "description": "AGC test"},
    0x2C: {"register": "TEST2",                 "description": "Various test settings"},
    0x2D: {"register": "TEST1",                 "description": "Various test settings"},
    0x2E: {"register": "TEST0",                 "description": "Various test settings"}
}

# Table 42: Command Strobes
COMMAND_REGISTERS = {
    0x30: {"register": "SRES",                  "description": "Reset chip."},
    0x31: {"register": "SFSTXON",               "description": "Enable and calibrate frequency synthesizer (if MCSM0.FS_AUTOCAL=1). If in RX (with CCA): Go to a wait state where only the synthesizer is running (for quick RX / TX turnaround)."},
    0x32: {"register": "SXOFF",                 "description": "Turn off crystal oscillator."},
    0x33: {"register": "SCAL",                  "description": "Calibrate frequency synthesizer and turn it off. SCAL can be strobed from IDLE mode without setting manual calibration mode (MCSM0.FS_AUTOCAL=0)"},
    0x34: {"register": "SRX",                   "description": "Enable RX. Perform calibration first if coming from IDLE and MCSM0.FS_AUTOCAL=1."},
    0x35: {"register": "STX",                   "description": "In IDLE state: Enable TX. Perform calibration first if MCSM0.FS_AUTOCAL=1. If in RX state and CCA is enabled: Only go to TX if channel is clear."},
    0x36: {"register": "SIDLE",                 "description": "Exit RX / TX, turn off frequency synthesizer and exit Wake-On-Radio mode if applicable."},
    0x38: {"register": "SWOR",                  "description": "Start automatic RX polling sequence (Wake-on-Radio) as described in Section 19.5 if WORCTRL.RC_PD=0."},
    0x39: {"register": "SPWD",                  "description": "Enter power down mode when CSn goes high."},
    0x3A: {"register": "SFRX",                  "description": "Flush the RX FIFO buffer. Only issue SFRX in IDLE or RXFIFO_OVERFLOW states."},
    0x3B: {"register": "SFTX",                  "description": "Flush the TX FIFO buffer. Only issue SFTX in IDLE or TXFIFO_UNDERFLOW states."},
    0x3C: {"register": "SWORRST",               "description": "Reset real time clock to Event1 value."},
    0x3D: {"register": "SNOP",                  "description": "No operation. May be used to get access to the chip status byte."},
}

# Table 44: Status Registers Overview
STATUS_REGISTERS = {
    0x30: {"register": "PARTNUM",               "description": "Part number for CC1101"},
    0x31: {"register": "VERSION",               "description": "Current version number"},
    0x32: {"register": "FREQEST",               "description": "Frequency Offset Estimate"},
    0x33: {"register": "LQI",                   "description": "Demodulator estimate for Link Quality"},
    0x34: {"register": "RSSI",                  "description": "Received signal strength indication"},
    0x35: {"register": "MARCSTATE",             "description": "Control state machine state"},
    0x36: {"register": "WORTIME1",              "description": "High byte of WOR timer"},
    0x37: {"register": "WORTIME0",              "description": "Low byte of WOR timer"},
    0x38: {"register": "PKTSTATUS",             "description": "Current GDOx status and packet status"},
    0x39: {"register": "VCO_VC_DAC",            "description": "Current setting from PLL calibration module"},
    0x3A: {"register": "TXBYTES",               "description": "Underflow and number of bytes in the TX FIFO"},
    0x3B: {"register": "RXBYTES",               "description": "Overflow and number of bytes in the RX FIFO"},
    0x3C: {"register": "RCCTRL1_STATUS",        "description": "Last RC oscillator calibration result"},
    0x3D: {"register": "RCCTRL0_STATUS",        "description": "Last RC oscillator calibration result"},
}

# 0x35 (0xF5): MARCSTATE – Main Radio Control State Machine State
# MARC_STATE[4:0] - R - Main Radio Control FSM State
# Note: it is not possible to read back the SLEEP or XOFF state numbers because setting CSn low will make the chip enter the IDLE mode from the SLEEP or XOFF states.
MARC_STATE = {
    # Value: {State name, State (Figure 25, page 50) }
    0x00: {"state_name": "SLEEP",               "state": "SLEEP"},
    0x01: {"state_name": "IDLE",                "state": "IDLE"},
    0x02: {"state_name": "XOFF",                "state": "XOFF"},
    0x03: {"state_name": "VCOON_MC",            "state": "MANCAL"},
    0x04: {"state_name": "REGON_MC",            "state": "MANCAL"},
    0x05: {"state_name": "MANCAL",              "state": "MANCAL"},
    0x06: {"state_name": "VCOON",               "state": "FS_WAKEUP"},
    0x07: {"state_name": "REGON",               "state": "FS_WAKEUP"},
    0x08: {"state_name": "STARTCAL",            "state": "CALIBRATE"},
    0x09: {"state_name": "BWBOOST",             "state": "SETTLING"},
    0x0A: {"state_name": "FS_LOCK",             "state": "SETTLING"},
    0x0B: {"state_name": "IFADCON",             "state": "SETTLING"},
    0x0C: {"state_name": "ENDCAL",              "state": "CALIBRATE"},
    0x0D: {"state_name": "RX",                  "state": "RX"},
    0x0E: {"state_name": "RX_END",              "state": "RX"},
    0x0F: {"state_name": "RX_RST",              "state": "RX"},
    0x10: {"state_name": "TXRX_SWITCH",         "state": "TXRX_SETTLING"},
    0x11: {"state_name": "RXFIFO_OVERFLOW",     "state": "RXFIFO_OVERFLOW"},
    0x12: {"state_name": "FSTXON",              "state": "FSTXON"},
    0x13: {"state_name": "TX",                  "state": "TX"},
    0x14: {"state_name": "TX_END",              "state": "TX"},
    0x15: {"state_name": "RXTX_SWITCH",         "state": "RXTX_SETTLING"},
    0x16: {"state_name": "TXFIFO_UNDERFLOW",    "state": "TXFIFO_UNDERFLOW"},
}

MULTI_BYTE_REGISTERS = {
    0x3E: {"register": "PATABLE",               "description": "PA Table"},
    0x3F: {"register": "TX/RX FIFO",            "description": "Tx / Rx FIFO"},
}

# Table 23: Status Byte Summary (bit masks)
STATUS_BYTE = {
    0x80: {"name": "CHIP_RDYn",                 "description": "Stays high until power and crystal have stabilized. Should always be low when using the SPI interface."},
    0x70: {"name": "STATE",                     "description": "Indicates the current main state machine mode"},
    0x0F: {"name": "FIFO_BYTES_AVAILABLE",      "description": "The number of bytes available in the RX FIFO or free bytes in the TX FIFO"},
}

STATE_BITS = {
    0b000: {"state": "IDLE",                    "description": "IDLE state (Also reported for some transitional states instead of SETTLING or CALIBRATE)"},
    0b001: {"state": "RX",                      "description": "Receive mode"},
    0b010: {"state": "TX",                      "description": "Transmit mode"},
    0b011: {"state": "FSTXON",                  "description": "Fast TX ready"},
    0b100: {"state": "CALIBRATE",               "description": "Frequency synthesizer calibration is running"},
    0b101: {"state": "SETTLING",                "description": "PLL is settling"},
    0b110: {"state": "RXFIFO_OVERFLOW",         "description": "RX FIFO has overflowed. Read out any useful data, then flush the FIFO with SFRX"},
    0b111: {"state": "TXFIFO_UNDERFLOW",        "description": "TX FIFO has underflowed. Acknowledge with SFTX"},
}


class ProtocolException(Exception):
    pass

class ProtocolFrameType:
    REGISTER = "register"
    COMMAND = "cmd"
    STATUS = "status"
    PA_TABLE = "pa table"
    FIFO = "fifo"
    ERROR = "protocol error"

class CC1101SpiProtocol:
    PROTOCOL_MSG = {
        "request": None,
        "response": None,
    }
    REQUEST = {
        "type": None,
        "access": None,
        "burst": None,
        "register": None,
        "data": None,
        "description": None,
        "error": None,
    }
    RESPONSE = {
        "status": None,
        "data": None,
        "error": None,
    }
    STATUS = {
        "chip_rdy": None,
        "state": None,
        "fifo_bytes_available": None,
    }

    def __init__(self):
        pass

    def process_frame(self, protocol_frame):
        protocol_msg = deepcopy(self.PROTOCOL_MSG)

        if len(protocol_frame) > 0:
            # Interpret Request
            protocol_msg["request"] = self.interpret_request(self.get_mosi_data(protocol_frame))

            if self.is_read_access(protocol_frame):
                # Interpret Response
                protocol_msg["response"] = self.interpret_response(self.get_miso_data(protocol_frame))
        return protocol_msg

    def is_read_access(self, protocol_frame):
        return (protocol_frame[0]["mosi"] & 0x80) != 0

    def get_mosi_data(self, protocol_frame):
        return [x["mosi"] for x in protocol_frame]

    def get_miso_data(self, protocol_frame):
        return [x["miso"] for x in protocol_frame]

    def is_read(self, data_byte):
        return True if (data_byte & 0x80) != 0 else False

    def is_write(self, data_byte):
        return True if (data_byte & 0x80) == 0 else False

    def is_burst(self, data_byte):
        return True if (data_byte & 0x40) != 0 else False

    def interpret_register(self, data_byte):
        register = None
        address = data_byte & 0x3F
        frame_type = None
        error = None

        if address < 0x30:
            frame_type = ProtocolFrameType.REGISTER
            register = CONFIG_REGISTERS[address]
        elif address == 0x3E:
            frame_type = ProtocolFrameType.PA_TABLE
            register = MULTI_BYTE_REGISTERS[address]
        elif address == 0x3F:
            frame_type = ProtocolFrameType.FIFO
            register = MULTI_BYTE_REGISTERS[address]
        elif self.is_read(data_byte) and self.is_burst(data_byte):
            frame_type = ProtocolFrameType.STATUS
            register = STATUS_REGISTERS[address]
        elif address <= 0x3D:
            if address != 0x37:
                frame_type = ProtocolFrameType.COMMAND
                register = COMMAND_REGISTERS[address]
            else:
                frame_type = ProtocolFrameType.ERROR
                error = "Invalid COMMAND"
        elif address > 0x3D:
            frame_type = ProtocolFrameType.ERROR
            error = "Invalid ADDRESS"

        return frame_type, register["register"], register["description"], error

    def interpret_request(self, data):
        request = deepcopy(self.REQUEST)

        # Access mode
        request["access"] = "W" if self.is_write(data[0]) else "R"
        request["burst"] = "B" if self.is_burst(data[0]) else ""

        # Register address
        request["type"], request["register"], request["description"], request["error"] = self.interpret_register(data[0])

        # Data Byte
        if len(data) > 1:
            request["data"] = data[1:]

        return request

    def interpret_status(self, status_byte):
        status = deepcopy(self.STATUS)
        status["chip_rdy"] = False if (status_byte & 0x80) != 0 else True
        status["state"] = STATE_BITS[(status_byte & 0x70) >> 4]["state"]
        status["fifo_bytes_available"] = (status_byte & 0x0F)
        return status

    def interpret_response(self, data):
        response = deepcopy(self.RESPONSE)

        # Status Byte
        response["status"] = self.interpret_status(data[0])

        # Data byte
        response["data"] = data[1:]

        return response
