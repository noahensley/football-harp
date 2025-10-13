import socket
import time


def decode_ax25_address(data, offset):
    """
    Decode a 7-byte AX.25 address field.
    Returns (callsign, next_offset, is_last)
    """
    if len(data) < offset + 7:
        return None, offset, True
    
    # Extract callsign (6 bytes, shifted right by 1)
    callsign_bytes = data[offset:offset+6]
    callsign = ''.join([chr(b >> 1) for b in callsign_bytes]).strip()
    
    # Extract SSID from 7th byte
    ssid_byte = data[offset+6]
    ssid = (ssid_byte >> 1) & 0x0F
    is_last = (ssid_byte & 0x01) != 0
    
    # Format callsign with SSID if not 0
    if ssid > 0:
        full_callsign = f"{callsign}-{ssid}"
    else:
        full_callsign = callsign
    
    return full_callsign, offset + 7, is_last

def parse_ax25_packet(ax25_data, target_callsign=None):
    """
    Parse AX.25 packet from KISS frame.
    Returns dictionary with packet info or None.
    """
    if not ax25_data or len(ax25_data) < 16:
        return None
    
    try:
        offset = 0
        
        # Decode destination address
        dest, offset, is_last = decode_ax25_address(ax25_data, offset)
        if not dest:
            return None
        
        # Decode source address
        source, offset, is_last = decode_ax25_address(ax25_data, offset)
        if not source:
            return None
        
        # Decode digipeater path
        path = []
        while not is_last and offset + 7 <= len(ax25_data):
            digi, offset, is_last = decode_ax25_address(ax25_data, offset)
            if digi:
                path.append(digi)
            else:
                break
        
        # Filter by destination if specified
        if target_callsign and dest != target_callsign:
            return None
        
        # Control and PID fields
        if offset + 2 > len(ax25_data):
            # Some packets might not have these, just extract what we have
            info = ax25_data[offset:].decode('ascii', errors='ignore').strip()
        else:
            control = ax25_data[offset]
            pid = ax25_data[offset + 1]
            info_start = offset + 2
            
            # Extract information field
            info = ax25_data[info_start:].decode('ascii', errors='ignore').strip()
        
        return {
            'destination': dest,
            'source': source,
            'path': path,
            'payload': info
        }
    
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def parse_command(payload):
    """
    Extract custom command from APRS payload.
    """
    if not payload:
        return None
    
    commands = ['CUTDOWN']
    
    payload_upper = payload.upper()
    for cmd in commands:
        if cmd in payload_upper:
            return cmd
    
    return None

def receive_direwolf_packets(lock, do_cutdown, host, port, callsign, filter_by_callsign=False):
    
    print("APRS Packet Decoder - KISS Protocol Mode")
    print("=" * 50)
    print(f"Connecting to Direwolf KISS port at {host}:{port}")
    if filter_by_callsign:
        print(f"Filtering for packets addressed to: {callsign}")
    else:
        print("Showing ALL packets (no filtering)")
    print("=" * 50)
    
    packets_seen = 0
    packets_filtered = 0
    
    while True:
        try:
            # Connect to Direwolf's KISS TCP interface
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            print(f"✓ Connected to Direwolf successfully!")
            print("Listening for KISS frames...\n")
            
            buffer = bytearray()
            FEND = 0xC0
            
            while True:
                # Receive data from Direwolf
                data = sock.recv(4096)
                if not data:
                    print("Connection closed by Direwolf")
                    break
                
                buffer.extend(data)
                
                # Look for complete KISS frames (FEND...FEND)
                while len(buffer) > 0:
                    # Find first FEND
                    try:
                        start = buffer.index(FEND)
                    except ValueError:
                        buffer.clear()
                        break
                    
                    # Remove any data before first FEND
                    if start > 0:
                        buffer = buffer[start:]
                    
                    # Need at least 2 bytes to look for end FEND
                    if len(buffer) < 2:
                        break
                    
                    # Look for end FEND
                    try:
                        end = buffer.index(FEND, 1)
                    except ValueError:
                        # Incomplete frame, wait for more data
                        break
                    
                    # Extract complete frame
                    frame = bytes(buffer[start:end+1])
                    buffer = buffer[end+1:]
                    
                    # KISS frame should be: FEND + command byte + AX.25 data + FEND
                    if len(frame) < 4:  # Too short
                        continue
                    
                    # Extract AX.25 data (skip FEND and command byte)
                    ax25_data = frame[2:-1]  # Skip first FEND+cmd, last FEND
                    
                    if len(ax25_data) < 14:  # Minimum AX.25 frame
                        continue
                    
                    # Parse AX.25 packet (without filter to count all)
                    packet_unfiltered = parse_ax25_packet(ax25_data, target_callsign=None)
                    if packet_unfiltered:
                        packets_seen += 1
                    
                    # Parse with filter if enabled
                    filter_callsign = callsign if filter_by_callsign else None
                    packet = parse_ax25_packet(ax25_data, target_callsign=filter_callsign)
                    
                    if packet:
                        packets_filtered += 1
                        print(f"\n{'='*50}")
                        print(f"[Packet #{packets_filtered}] Received at {time.strftime('%H:%M:%S')}")
                        print(f"  From: {packet['source']}")
                        print(f"  To: {packet['destination']}")
                        if packet['path']:
                            print(f"  Path: {' -> '.join(packet['path'])}")
                        print(f"  Payload: {packet['payload']}")
                        
                        # Check for command
                        command = parse_command(packet['payload'])
                        if command:
                            print(f"  >>> COMMAND DETECTED: {command} <<<")
                            with lock:
                                do_cutdown = True
                        
                        print(f"  (Total packets decoded: {packets_seen})")
                        print('='*50)
            
        except ConnectionRefusedError:
            print(f"✗ Could not connect to Direwolf at {host}:{port}")
            print("Make sure Direwolf is running with KISSPORT 8001 enabled.")
            print("Retrying in 5 seconds...")
            time.sleep(5)
        
        except KeyboardInterrupt:
            print(f"\n\n{'='*50}")
            print("Shutting down...")
            print(f"Total packets decoded: {packets_seen}")
            if filter_by_callsign:
                print(f"Packets for {callsign}: {packets_filtered}")
            else:
                print(f"Packets displayed: {packets_filtered}")
            print('='*50)
            try:
                sock.close()
            except:
                pass
            break
        
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            print("Reconnecting in 5 seconds...")
            try:
                sock.close()
            except:
                pass
            time.sleep(5)
