import pygame


# Given three colinear points p, q, r, the function checks if  
# point q lies on line segment 'pr'  
def on_Segment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r) 
    # function returns the following values: 
    # 0 : Colinear points 
    # 1 : Clockwise points 
    # 2 : Counterclockwise 

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
    # for details of below formula.  

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation 
        return 1
    elif (val < 0):

        # Counterclockwise orientation 
        return 2
    else:

        # Colinear orientation 
        return 0


# The main function that returns true if  
# the line segment 'p1q1' and 'p2q2' intersect. 
def do_intersect(p1, q1, p2, q2):
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case 
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases 

    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
    if ((o1 == 0) and on_Segment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
    if ((o2 == 0) and on_Segment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
    if ((o3 == 0) and on_Segment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
    if ((o4 == 0) and on_Segment(p2, q1, q2)):
        return True

    # If none of the cases 
    return False


def segment_intersect_rect(rect, seg):
    tl = pygame.Vector2(rect.topleft)
    tr = pygame.Vector2(rect.topright)
    bl = pygame.Vector2(rect.bottomleft)
    br = pygame.Vector2(rect.bottomright)

    p1 = pygame.Vector2(seg[0])
    p2 = pygame.Vector2(seg[1])

    return do_intersect(p1, p2, tl, tr) or do_intersect(p1, p2, tl, bl) or do_intersect(
        p1, p2, tr, br) or do_intersect(p1, p2, bl, br)


# Rotate from center
def rot_center(image, angle):
    center = image.get_rect().center
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)

    return rotated_image, new_rect


def is_on(a, b, c):
    # (or the degenerate case that all 3 points are coincident)
    return (collinear(a, b, c)
            and (within(a.x, c.x, b.x) if a.x != b.x else
                 within(a.y, c.y, b.y)))


# Collinear
def collinear(a, b, c):
    return (b.x - a.x) * (c.y - a.y) == (c.x - a.x) * (b.y - a.y)


# Is inside range
def within(p, q, r):
    return p <= q <= r or r <= q <= p


# Is on rect. In Python 3, there is already this method, so please use python 3 next year!!!
def on_rect(rect, pt):
    tl = pygame.Vector2(rect.topleft)
    tr = pygame.Vector2(rect.topright)
    bl = pygame.Vector2(rect.bottomleft)
    br = pygame.Vector2(rect.bottomright)
    pt = pygame.Vector2(pt)
    return is_on(tl, tr, pt) or is_on(tl, bl, pt) or is_on(tr, br, pt) or is_on(bl, br, pt)
