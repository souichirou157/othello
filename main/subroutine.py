
def CheckBoard(size,x,y,MovablePos):
    
    if x < 1 or size < x       : return False
    if y < 1 or size < y       : return False
    if MovablePos[x,y] == 0    : return False
            
