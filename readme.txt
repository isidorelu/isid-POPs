## isid POPs! 1.0 GENERAL NOTES

#################################################

## POPs! is a music track builder in line with Digital Audio Workstations, such as Logic Pro X and Ableton Live, that is optimized for intuitive use. Designed for a simple module-based workflow unique to the world of DAWs, POPs! imparts a friendly user experience for those that have little to no experience in music making.

Features included in this 1.0 version of POPs! include:

- Sequencing with custom or built-in samples
- Pitch writing & sequencing with a basic single-voice, sine wave synthesizer
- Basic pattern layering with mix adjustment
- Unique two-bar sections that one can add, delete, toggle, reorder, & duplicate with aliasing as desired
- Section & pattern playback and full track bounce
- Adjustable BPM & Key

#################################################

## Getting Started:

1. Download & extract the program zip file.

2. Import any additional sound samples (16-bit, stereo) you would like to use into the "samples" folder in the main "isid POPs!" folder.
(Note: The folder contains built-in samples already designed by Isidore Lu that are ready for use.)

3. Run the code base from the main "isid POPs!" folder.

No additional libraries aside from CMU Graphics is needed to run this program.

#################################################

## Select Feature Instructions:

1.  BPM CHANGE - Click on BPM while no modules are selected. Type and enter as desired.
2.  KEY CHANGE - Press 'k' while no modules are selected. Type and enter as desired.
3.  SECTION DELETE - Triple-click on section
4.  SECTION REORDER - Drag section to desired location
5.  SECTION DUPLICATE - Select section and press 'd'
6.  MENU/SEQUENCER OPEN - Press 'enter' when module is selected
7.  NOTE LENGTHEN/SHORTEN - Select note & use arrow keys accordingly
8.  NOTE DELETE - Shorten note until it disappears
9.  MIX ADJUSTMENT - Select module & use up and down arrow keys accordingly
10. SYNTH OCTAVE CHANGE - The upper set of arrows in the SYNTH menu corresponds to octave change
11. SAMPLE SELECT - In a SAMPLE menu, type & enter desired sample from the "samples" folder while sample box is empty. (Note: The code will crash if the file does not exist.)
12. PLAY CURRENT PATTERN - In a menu, press spacebar.

Workflow Note: Play/load patterns individually at least once before playing sections, and play/load sections individually at least once before bouncing the full track to ensure no pieces from your track are missing. You can view these respective layer tracks in the main "isid POPs!" folder.

#################################################

## Citation Notes:

The sound algorithms in isid POPs! draw from and build upon Pat Virtue's implementation of pitch synthesis & sequencing and harmonic generation. Specifically the use of lists for horizontal sequencing, the use of loops & sine formulas for tone generation, and the technique of adding amplitudes of two tones of a given sample in time for harmonic generation (which is exploited generally in POPs! for the effect of "layering") are ideas used in this project. Furthermore, Mike Taylor's decay algorithm was used for the synth implementation.

All other code is original work. All image and sound assets are original work.

Libraries Used:
- CMU Graphics -  <https://academy.cs.cmu.edu/desktop>
- Pillow -  <https://pillow.readthedocs.io/en/stable/index.html>

Built-In Modules Used:
- OS, Pathlib, String, Random, Wave, Struct, Math

Implementation References:
- <https://docs.python.org/3/library/struct.html>
- <https://docs.python.org/3/library/wave.html>
- <http://soundfile.sapp.org/doc/WaveFormat/>
- <http://www.hydrogen18.com/blog/joys-of-writing-a-wav-file.html>
- <https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave>
- <https://github.com/mgeier/python-audio/blob/master/audio-files/audio-files-with-wave.ipynb>
- <https://cmtext.indiana.edu/acoustics/chapter1_pitch.php>
- <https://www.youtube.com/watch?v=udbA7u1zYfc&t>