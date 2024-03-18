import aprslib
import sounddevice as sd
import numpy as np
import subprocess

def create_aprs_packet(callsign, ssid, telemetry, message=""):
    """
    Creates an APRS packet from an input string using a designated callsign, SSID, and optional message.
    
    Parameters:
        callsign (str): The callsign of the control operator.
        ssid (str): The SSID classifying the APRS transmissions (i.e. 11 = balloon).
        telemetry (str): The string containing the collected data.
        message (str, optional): An optional message to be appended to the APRS packet.

    Returns:
        A formatted APRS packet string containing data and other APRS information.
    """
    # Construct the APRS packet string
    packet = f"{callsign}-{ssid}>APRS::{telemetry}"

    if message:
        # Appends message to packet if supplied
        packet += ":" + message

    # Returns APRS packet
    return packet
    
def transmit_audio(packet, sample_rate):
    """
    Transmits an APRS packet to the sound card on the Rapsberry Pi 0W.

    Parameters:
        packet (str): The formatted APRS packet to be transmitted.
        sample_rate (int): The sampling rate for transmission.
    """
    try:
        # Convert APRS packet to audio signal (you may need to adjust the encoding and other parameters)
        audio_signal = np.array([ord(c) for c in packet])  # Convert each character to its ASCII value

        # Adjust the sample rate if needed
        sd.play(audio_signal, samplerate=sample_rate)

        # Waits for all played audio to finish playing
        sd.wait()
        
        print("APRS packet transmitted successfully.")
    except Exception as e:
        print("Error occured during audio transmission: {e}")
