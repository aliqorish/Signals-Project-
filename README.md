In this project, I built a simplified version of Shazam. Instead of matching against millions of songs, it locates a short audio clip within a longer recording.
To achieve this, I use the Fast Fourier Transform (FFT) to analyze audio signals in the frequency domain.
frosti.wav is the sample audio, to change it simply replace it with another .wav file with the same name or change the name in line 11 of the code.
