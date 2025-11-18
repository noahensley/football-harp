#!/usr/bin/env python3
"""
UBLOX Max M8Q GPS Module - I2C Communication
Reads GPS data via I2C and parses NMEA sentences manually
No external dependencies required (except smbus)
"""

import smbus
import time

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


def main(timeout_seconds=20, max_no_fix_cycles=10):
    """
    Example usage
    
    Args:
        timeout_seconds: Maximum time to wait for initial GPS fix (default 300s = 5 min)
        max_no_fix_cycles: Maximum iterations without a fix before giving up (default 100)
    """
    print("Initializing UBLOX GPS on I2C...")
    
    try:
        gps = UBLOX_I2C(bus_num=1, address=0x42)
        print("GPS module connected!")
        print(f"Waiting for GPS fix (timeout: {timeout_seconds}s)...\n")
        
        start_time = time.time()
        last_fix = 0
        no_fix_count = 0
        got_first_fix = False
        
        while True:
            # Check timeout
            elapsed = time.time() - start_time
            if not got_first_fix and elapsed > timeout_seconds:
                print(f"\n\nTimeout: No GPS fix after {timeout_seconds} seconds.")
                print("Make sure antenna has clear view of sky.")
                return False
            data = gps.parse_gps_data()
            
            if data:
                # Only print when we have a fix
                has_fix = data.get('fix_quality', 0) > 0
                
                if has_fix:
                    got_first_fix = True
                    no_fix_count = 0
                    print("\n" + "="*50)
                    
                    if 'latitude' in data and 'longitude' in data:
                        print(f"Position: {data['latitude']:.6f}, {data['longitude']:.6f}")
                    
                    if 'altitude' in data:
                        print(f"Altitude: {data['altitude']:.1f} m")
                    
                    if 'num_sats' in data:
                        print(f"Satellites: {data['num_sats']}")
                    
                    if 'fix_quality' in data:
                        quality_names = {0: 'No fix', 1: 'GPS fix', 2: 'DGPS fix'}
                        print(f"Fix quality: {quality_names.get(data['fix_quality'], 'Unknown')}")
                    
                    if 'hdop' in data:
                        print(f"HDOP: {data['hdop']:.1f}")
                    
                    if 'speed_knots' in data:
                        print(f"Speed: {data['speed_knots']:.1f} knots ({data['speed_knots'] * 1.852:.1f} km/h)")
                    
                    if 'course' in data:
                        print(f"Course: {data['course']:.1f}°")
                    
                    if 'time' in data:
                        time_str = data['time']
                        if len(time_str) >= 6:
                            hh = time_str[0:2]
                            mm = time_str[2:4]
                            ss = time_str[4:6]
                            print(f"UTC Time: {hh}:{mm}:{ss}")
                    
                    if 'date' in data:
                        date_str = data['date']
                        if len(date_str) >= 6:
                            dd = date_str[0:2]
                            mm = date_str[2:4]
                            yy = date_str[4:6]
                            print(f"Date: {dd}/{mm}/{yy}")
                    
                    last_fix = time.time()
                    
                else:
                    # No fix in this cycle
                    no_fix_count += 1
                    
                    # Check if we've lost fix for too long (after having a fix)
                    if got_first_fix and no_fix_count > max_no_fix_cycles:
                        print(f"\n\nLost GPS fix for {max_no_fix_cycles} cycles. Exiting.")
                        return False
                    
                    if time.time() - last_fix > 5:
                        # Print waiting message every 5 seconds if no fix
                        print(".", end="", flush=True)
                        last_fix = time.time()
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\nExiting...")
        return True
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check I2C is enabled: sudo raspi-config")
        print("2. Check device is detected: i2cdetect -y 1")
        print("3. Install smbus: sudo apt-get install python3-smbus")
        print("4. Make sure EN pin is connected to 3.3V")
        return False
