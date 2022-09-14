import os
import sys
from pedalboard import Pedalboard, Reverb, HighpassFilter, \
  LowpassFilter, PitchShift, Gain, Resample

from pedalboard.io import AudioFile


def check_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

file_name = input("Audio file to edit (enter the full file name): ")

# Make sure file exists
if not os.path.isfile(file_name):
  sys.exit("Invalid file name. Note, the file must be in the same directory. Enter in the form: example.wav")

# Get file type
file_type = file_name[len(file_name)-3:]

# Try opening file
try:
  with AudioFile(file_name) as f:
    audio = f.read(f.frames)
    samplerate = f.samplerate
except Exception as e:
  sys.exit(e)

# Let user add their own effects
board = Pedalboard([])

while (1==1): # Infinite loop; user can add as many effects as they like, and export/exit when they wish.
  option = input("""
Select an option by entering a number between 1-9:
1) Add a High Pass Filter (remove low frequencies)
2) Add a Low Pass Filter (remove high frequencies)
3) Change the Pitch
4) Increase/Decrease Volume
5) Resample (lower the audio quality) 
6) Add Reverb
7) Export File
8) Exit
""")
  if option == "1":
    cutoff = '.'
    while not check_float(cutoff):
      cutoff = input("Cutoff Frequency: ")
    board.append(HighpassFilter(float(cutoff)))
    print("High Pass Filter added.")

  if option == "2":
    cutoff = '.'
    while not check_float(cutoff):
      cutoff = input("Cutoff Frequency: ")
    board.append(LowpassFilter(float(cutoff)))
    print("Low Pass Filter added.")

  if option == "3":
    semitones = '.'
    while not check_float(semitones):
      semitones = input("Semitones (can be negative): ")
    board.append(PitchShift(float(semitones)))
    print("Pitch shifted.")

  if option == "4":
    gain_amount = "."
    while not check_float(gain_amount):
      gain_amount = input("Gain amount/loss (in db): ")
    board.append(Gain(float(gain_amount)))
    print("Volume changed.")

  if option == "5":
    new_sample_rate = '.'
    while not check_float(new_sample_rate):
      new_sample_rate = input("New Sample Rate: ")
    board.append(Resample(float(new_sample_rate)))
    print("Resampled.")

  if option == "6":
    room_size = "."
    while not check_float(room_size):
      room_size = input("Room size (%): ")

    wet_level = "."
    while not check_float(wet_level):
      wet_level = input("Wet level (%): ")
    
    room_size, wet_level = float(room_size) / 100, float(wet_level) / 100
    board.append(Reverb(room_size=room_size, wet_level=wet_level))
    print("Reverb added.")

  if option == "7":
    effected = board(audio, samplerate)
    new_file_name = "modified_" + file_name
    with AudioFile(new_file_name, 'w', samplerate, effected.shape[0]) as f:
      f.write(effected)
    sys.exit("Exported audio to " + new_file_name + ".")

  if option == "8":
    sys.exit("Program exited.")