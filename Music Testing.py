import numpy as np
from pydub import AudioSegment
from pydub.playback import play

# Define the sample rate and duration
sample_rate = 44100  # 44.1 kHz
note_duration = 0.3  # Duration of each note in seconds

# Define the frequencies for a happy melody (C Major scale)
notes = {
    'C4': 261.63,  # Middle C
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25,  # High C
}

# Define a simple happy melody using the notes above
melody = ['C4', 'E4', 'G4', 'C5', 'E4', 'G4', 'C5', 'E5']

# Function to generate a sine wave for a given frequency and duration
def generate_tone(frequency, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)  # Sine wave
    tone = tone * (2**15 - 1) / np.max(np.abs(tone))  # Normalize to 16-bit range
    return tone.astype(np.int16)

# Generate the melody
audio_segments = []
for note in melody:
    tone = generate_tone(notes[note], note_duration)
    audio_segment = AudioSegment(
        tone.tobytes(),
        frame_rate=sample_rate,
        sample_width=tone.dtype.itemsize,
        channels=1
    )
    audio_segments.append(audio_segment)

# Add a short silence between notes for clarity
silence_duration = 50  # 50 milliseconds
silence = AudioSegment.silent(duration=silence_duration)
audio_segments_with_silence = []
for segment in audio_segments:
    audio_segments_with_silence.append(segment)
    audio_segments_with_silence.append(silence)

# Combine all segments into one audio track
final_audio = sum(audio_segments_with_silence)

# Play the melody
play(final_audio)

# Optionally, export the melody as a WAV file
final_audio.export("happy_melody.wav", format="wav")
print("Happy melody saved as 'happy_melody.wav'")