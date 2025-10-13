import re
import socket
import time

def parse_aprs_packet(line, target_callsign=None):
    """
    Parse a single line of Direwolf decoded output.
    Returns a dictionary with packet information or None if not parseable.
    
    Args:
        line: Raw line from Direwolf output
        target_callsign: Optional callsign to filter for (e.g., "PAYLOAD-11")
    """
    # Look for lines that contain actual packet data
    # Direwolf format: [channel] source>destination,path:payload
    match = re.search(r'\[(\d+)\]\s+([A-Z0-9-]+)>([A-Z0-9-,]+):(.+)', line)
    
    if match:
        channel = match.group(1)
        source = match.group(2)
        destination_path = match.group(3)
        payload = match.group(4)
        
        # Split destination from digipeater path
        dest_parts = destination_path.split(',')
        destination = dest_parts[0]
        path = dest_parts[1:] if len(dest_parts) > 1 else []
        
        # Filter by destination callsign if specified
        if target_callsign and destination != target_callsign:
            return None
        
        return {
            'channel': channel,
            'source': source,
            'destination': destination,
            'path': path,
            'payload': payload,
            'raw': line
        }
    
    return None

def parse_command(payload):
    """
    Extract custom command from APRS payload.
    This is where you'd implement your command protocol.
    """
    # Example: Look for specific command keywords
    commands = ['CUTDOWN', 'VALVE_OPEN', 'VALVE_CLOSE', 'STATUS', 'RESET']
    
    payload_upper = payload.upper()
    for cmd in commands:
        if cmd in payload_upper:
            return cmd
    
    return None

def main():
    # Configuration
    DIREWOLF_HOST = 'localhost'
    DIREWOLF_PORT = 8000  # AGW Port
    TARGET_CALLSIGN = 'PAYLOAD-11'  # Change this to your actual payload callsign
    
    print("APRS Packet Decoder - Real-time Socket Mode")
    print("=" * 50)
    print(f"Connecting to Direwolf at {DIREWOLF_HOST}:{DIREWOLF_PORT}")
    print(f"Filtering for packets addressed to: {TARGET_CALLSIGN}")
    print("=" * 50)
    
    packets_seen = 0
    packets_filtered = 0
    
    while True:
        try:
            # Connect to Direwolf's KISS TCP interface
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((DIREWOLF_HOST, DIREWOLF_PORT))
            print(f"Connected to Direwolf successfully!")
            print("Listening for packets...\n")
            
            buffer = ""
            
            while True:
                # Receive data from Direwolf
                data = sock.recv(4096)
                if not data:
                    print("Connection closed by Direwolf")
                    break
                
                # Decode and add to buffer
                buffer += data.decode('utf-8', errors='ignore')
                
                # Process complete lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    
                    # Count all packets
                    packet_unfiltered = parse_aprs_packet(line, target_callsign=None)
                    if packet_unfiltered:
                        packets_seen += 1
                    
                    # Parse with filter
                    packet = parse_aprs_packet(line, target_callsign=TARGET_CALLSIGN)
                    if packet:
                        packets_filtered += 1
                        print(f"\n[Packet #{packets_filtered}] Received at {time.strftime('%H:%M:%S')}")
                        print(f"  Channel: {packet['channel']}")
                        print(f"  From: {packet['source']}")
                        print(f"  To: {packet['destination']}")
                        if packet['path']:
                            print(f"  Path: {' -> '.join(packet['path'])}")
                        print(f"  Payload: {packet['payload']}")
                        
                        # Check if this is a command packet
                        command = parse_command(packet['payload'])
                        if command:
                            print(f"  >>> COMMAND DETECTED: {command}")
                        
                        print(f"  (Total packets seen: {packets_seen})")
            
        except ConnectionRefusedError:
            print(f"Error: Could not connect to Direwolf at {DIREWOLF_HOST}:{DIREWOLF_PORT}")
            print("Make sure Direwolf is running with KISSPORT 8001 enabled in the config.")
            print("Retrying in 5 seconds...")
            time.sleep(5)
        
        except KeyboardInterrupt:
            print(f"\n\n{'=' * 50}")
            print("Shutting down...")
            print(f"Total packets decoded: {packets_seen}")
            print(f"Packets for {TARGET_CALLSIGN}: {packets_filtered}")
            print("=" * 50)
            try:
                sock.close()
            except:
                pass
            break
        
        except Exception as e:
            print(f"Error: {e}")
            print("Reconnecting in 5 seconds...")
            try:
                sock.close()
            except:
                pass
            time.sleep(5)

if __name__ == '__main__':
    main()
