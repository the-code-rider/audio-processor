import librosa.display
import librosa.feature
import tkinter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import plotly.express as px

class Visualizer:

    def __init__(self):
        self.DOWNSAMPLE_RATE = 16000

    # doesn't work with streamlit; unless the waveform is saved and displayed as a picture
    # todo figure out a fix
    def waveform(self, waveform, sample_rate):
        # plt.figure(figsize=(14,5))
        librosa.display.waveshow(waveform, sr=sample_rate)
        plt.title('Waveform')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf
        # plt.show()

    def plotly_waveform(self, y, sr, downsample = True):
        audio = None
        # handle stero
        audio = y[1] if len(y) == 2 else y
        # Generate time axis

        audio_downsampled = librosa.resample(audio, orig_sr=sr, target_sr=self.DOWNSAMPLE_RATE)

        time = np.linspace(0, len(audio_downsampled) / sr, num=len(audio_downsampled))

        print(len(audio_downsampled))
        print(len(time))

        # Create a plotly figure
        fig = px.line(x=time, y=audio_downsampled, labels={'x': 'Time', 'y': 'Amplitude'}, title='Audio Waveform')
        return fig


    def spectrogram(self, waveform, sample_rate):
        S = librosa.feature.melspectrogram(y=waveform[1], sr=sample_rate)
        S_DB = librosa.power_to_db(S, ref=np.max)
        librosa.display.specshow(S_DB, sr=sample_rate, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel Spectrogram')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf
        # plt.show()


