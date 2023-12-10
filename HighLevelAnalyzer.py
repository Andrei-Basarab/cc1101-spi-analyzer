# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting
from copy import deepcopy
from CC1101SpiProtocol import CC1101SpiProtocol, ProtocolFrameType, MARC_STATE


SPI_DATA_FRAME = {"mosi": 0, "miso": 0}


class SpiFrameType:
    error = "error"
    enable = "enable"
    disable = "disable"
    result = "result"

class SpiFrameState:
    idle = 0
    start = 1
    active = 2
    end = 3
    error = 4

# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    # List of settings that a user can set for this High Level Analyzer.
    # TODO Check the String/Number/Choice settings
    # my_string_setting = StringSetting()
    # my_number_setting = NumberSetting(min_value=0, max_value=100)
    # my_choices_setting = ChoicesSetting(choices=('A', 'B'))

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'spi error': {
            'format': 'Error: {{type}}'
        },
        ProtocolFrameType.ERROR: {
            'format': 'Error: {{type}}'
        },
        ProtocolFrameType.REGISTER: {
            'format': 'Register: {{data.access}} | {{data.register}} = {{data.focus_data}}'
        },
        ProtocolFrameType.COMMAND: {
            'format': 'Command: {{data.register}}'
        },
        ProtocolFrameType.STATUS: {
            'format': 'Status: {{data.register}} = {{data.focus_data}}'
        },
        ProtocolFrameType.PA_TABLE: {
            'format': 'PA Table: {{data.access}} = {{data.focus_data}}'
        },
        ProtocolFrameType.FIFO: {
            'format': 'FIFO: {{data.access}} = {{data.focus_data}}'
        },
    }

    def __init__(self):
        '''
        Initialize HLA.
        Settings can be accessed using the same name used above.
        '''
        self.state = SpiFrameState.idle
        self.spi_frame_queue = []
        self.protocol = CC1101SpiProtocol()
        self.start_time = 0
        self.end_time = 0

        # TODO Check the String/Number/Choice settings
        # print(
        #     "Settings:",
        #     self.my_string_setting,
        #     self.my_number_setting,
        #     self.my_choices_setting
        # )

    def decode(self, frame: AnalyzerFrame):
        '''
        Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.
        The type and data values in `frame` will depend on the input analyzer.
        '''
        # Return the data frame itself
        return self.frame_state_machine(frame)

    def frame_state_machine(self, frame):
        return_frame = None

        # Check for error frames
        if frame.type == SpiFrameType.error:
            self.state = SpiFrameState.error
            return_frame = AnalyzerFrame("spi error", frame.start_time, frame.end_time, {"error_details": "clock in wrong state when enable signal became active"})

        # Check Idle state
        if self.state == SpiFrameState.idle:
            if frame.type == SpiFrameType.enable:
                self.start_time = frame.start_time  # Log start time
                self.state = SpiFrameState.start
            else:
                self.state = SpiFrameState.error

        # Check Start state
        elif self.state == SpiFrameState.start:
            if frame.type == SpiFrameType.result:
                self.start_time = frame.start_time  # Log start time
                self.end_time = frame.end_time      # Log end time
                self.state = SpiFrameState.active
            elif frame.type == SpiFrameType.disable:
                self.end_time = frame.end_time      # Log end time
                self.state = SpiFrameState.error
                return_frame = AnalyzerFrame("spi error", self.start_time, self.end_time, {"error_details": "no SPI frame"})
            else:
                self.state = SpiFrameState.error

        # Check Active state
        elif self.state == SpiFrameState.active:
            if frame.type == SpiFrameType.disable:
                self.state = SpiFrameState.end
            elif frame.type == SpiFrameType.result:
                self.end_time = frame.end_time      # Log end time
            else:
                self.state = SpiFrameState.error

        # Execute Active state
        if self.state == SpiFrameState.active:
            self.spi_frame_queue.append(self.get_spi_data_frame(frame))

        # Execute End state
        if self.state == SpiFrameState.end:
            if len(self.spi_frame_queue) > 0:
                protocol_msg = self.protocol.process_frame(self.spi_frame_queue)
                frame_type, frame_data = self.construct_table(protocol_msg)
                return_frame = AnalyzerFrame(frame_type, self.start_time, self.end_time, frame_data)

            self.spi_frame_queue.clear()

            # Automatic transition
            self.state = SpiFrameState.idle

        # Execute Error state
        elif self.state == SpiFrameState.error:

            # Automatic transition
            self.state = SpiFrameState.idle

        return return_frame

    def construct_table(self, protocol_msg):
        frame_type           = protocol_msg["request"]["type"]
        access               = protocol_msg["request"]["access"]
        burst                = protocol_msg["request"]["burst"]
        register             = protocol_msg["request"]["register"]
        request_data         = protocol_msg["request"]["data"]
        write_data           = "" if request_data is None else " ".join(["{:02X}".format(x) for x in request_data])
        response             = protocol_msg["response"]
        chip_ready           = "" if response is None else "OK" if response["status"]["chip_rdy"] else "NOT RDY"
        state                = "" if response is None else response["status"]["state"]
        fifo_bytes_available = "" if response is None else "{}".format(response["status"]["fifo_bytes_available"])
        read_data            = "" if response is None else " ".join(["{:02X}".format(x) for x in response["data"]])
        description          = protocol_msg["request"]["description"]

        # Focus Data is used mainly for the Protocol UI labels
        if frame_type == ProtocolFrameType.ERROR:
            focus_data = ""
        elif frame_type == ProtocolFrameType.REGISTER:
            focus_data = write_data if access == "W" else read_data
        elif frame_type == ProtocolFrameType.COMMAND:
            focus_data = ""
        elif frame_type == ProtocolFrameType.STATUS:
            if register == "MARCSTATE":
                focus_data = MARC_STATE[response["data"][0]]["state"]
            else:
                focus_data = read_data
        elif frame_type == ProtocolFrameType.PA_TABLE:
            focus_data = write_data if access == "W" else read_data
        elif frame_type == ProtocolFrameType.FIFO:
            focus_data = write_data if access == "W" else read_data

        return (
            frame_type,
            {
                "raw_data":             self.raw_data(),
                "access":               access,
                "burst":                burst,
                "register":             register,
                "write_data":           write_data,
                "chip_ready":           chip_ready,
                "state":                state,
                "fifo_bytes_available": fifo_bytes_available,
                "read_data":            read_data,
                "register_description": description,
                "focus_data":           focus_data,
                "error_details":        "",
            }
        )

    def from_byte(self, data_raw):
        return int.from_bytes(data_raw, "big")

    def get_spi_data_frame(self, frame):
        spi_data_frame = deepcopy(SPI_DATA_FRAME)
        spi_data_frame["mosi"] = self.from_byte(frame.data["mosi"])
        spi_data_frame["miso"] = self.from_byte(frame.data["miso"])
        return spi_data_frame

    def raw_data(self):
        content = "["
        for frame in self.spi_frame_queue:
            content += "({:02X}, {:02X}) ".format(frame["mosi"], frame["miso"])
        return content.rstrip() + "]"
