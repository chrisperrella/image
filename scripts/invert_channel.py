import cv2, sys
from pathlib import Path

def main(image_path, output_path=None):
	image = cv2.imread(str(image_path))
	image[:, :, 1] = 255 - image[:, :, 1]
		
	if output_path is None:
		output_path = Path(image_path.parent, 
						f"{image_path.stem}_inverted.png")
	cv2.imwrite(str(output_path), image)

if __name__ == '__main__':
	image_path = Path(sys.argv[1])
	main(image_path)