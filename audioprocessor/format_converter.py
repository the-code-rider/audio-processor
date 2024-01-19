from pydub import AudioSegment

def convert_to_wav(input_audio_path, output_audio_path, sr = 16000):
    input_audio = AudioSegment.from_mp3(input_audio_path)
    audio_with_new_sr = input_audio.set_frame_rate(sr)
    audio_with_new_sr.export(output_audio_path, format='wav')



if __name__ == '__main__':
    i = 'Muse.mp3'
    o = 'Muse.wav'
    convert_to_wav(i, o)