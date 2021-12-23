# png-storage

Simple utility for storing files/directories in PNG files by abusing the fact that PNG images are read front to back, and ZIP files are read back to front.

This meas that you can concatinate them together, and the resulting file is both a zip file, and a png.
