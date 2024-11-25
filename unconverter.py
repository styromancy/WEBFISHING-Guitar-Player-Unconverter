from tkinter.filedialog import askopenfilenames
from tkinter import Tk
from time import sleep
import os

Tk().withdraw()

try:
    from midiutil import MIDIFile
except ImportError as e:
    print(f"Exception occurred: {e}")
    print("Try running this command: \tpython -m pip install midiutil")

"""
Prompts the user for a file or list of files. 
"Reverts" the files back to Midi format and exports them to a shared output directory.
"""


def unconvert(input_file_name, output_file_name):
    """
    Takes input_file_name and converts it out of that weird plaintext format.
    Outputs to output_file_name.

    The expected file type is an extensionless file with the following information in cleartext on each newline:
    [int Timestamp] [int note_1] [int note_2] ... [int note_n]
    """

    midi_file = MIDIFile(1)
    midi_file.addTempo(
        0, 0, 1 * 60 * 1000
    )  # 60,000 BPM because these are timestamped by the millisecond
    with open(input_file_name) as f:
        data = [x.strip() for x in f.readlines()]

    for row in data:
        info = row.split()
        timestamp = int(info[0])  # timestamp is the first int in the row
        notes = [int(x) for x in info[1:]]  # the rest are notes
        duration = 1000  # 1 second
        for note in notes:
            midi_file.addNote(0, 0, note, timestamp, duration, 100)

    with open(output_file_name, "wb") as output:
        midi_file.writeFile(output)
    
    print(f"Exported {output_file_name}")


def _main():
    """
    Prompt for input files and start unconverting.
    Prints output directory to console.
    """

    file_names = askopenfilenames(
        defaultextension="",
        title="Select file(s) to unconvert...",
        initialdir=os.path.dirname(os.path.abspath(__file__)),
    ) # Prompt user for files with directory of this script as the default
    
    if len(file_names) < 1:
        print("No files provided")
        return
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(file_names[0])), 'unconverted') # outputs to /dir/to/first/file/unconverted
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) # create output directory if it isn't real
        
    print(f"Output directory: {output_dir}")    
            
    for abs_file_name in file_names:
        output_name = os.path.basename(abs_file_name) + '.mid'  # base file name + ".mid"
        output_name = os.path.join(output_dir, output_name) 
        unconvert(abs_file_name, output_name)


if __name__ == "__main__":
    _main()
    input("Press enter to exit")
