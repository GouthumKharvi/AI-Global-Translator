import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(duration=5, filename="input.wav"):
    print("Recording... Speak now!")
    fs = 16000  # Sample rate
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, recording)
    print("Recording saved as", filename)

record_audio()
