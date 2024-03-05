import os
from vosk import Model, KaldiRecognizer
import wave
from faster_whisper import WhisperModel

class SpeechRecog:

    def __init__(self):
        model_path = '../model/vosk-model-en-us-0.42-gigaspeech'
        # model_path = '../model/vosk-model-en-us-0.22-lgraph'
        self.model = Model(model_path)

    def transcribe(self, audio_path = 'NoLeadersPlease.wav'):
        # Use wave to read the audio file
        with wave.open(audio_path, "rb") as wf:
            rec = KaldiRecognizer(self.model, wf.getframerate())

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    pass

            result = rec.FinalResult()
            print(result)

    def transcribe_in_chunks(self, audio_path = 'NoLeadersPlease.wav'):
        wf = wave.open(audio_path, "rb")

        # Create a recognizer with the model and the correct sample rate
        rec = KaldiRecognizer(self.model, wf.getframerate())

        # Process the audio chunk by chunk
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                # Print partial results
                result = rec.Result()
                print(result)
            else:
                # Print partial results that are not yet finalized
                partial_result = rec.PartialResult()
                print(partial_result)

        # Final result for any remaining audio
        final_result = rec.FinalResult()
        print(final_result)

        # Close the audio file
        wf.close()


if __name__ == '__main__':
    sr = SpeechRecog()
    sr.transcribe_in_chunks(audio_path='audio.wav')

