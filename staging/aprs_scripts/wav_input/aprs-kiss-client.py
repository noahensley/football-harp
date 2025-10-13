import socket

def parse_kiss(data):
    """
    Basic KISS frame parser.
    KISS frames: 0xC0 [cmd] [data...] 0xC0
    cmd = 0x00 for data frame
    """
    if len(data) < 2:
        return None
    
    # Check for KISS frame delimiters
    if data[0] == 0xC0:
        # Find end delimiter
        try:
            end = data.index(0xC0, 1)
            frame = data[1:end]
            
            if len(frame) > 0:
                cmd = frame[0]
                if cmd == 0x00:  # Data frame
                    # Return raw packet data (skip command byte)
                    return frame[1:].decode('latin-1', errors='ignore')
        except ValueError:
            pass
    
    return None

def main():
    # Connect to Direwolf's KISS port (default 8001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10.0)  # 10 second timeout
    
    print("Connecting to Direwolf on localhost:8001...")
    
    try:
        sock.connect(('localhost', 8001))
    except ConnectionRefusedError:
        print("Error: Could not connect to Direwolf.")
        print("Make sure Direwolf is running first!")
        sock.close()
        return
    
    print("Connected! Waiting for APRS packets...\n")
    
    try:
        
        while True:
            try:
                data = sock.recv(1024)
                if data:
                    aprs_packet = parse_kiss(data)
                    if aprs_packet:
                        # Extract payload (part after the comma)
                        if ',' in aprs_packet:
                            payload = aprs_packet.split(',', 1)[1]
                            print(f"Payload: {payload}")
                        else:
                            print(f"Packet: {aprs_packet}")
                else:
                    print("\nConnection closed by Direwolf (WAV file finished)")
                    break
                    
            except socket.timeout:
                print("\nTimeout - no more data received")
                break
                
    except ConnectionRefusedError:
        print("Error: Could not connect to Direwolf.")
        print("Make sure Direwolf is running first!")
    except ConnectionResetError:
        print("\nConnection closed by Direwolf (WAV file finished)")
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        sock.close()
        print("Disconnected")

if __name__ == "__main__":
    main()