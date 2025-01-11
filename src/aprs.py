import aprslib
import sounddevice as sd
import numpy as np
import subprocess


def create_aprs_packet(callsign, ssid, telemetry, message=""):
    """
    Creates an APRS packet using aprslib.
    """
    # Extract position from telemetry
    lat = telemetry["VFAN"]["Latitude"]
    lon = telemetry["VFAN"]["Longitude"]
    
    telemetry_list = []
    for sensor in telemetry.keys():
        for data in telemetry[sensor].keys():
            telemetry_list.append(telemetry[sensor][data])
            
    telemetry_string = ", ".join(telemetry_list)
    
    # Combine callsign and SSID
    source = f"{callsign}-{ssid}"
    packet = aprslib.util.format_aprs_position(
        position=f"{lat}/{lon}",  # Replace with your position
        comment=telemetry_string + " " + message
    )
    return f"{source}>APRS::{packet}"


def generate_afsk(packet, baudrate=1200, sample_rate=48000):
    """
    Generate AFSK audio for a given APRS packet.
    """
    # Map binary `1` to 1200 Hz and `0` to 2200 Hz
    tones = {'1': 1200, '0': 2200}
    
    # NRZI encode the packet into a bitstream (implement NRZI logic here)
    bitstream = ''.join(format(ord(c), '08b') for c in packet)  # Example bitstream generation
    
    # Generate the audio signal
    signal = np.array([])
    for bit in bitstream:
        freq = tones[bit]
        t = np.arange(0, 1 / baudrate, 1 / sample_rate)
        sine_wave = np.sin(2 * np.pi * freq * t)
        signal = np.concatenate((signal, sine_wave))
    
    return signal

    
def transmit_audio(signal, sample_rate=48000):
    """
    Transmits a waveform as audio.
    """
    try:
        sd.play(signal, samplerate=sample_rate)
        sd.wait()  # Wait for playback to finish
        print("APRS packet transmitted successfully.")
    except Exception as e:
        print(f"Error occurred during audio transmission: {e}")

