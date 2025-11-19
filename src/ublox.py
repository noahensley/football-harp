"""
UBLOX Max M8Q GPS Module - I2C Communication
Reads GPS data via I2C and parses NMEA sentences manually
No external dependencies required (except smbus)

Troubleshooting tips:
    1. Check I2C is enabled: sudo raspi-config
    2. Check device is detected: i2cdetect -y 1
    3. Install smbus: sudo apt-get install python3-smbus
    4. Make sure EN pin is connected to 3.3V
"""

import smbus
import time

from config import DEBUG_MODE


class UBLOX_I2C:

    def __init__(self, bus_num=1, address=0x42):
        """
        Initializes an I2C connection to UBLOX GPS module.
        
        param bus_num: I2C bus number (usually 1 on Raspberry Pi)
        param address: I2C address (default 0x42 for UBLOX)
        """
        self.bus = smbus.SMBus(bus_num)
        self.address = address
        self.buffer = b''

        
    def data_available(self):
        """
        Checks how many bytes are available to read.

        returns: The data available bit status
        """
        try:
            # Read registers 0xFD and 0xFE for available byte count
            high = self.bus.read_byte_data(self.address, 0xFD)
            low = self.bus.read_byte_data(self.address, 0xFE)
            return (high << 8) | low
        except Exception:
            raise
        
    
    def read_data(self, num_bytes=32):
        """
        Reads raw data from GPS module.

        param num_bytes: The number of bytes to read
        """
        try:
            # Read from data stream register (0xFF)
            data = self.bus.read_i2c_block_data(self.address, 0xFF, num_bytes)
            return bytes(data)
        except Exception:
            raise
        
    
    def get_nmea_sentences(self):
        """
        Fetches a collection of NMEA sentences.

        returns: A collection of NMEA sentence byte data decoded into ASCII
        """
        try:
            available = self.data_available()
        
            if available > 0:
                # Read available data (max 32 bytes at a time due to I2C limitation)
                chunk_size = min(available, 32)
                data = self.read_data(chunk_size)
                self.buffer += data
                
                # Process complete NMEA sentences
                sentences = []
                while b'\n' in self.buffer:
                    line, self.buffer = self.buffer.split(b'\n', 1)
                    try:
                        sentence = line.decode('ascii', errors='ignore').strip()
                        if sentence.startswith('$'):
                            sentences.append(sentence)
                    except Exception:
                        pass
            
        except Exception:
            raise

        return sentences
    
    
    def parse_gga(self, sentence):
        """
        Parses GGA (Global Positioning System Fix Data) sentence.

        param sentence: The GGA sentence to be parsed
            (Follows standard GGA Sentence structure
                Source: https://docs.fixposition.com/fd/nmea-gp-gga)
        returns: A collection of parsed data from the GGA sentence
        """
        if type(sentence) != str:
            raise TypeError("Input GGA sentence must be a string.")
        parts = sentence.split(',')
        if len(parts) < 15 or not parts[0].endswith('GGA'):
            raise ValueError("Input GGA sentence is incomplete.")
        
        data = {}
        try:
            # Time (hhmmss.ss)
            if parts[1]:
                data['time'] = parts[1]
            
            # Latitude
            if parts[2] and parts[3]:
                lat = float(parts[2][:2]) + float(parts[2][2:]) / 60.0
                if parts[3] == 'S':
                    lat = -lat
                data['latitude'] = lat
            
            # Longitude
            if parts[4] and parts[5]:
                lon = float(parts[4][:3]) + float(parts[4][3:]) / 60.0
                if parts[5] == 'W':
                    lon = -lon
                data['longitude'] = lon
            
            # Fix quality (0=no fix, 1=GPS, 2=DGPS)
            if parts[6]:
                data['fix_quality'] = int(parts[6])
            
            # Number of satellites
            if parts[7]:
                data['num_sats'] = int(parts[7])
            
            # Horizontal dilution of precision
            if parts[8]:
                data['hdop'] = float(parts[8])
            
            # Altitude
            if parts[9]:
                data['altitude'] = float(parts[9])
                
        except Exception:
            raise
        
        return data
    
    
    def parse_rmc(self, sentence):
        """
        Parses RMC (Recommended Minimum) sentence.

        param sentence: The RMC sentence to be parsed
            (Follow standard RMC sentence structure
                Source: https://docs.fixposition.com/fd/nmea-gp-rmc)
        returns: A collection of parsed data from the RMC sentence
        """
        if type(sentence) != str:
            raise TypeError("Input RMC sentence must be a string.")
        parts = sentence.split(',')
        if len(parts) < 12 or not parts[0].endswith('RMC'):
            raise ValueError("Input RMC sentence is incomplete.")
        
        data = {}
        try:
            # Status (A=active, V=void)
            if parts[2]:
                data['status'] = parts[2]
            
            # Speed over ground (knots)
            if parts[7]:
                data['speed_knots'] = float(parts[7])
            
            # Course over ground (degrees)
            if parts[8]:
                data['course'] = float(parts[8])
            
            # Date (ddmmyy)
            if parts[9]:
                data['date'] = parts[9]
                
        except (ValueError, IndexError):
            raise
        
        return data
    
    
    def parse_gps_data(self):
        """
        Parses GPS data from NMEA GGA or NMEA RMC sentences.

        returns: A collection of parsed GPS data.
        """
        try:
            sentences = self.get_nmea_sentences()
            gps_data = {}
            
            for sentence in sentences:
                if 'GGA' in sentence:
                    gga_data = self.parse_gga(sentence)
                    gps_data.update(gga_data)
                elif 'RMC' in sentence:
                    rmc_data = self.parse_rmc(sentence)
                    gps_data.update(rmc_data)
        
        except Exception:
            raise

        return gps_data


def poll_gps(timeout_seconds=20, max_no_fix_cycles=10):
    """
    Polls the GPS module for positional data.

    param timeout_seconds: Maximum time to wait for initial GPS fix
    param max_no_fix_cycles: Maximum iterations without a fix before giving up
    """
    try:
        print("[UBLOX] Polling GPS...", end="")
        gps = UBLOX_I2C(bus_num=1, address=0x42)
        if DEBUG_MODE:
            print("\nGPS module connected!")
            print(f"Waiting for GPS fix (timeout: {timeout_seconds}s)...")
        
        start_time = time.time()
        last_fix = 0
        no_fix_count = 0
        got_first_fix = False
        data = {}
        
        while True:
            # Check timeout
            elapsed = time.time() - start_time
            if not got_first_fix and elapsed > timeout_seconds:
                raise RuntimeError(f"Timeout: No GPS fix after {timeout_seconds} seconds.")
            
            try:
                data = gps.parse_gps_data()
            except Exception:
                pass
            
            if data:
                # Only print when we have a fix
                has_fix = data.get('fix_quality', 0) > 0
                
                if has_fix:
                    got_first_fix = True
                    no_fix_count = 0
                    print("DONE")
                    return data                 
                else:
                    # No fix in this cycle
                    no_fix_count += 1
                    
                    # Check if we've lost fix for too long (after having a fix)
                    if got_first_fix and no_fix_count > max_no_fix_cycles:
                        raise RuntimeError(f"Lost GPS fix for {max_no_fix_cycles} cycles.")
                    
                    if time.time() - last_fix > 5:
                        # Print waiting message every 5 seconds if no fix
                        print(".", end="", flush=True)
                        last_fix = time.time()
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        raise
    except Exception:
        raise
