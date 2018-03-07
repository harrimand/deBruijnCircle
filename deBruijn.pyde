""" 
Animate rotating ring of red and green LEDs in de Bruijn sequence.  
Source Code developed using the Processing3 IDE in python mode.
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
"""
from __future__ import print_function
import math

def settings():
    size(800, 800)

def setup():
    global circle        #type Shape: LEDs in a circular pattern
    global capture       #type Shape: Window to select bits for conversion
    global R, G, B       #type Color: Red, Green and Blue
    global dbString      #type String: containing de Bruijn Sequence 
    global npoints       #type Int:   Number of LEDs in circular pattern  
    global capIndex      #type Int:  Index of nbits contiguous LEDS
    global nbits         #type Int:  Number of bits in binary value
    background(0)
    R = color(255, 0, 0)
    G = color(0, 192, 0)
    B = color(0, 0, 255)

    ellipseMode(CENTER)

    fill(G)
    ellipse(400, 400, 50, 50)
    fill(B)
    stroke(R)
    strokeWeight(3)
    textAlign(CENTER, CENTER)
    textSize(48)    #Used for size of decimal display

    radius = 300
    nbits = 5    #Number of bits 
                 #Number of LEDs = 2^nbits
    
    nbits = nbits if nbits <= 7 else 7
    
    dbString = deBruijnStr(nbits)
    print(dbString)
    # Calculate number of LEDs in circle 
    npoints = 2**nbits
    
    # Create circle of LEDs
    circle = createCircle(radius, npoints)
    
    # Align LEDs in capture window.
    circle.rotate((nbits + 1) % 2 * math.pi / npoints)
    
    # Create window frame around bits to be converted to decimal
    capture = captureBits(radius, nbits)
    
    # Select offset to LED at beginning of capture window
    capIndex = [0, 1, 3, 5, 11, 22, 46, 93][nbits]

def deBruijnStr(nb):
    '''Generate binary 2^nb length string matching de Bruijn sequence'''  
    dbStr = "0" * nb
    for i in range(2**nb - nb):
        dbStr += "1" if dbStr[-nb + 1:] + "1" not in dbStr else "0"
    return dbStr

def createCircle(radius, numPoints):
    '''Create a shape of 2^nbits LEDS in circular pattern.''' 
    circle = createShape(GROUP)
    circle.addChild(makeStar(160))
    # fill(R)
    # circle.addChild(createShape(LINE, 0, 0, radius, 0))
    fill(B)
    circle.addChild(createShape(ELLIPSE, 0, 0, 40, 40))    
    LEDsize = 20
    deltaA = 2 * math.pi / numPoints

    for i in range(0, numPoints):
        angle = i * deltaA
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        LED = R if int(dbString[i]) else G
        fill(LED)
        stroke(LED)
        Pt = createShape(ELLIPSE, x, -y, LEDsize, LEDsize)
        circle.addChild(Pt)
    return circle    

def makeStar(r):
    """  Vertex scalers are calculated for a 5 point star using points at radius r 
    evenly distributed in 72 degree increments.  Inner points are 36 degrees from 
    outer points.  x scalers (h1 - h5) and y scalers (v1 - v5) were pre-calculated 
    using the cos(), sin() functions and intersect points for lines connecting 
    outer points. 
    """
    h1 = 0
    h2 = .224514
    h3 = .363271
    h4 = .587785
    h5 = .951057
    v1 = -1
    v2 = -.309017
    v3 = .118034
    v4 = .381966
    v5 = .809017
    st = createShape()
    st.beginShape()
    st.fill(255,255,255)
    st.noStroke()
    st.vertex(h1*r, v1*r)
    st.vertex(h2*r, v2*r)
    st.vertex(h5*r, v2*r)
    st.vertex(h3*r, v3*r)
    st.vertex(h4*r, v5*r)
    st.vertex(h1*r, v4*r)
    st.vertex(-h4*r, v5*r)
    st.vertex(-h3*r, v3*r)
    st.vertex(-h5*r, v2*r)
    st.vertex(-h2*r, v2*r)
    st.endShape(CLOSE)
    return st

def captureBits(r, nb):
    ''' Draw border around LEDs used to make decimal number 
    when rotation stops.
    '''
    noFill()
    cap = createShape(GROUP)
    angW = math.pi / 2**nb * nb
    angSt = math.pi / 2 - angW 
    angEnd = math.pi / 2 + angW
    angStX1 = (r - 15) * math.cos(angSt)
    angStY1 = ( r - 15) * math.sin(angSt)
    angStX2 = (r + 15) * math.cos(angSt)
    angStY2 = (r + 15) * math.sin(angSt)
    angEndX1 = (r - 15) * math.cos(angEnd)
    angEndY1 = (r - 15) * math.sin(angEnd)
    angEndX2 = (r + 15) * math.cos(angEnd)
    angEndY2 = (r + 15) * math.sin(angEnd)    
    stroke(255)
    cap.addChild(createShape(LINE, angStX1, angStY1, angStX2, angStY2))
    cap.addChild(createShape(LINE, angEndX1, angEndY1, angEndX2, angEndY2))
    cap.addChild(createShape(ARC, 0, 0, 2 * r - 30, 2 * r - 30, angSt, angEnd))
    cap.addChild(createShape(ARC, 0, 0, 2 * r + 30, 2 * r + 30, angSt, angEnd))
    return cap


def capDec(capIndex, nbits):
    '''Get nbits contiguous bit values with wrapping from 
    end of the dbString to the beginning of string''' 
    seqEnd = (capIndex + nbits - 1) % len(dbString)
    if capIndex < (len(dbString) - nbits + 1):
        seqStr = dbString[capIndex:capIndex + nbits]
    else:
        seqStr = dbString[capIndex:] + dbString[:seqEnd + 1]
    return seqStr
                                
def draw():
    global capIndex
    pushMatrix()        
    translate(width/2, height/2)
    circle.rotate(2 * math.pi / npoints)
    background(0)
    shape(circle)
    shape(capture)
    popMatrix()
    capIndex = (capIndex + 1) % len(dbString)
#    print("Sequence: ", capDec(capIndex, nbits))
    delay(100)
#   noLoop()

def keyPressed():
    if key == " ":    # If space pressed pause rotation
        binSeq = capDec(capIndex, nbits)
        decSeq = int(binSeq, 2)
        print("Sequence: ", binSeq, " ", decSeq)
        fill(255, 255, 0)
        text(str(decSeq), width/2, height*3/4)
        noLoop()
    else: loop()      # Continue rotation 
