import librosa
import noisereduce as nr
import soundfile as sf
import scipy
import torch
from noisereduce.torchgate import TorchGate as TG


class NoiseReducer:

    def __init__(self):
        self.gpu_available = torch.cuda.is_available()

    def reduce(self, y, sr, non_stationary=True, use_torchgate=False):
        if use_torchgate:
            device = torch.device('cpu') if self.gpu_available else torch.device('cpu')
            tg = TG(sr=sample_rate, nonstationary=True).to(device)

            audio_tensor = self._convert_waveform_to_tensor(y)
            reduced_noise_tensor = tg(audio_tensor)

            if self.gpu_available:
                reduced_noise_tensor_cpu = reduced_noise_tensor.cpu()
                reduced_noise_tensor_numpy = reduced_noise_tensor_cpu.numpy()
            else:
                reduced_noise_tensor_numpy = reduced_noise_tensor.numpy()

            return reduced_noise_tensor_numpy


        else:
            reduced_noise_audio = nr.reduce_noise(y=y, sr=sr)
            return reduced_noise_audio


    def _convert_waveform_to_tensor(self, y):
        audio_tensor = torch.tensor(y)
        if self.gpu_available:
            audio_tensor = audio_tensor.to('cuda')
        return audio_tensor



# Load the audio file
file_path = 'NoLeadersPleasebyCharlesBukowski.mp3'  # Replace with your file path
audio_data, sample_rate = librosa.load(file_path, sr=None)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
tg = TG(sr=sample_rate, nonstationary=False).to(device)

reduced_torch = tg((audio_data, sample_rate))
sf.write('reduced_noise_torch.wav', reduced_torch, sample_rate)

exit(0)



# Perform noise reduction
reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=sample_rate)

# Save the processed audio
output_file_path = 'processed_audio_file.wav'  # Replace with your desired output file path
# librosa.output.write_wav(output_file_path, reduced_noise_audio)
sf.write('reduced_noise.wav', reduced_noise_audio, sample_rate)

# Define the band-pass filter
def bandpass_filter(signal, sr, lowcut, highcut):
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = scipy.signal.butter(4, [low, high], btype='band')
    return scipy.signal.lfilter(b, a, signal)