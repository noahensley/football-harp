import aprslib
import sounddevice as sd
import numpy as np
import subprocess

from debug import DEBUG_MODE

def create_aprs_packet(callsign, ssid, telemetry, message=""):
    """
    Creates an APRS packet using aprslib.

    Parameters:
        callsign (str): The callsign of the station (e.g., "N0CALL").
        ssid (str): The SSID (e.g., "11").
        latitude (str): Latitude in the format "4903.50N".
        longitude (str): Longitude in the format "07201.75W".
        telemetry (str): Telemetry or additional data to include.
        message (str, optional): Optional message.

    Returns:
        str: A formatted APRS packet string.
    """
    if DEBUG_MODE:
        print("Encoding APRS packet...")
        
    try:
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
        position = f"!{lat}/{lon}"
        comment = f"{telemetry_string} {message}".strip()

        # Construct the APRS packet
        packet = f"{source}>APRS,TCPIP*:{position} {comment}"
        return packet

    except Exception as e:
        raise Exception("Unable to create APRS packet: ", e)


def generate_afsk(packet, baudrate=1200, sample_rate=48000):
    """
    Generate AFSK audio for a given APRS packet.
    """
    if DEBUG_MODE:
        print("Generating AFSK audio from packet...")
        
    try:
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

    except Exception as e:
        raise Exception("Unable to generate AFSK audio: ", e)

    
def transmit_audio(signal, sample_rate=48000):
    """
    Transmits a waveform as audio.
    """
    if DEBUG_MODE:
        print("Transmitting audio...")
        
    try:
        sd.play(signal, samplerate=sample_rate)
        sd.wait()  # Wait for playback to finish
        print("APRS packet transmitted successfully.")

    except Exception as e:
        raise Exception("Error occurred during audio transmission: ", e)

