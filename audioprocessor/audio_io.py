import librosa
import soundfile as sf
import numpy as np
class AudioIo:

    # todo: load from youtube
    def load_audio(self, audio_path, sr=None, mono=False):
        try:
            waveform, sample_rate = librosa.load(audio_path, sr=sr,mono=mono)
            return waveform, sample_rate
        except Exception as e:
            print(e)
            return None

    def save(self, audio_np_array, sr, output_filename):
        sf.write(output_filename, np.ravel(audio_np_array), sr)
        return output_filename


