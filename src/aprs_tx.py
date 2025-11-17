#!/usr/bin/env python3
# TODO:
# Currently only using VOX to key transmitter
import socket
import time
import struct
#from pathlib import Path - Use if telemetry is also logged

from debug import DEBUG_MODE


def create_aprs_packet(callsign, ssid, telemetry, message=""):
    """
    Creates an APRS packet string for transmission.
    
    Args:
        callsign: Station callsign (e.g., "N0CALL")
        ssid: SSID (e.g., "11")
        telemetry: Dictionary containing sensor data including lat/lon
        message: Optional message text
        
    Returns:
        str: APRS packet in TNC2 format
    """
    print("[APRS_Tx] Creating APRS packet...", end="")
    
    try:
        # Extract position from telemetry
        lat = telemetry["VFAN"]["Latitude"]
        lon = telemetry["VFAN"]["Longitude"]
        
        # Build telemetry string
        telemetry_list = []
        for sensor in telemetry.keys():
            for data in telemetry[sensor].keys():
                if data not in ["Latitude", "Longitude"]:  # Skip position data
                    telemetry_list.append(f"{data}={telemetry[sensor][data]}")
        
        telemetry_string = ", ".join(telemetry_list)
        
        # Construct APRS packet in TNC2 format
        source = f"{callsign}-{ssid}"
        # Position report with timestamp and comment
        packet = f"{source}>APRS,WIDE1-1:!{lat}/{lon}>{telemetry_string} {message}".strip()
        
        if DEBUG_MODE:
            print(f"\n\tPacket: {packet}")
        else:
            print("DONE")
        return packet
        
    except Exception as e:
        raise Exception("Unable to create APRS packet", e)


def encode_kiss_frame(packet):
    """
    Encode an APRS packet into a KISS frame for transmission.
    
    Args:
        packet: APRS packet string in TNC2 format
        
    Returns:
        bytes: KISS-encoded frame
    """
    FEND = 0xC0  # Frame End
    FESC = 0xDB  # Frame Escape
    TFEND = 0xDC  # Transposed Frame End
    TFESC = 0xDD  # Transposed Frame Escape
    
    # Command byte: 0x00 = data frame on port 0
    frame = bytearray([FEND, 0x00])
    
    # Add the packet data (direwolf will parse TNC2 format)
    data = packet.encode('ascii')
    
    # Escape special characters
    for byte in data:
        if byte == FEND:
            frame.extend([FESC, TFEND])
        elif byte == FESC:
            frame.extend([FESC, TFESC])
        else:
            frame.append(byte)
    
    # End frame
    frame.append(FEND)
    
    return bytes(frame)


def transmit_via_direwolf_kiss(packet, kiss_host='localhost', kiss_port=8001):
    """
    Transmit APRS packet via existing direwolf service using KISS protocol.
    
    Args:
        packet: APRS packet string in TNC2 format
        kiss_host: Direwolf KISS server hostname
        kiss_port: Direwolf KISS TCP port (default 8001)
    """
    if DEBUG_MODE:
        print(f"[APRS_Tx] Connecting to direwolf KISS interface at {kiss_host}:{kiss_port}...", end="")
    
    sock = None
    try:
        # Connect to direwolf KISS interface
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((kiss_host, kiss_port))
        
        if DEBUG_MODE:
            print("[APRS_Tx] DONE")
        
        # Encode and send packet
        kiss_frame = encode_kiss_frame(packet)
        if DEBUG_MODE:
            print("[APRS_Tx] Sending...", end="")
        sock.sendall(kiss_frame)
        
        if DEBUG_MODE:
            print(f"DONE.\n\tSent {len(kiss_frame)} bytes to direwolf")
        
        # Wait for transmission to complete
        # Direwolf will handle the actual transmission timing and PTT
        time.sleep(1.0)  # Adjust based on typical packet length
        
        if DEBUG_MODE:
            print("[APRS_Tx] Transmission complete")
        
    except ConnectionRefusedError:
        raise Exception(
            f"Cannot connect to direwolf on {kiss_host}:{kiss_port}. "
            "Ensure direwolf service is running and KISS is enabled in config."
        )
    except socket.timeout:
        raise Exception("Connection to direwolf timed out")
    except Exception as e:
        raise Exception("Transmission error:", e)
    finally:
        if sock:
            sock.close()


def transmit_via_direwolf_agw(packet, agw_host='localhost', agw_port=8000):
    """
    Transmit APRS packet via existing direwolf service using AGW protocol.
    Alternative to KISS, may be easier for some applications.
    
    Args:
        packet: APRS packet string in TNC2 format
        agw_host: Direwolf AGW server hostname
        agw_port: Direwolf AGW TCP port (default 8000)
    """
    if DEBUG_MODE:
        print(f"Connecting to direwolf AGW interface at {agw_host}:{agw_port}...", end="")
    
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((agw_host, agw_port))
        
        if DEBUG_MODE:
            print("DONE")
        
        # AGW 'K' frame = send unproto (UI) frame
        # This is a simplified implementation
        parts = packet.split(':', 1)
        if len(parts) != 2:
            raise ValueError("Invalid packet format")
        
        header = parts[0]
        info = parts[1]
        
        # Send raw packet (direwolf AGW accepts TNC2 format)
        # Frame format: 'K' command with radio port 0
        agw_frame = bytearray()
        agw_frame.extend(b'K')  # Unproto frame type
        agw_frame.extend(struct.pack('<I', 0))  # Port number
        agw_frame.extend(packet.encode('ascii'))
        
        sock.sendall(agw_frame)
        
        time.sleep(1.0)
        
        if DEBUG_MODE:
            print("[APRS_Tx] Transmission complete")
        
    except ConnectionRefusedError:
        raise Exception(
            f"Cannot connect to direwolf on {agw_host}:{agw_port}. "
            "Ensure direwolf service is running and AGWPE is enabled in config."
        )
    except Exception as e:
        raise Exception("Transmission error:", e)
    finally:
        if sock:
            sock.close()


def transmit_aprs(callsign, ssid, telemetry, message="",
                  interface='kiss',  # 'kiss' or 'agw'
                  kiss_host='localhost', kiss_port=8001,
                  agw_host='localhost', agw_port=8000):
    """
    Complete APRS transmission workflow via running direwolf service.
    
    Note: PTT is handled by direwolf configuration. Ensure direwolf.conf
    has PTT configured (e.g., "PTT GPIO 17") or use VOX on your radio.
    
    Args:
        callsign: Station callsign
        ssid: SSID
        telemetry: Telemetry dictionary
        message: Optional message
        interface: 'kiss' or 'agw' (KISS recommended)
        kiss_host/kiss_port: KISS interface settings
        agw_host/agw_port: AGW interface settings
    """
    try:
        # Create packet
        print("[APRS_Tx] Creating APRS packet...", end="")
        packet = create_aprs_packet(callsign, ssid, telemetry, message)
        print("DONE")
        # Transmit via selected interface
        # Direwolf handles PTT based on its configuration
        print("[APRS_Txt] Transmitting...", end="")
        if interface == 'kiss':
            transmit_via_direwolf_kiss(packet, kiss_host, kiss_port)
        elif interface == 'agw':
            transmit_via_direwolf_agw(packet, agw_host, agw_port)
        else:
            raise ValueError(f"Invalid interface: {interface}")
        
        print("DONE")
        
    except Exception as e:
        raise Exception(e)


# Test
if __name__ == "__main__":
    # Example telemetry data (format should not matter, it's byte-encoded)
    test_telemetry = {
        "VFAN": {
            "Latitude": "4903.50N",
            "Longitude": "07201.75W",
            "Altitude": "123m"
        },
        "Sensors": {
            "Temp": "25C",
            "Battery": "12.6V"
        }
    }
    
    # Transmit using existing direwolf service
    # PTT is handled by direwolf config or VOX on the radio
    transmit_aprs(
        callsign="N0CALL",
        ssid="11",
        telemetry=test_telemetry,
        message="Test beacon",
        interface='kiss'
    )
