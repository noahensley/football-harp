import aprslib
import sounddevice as sd
import numpy as np
import subprocess

def create_aprs_packet(callsign, ssid, telemetry, message=""):
    """Creates an APRS packet from an input string
    using a designated callsign, SSID, and optional
    message."""
    # Construct the APRS packet string
    packet = f"{callsign}-{ssid}>APRS::{telemetry}"
    if message:
        # Appends message to packet if supplied
        packet += f':{message}'
    # Returns APRS packet
    return packet
    
def transmit_audio(packet, sample_rate):
    """Transmits an APRS packet to the sound card
    on the Rapsberry Pi 0W."""
    # Convert APRS packet to audio signal (you may need to adjust the encoding and other parameters)
    audio_signal = np.array([ord(c) for c in packet])  # Convert each character to its ASCII value
    # Adjust the sample rate if needed
    sd.play(audio_signal, samplerate=sample_rate)
    sd.wait()
    print("APRS packet transmitted successfully.")

def update_direwolf_beacon_config(lat, lon):
    """Re-configured Direwolf configuration file as
    the position of the Raspberry Pi 0W changes."""
    # Define the new BEACON line with the provided latitude and longitude
    new_config = f'BEACON every 10 minutes symbol="b" lat={lat} long={lon} comment="Direwolf APRS"'
    # Read the current contents of the direwolf.conf file
    with open('/etc/direwolf.conf', 'r') as f:
        conf_contents = f.readlines()
    # Find and update the BEACON line in the configuration file
    for i, line in enumerate(conf_contents):
        if line.startswith('BEACON'):
            conf_contents[i] = f'{new_config}\n'
    # Write the modified contents back to the file using sudo
    with open('/etc/direwolf.conf', 'w') as f:
        subprocess.run(['sudo', 'tee', '/etc/direwolf.conf'], input=''.join(conf_contents), text=True, check=True)

def restart_direwolf():
    """Restarts the Direwolf APRS via the command line."""
    # Restart Direwolf by running the command
    subprocess.run(['sudo', 'systemctl', 'restart', 'direwolf'])
