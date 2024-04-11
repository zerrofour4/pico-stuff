def msb(n):
    ndx = 0
    while ( 1 < n ):
      n = ( n >> 1 )
      ndx += 1
 
    return ndx
