import cv2
import numpy as np

def rgb_to_yuv( image ):    
    b, g, r = cv2.split( image.astype( float ) )

    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    u = 0.5389 * ( b - y ) + 128
    v = 0.6350 * ( r - y ) + 128

    y = np.round( y ).astype( np.uint8 )
    u = np.round( np.clip( u, 0, 255 ) ).astype( np.uint8 )
    v = np.round( np.clip( v, 0, 255 ) ).astype( np.uint8 )
    
    return cv2.merge( ( y, u, v ) )


def rgb_to_ycocg( image ):
    b, g, r = cv2.split( image.astype( float ) )

    y = 0.25 * r + 0.5 * g + 0.25 * b
    co = 0.5 * r - 0.5 * b + 0.5
    cg = -0.25 * r + 0.5 * g - 0.25 * b + 0.5

    co = co + 127
    cg = cg + 127

    co = 255 - co

    y = np.round( y ).astype( np.uint8 )
    co = np.round( np.clip( co, 0, 255 ) ).astype( np.uint8 )
    cg = np.round( np.clip( cg, 0, 255 ) ).astype( np.uint8 )
    
    return cv2.merge( ( y, co, cg ) )


def rgb_to_ygocg( image ):
    b, g, r = cv2.split( image.astype( float ) )

    y = 0.25 * r + 0.5 * g + 0.25 * b
    go = 0.5 * g - 0.5 * b + 0.5
    cg = -0.25 * r + 0.5 * g - 0.25 * b + 0.5

    go = go + 127
    cg = cg + 127

    go = 255 - go

    y = np.round( y ).astype( np.uint8 )
    go = np.round( np.clip( go, 0, 255 ) ).astype( np.uint8 )
    cg = np.round( np.clip( cg, 0, 255 ) ).astype( np.uint8 )
    
    return cv2.merge( ( y, go, cg ) )