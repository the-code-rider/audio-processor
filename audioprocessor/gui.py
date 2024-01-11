import streamlit as st

from audioprocessor.audio_io import AudioIo
from audioprocessor.visualizer import Visualizer

audio_loader = AudioIo()
viz = Visualizer()


def main():
    st.title('Audio Processor')
    uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "flac", "ogg", "aiff"])

    if uploaded_file is not None:
        st.audio(uploaded_file)
        y, sr = audio_loader.load_audio(uploaded_file)
        print(f'audio length :{len(y)}')
        print(f'sample rate :sr')
        wave = viz.waveform(y, sr)
        st.image(wave, caption="Waveform", use_column_width=True)

        # todo make the following optional
        # fig = viz.plotly_waveform(y, sr)
        # st.plotly_chart(fig, use_container_width=True)

        spec = viz.spectrogram(y, sr)
        st.image(spec, caption="Spectogram", use_column_width=True)



if __name__ == '__main__':
    main()