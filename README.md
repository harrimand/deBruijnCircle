# deBruijnCircle
Animate rotating ring of red and green LEDs in de Bruijn sequence.   Source Code developed using the Processing3 IDE in python mode.
Red LEDs represent a binary 1
Green LEDs represent a binary 0
Red and Green LEDs are ordered to match the circular de Bruijn sequence.
Example 3 bit de Bruijn sequence: "00011101"
All 3 bit numbers can be found by selecting 3 contiguous bits. When you 
    wrap the leading 0s to the end of the string you can get "010" and "100"

nbits specifies the number of bits in each binary number in the string.
nbits value 3..6 produce the best appearance in the given window size  

Usage: Press space to pause rotation and convert captured binary value.
Press any other key to resume rotation.
