#!/usr/bin/env python3
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
        Initialize I2C connection to UBLOX GPS module
        
        Args:
            bus_num: I2C bus number (usually 1 on Raspberry Pi)
            address: I2C address (default 0x42 for UBLOX)
        """
        self.bus = smbus.SMBus(bus_num)
        self.address = address
        self.buffer = b''
        
    def data_available(self):
        """Check how many bytes are available to read"""
        try:
            # Read registers 0xFD and 0xFE for available byte count
            high = self.bus.read_byte_data(self.address, 0xFD)
            low = self.bus.read_byte_data(self.address, 0xFE)
            return (high << 8) | low
        except Exception as e:
            print(f"Error checking data availability: {e}")
            return 0
    
    def read_data(self, num_bytes=32):
        """Read raw data from GPS module"""
        try:
            # Read from data stream register (0xFF)
            data = self.bus.read_i2c_block_data(self.address, 0xFF, num_bytes)
            return bytes(data)
        except Exception as e:
            print(f"Error reading data: {e}")
            return b''
    
    def get_nmea_sentences(self):
        """Read and parse NMEA sentences"""
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
            
            return sentences
        return []
    
    def parse_gga(self, sentence):
        """Parse GGA (Global Positioning System Fix Data) sentence"""
        parts = sentence.split(',')
        if len(parts) < 15 or not parts[0].endswith('GGA'):
            return {}
        
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
                
        except (ValueError, IndexError):
            pass
        
        return data
    
    def parse_rmc(self, sentence):
        """Parse RMC (Recommended Minimum) sentence"""
        parts = sentence.split(',')
        if len(parts) < 12 or not parts[0].endswith('RMC'):
            return {}
        
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
            pass
        
        return data
    
    def parse_gps_data(self):
        """Get parsed GPS data from NMEA sentences"""
        sentences = self.get_nmea_sentences()
        gps_data = {}
        
        for sentence in sentences:
            if 'GGA' in sentence:
                gga_data = self.parse_gga(sentence)
                gps_data.update(gga_data)
            elif 'RMC' in sentence:
                rmc_data = self.parse_rmc(sentence)
                gps_data.update(rmc_data)
        
        return gps_data


def poll_gps(timeout_seconds=20, max_no_fix_cycles=10):
    """
    Example usage
    
    Args:
        timeout_seconds: Maximum time to wait for initial GPS fix (default 300s = 5 min)
        max_no_fix_cycles: Maximum iterations without a fix before giving up (default 100)
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
            
            data = gps.parse_gps_data()
            
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
    except Exception as e:
        raise
