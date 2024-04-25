from pydub import AudioSegment
from pydub.playback import play
import soundfile as sf

data, samplerate = sf.read('unswer.ogg')  # Записываем запись с wav в переменную
sf.write('unswer.wav', data, samplerate)
song = AudioSegment.from_ogg("unswer.wav")
play(song)