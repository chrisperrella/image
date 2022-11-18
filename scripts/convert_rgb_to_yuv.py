import sys, cv2
from pathlib import Path

from image import colorspace

def main(image_path, output_path=None):
	try:
		image = cv2.imread( str( image_path ) )
	except cv2.error:
		print("Error: Image file is not valid.")
		return

	image = colorspace.rgb_to_ygocg( image )

	if output_path is None:
		output_path = Path( image_path.parent, 
						 f"{image_path.stem}_yuv.png" )
	cv2.imwrite( str( output_path ), image )

	
if __name__ == '__main__':
	source_path = Path( sys.argv[1] )
	main( source_path )