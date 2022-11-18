import sys, cv2
import numpy as np
from pathlib import Path

def get_type_range(image):
	data_type = image.dtype
	cell_range = None

	if data_type == np.uint8:
		cell_range = 255
	elif data_type == np.uint16:
		cell_range = 65535

	return cell_range


def get_percent_between_min_max(image, 
								min_percent, 
								max_percent, 
								closed_left=False, 
								closed_right=False):
	l = np.greater if not closed_left else np.greater_equal
	r = np.less if not closed_right else np.less_equal
	c = l( image, min_percent ) & r( image, max_percent )
	return np.count_nonzero( c ) / image.size


def main(image_path, output_path=None, auto_threshold=True, clamp_threshold=0.1): 
	try:
		image = cv2.imread(str(image_path))
	except cv2.error:
		print("Error: Image file is not valid.")
		return
	
	max_range = get_type_range(image)
	source_mid_point = max_range / 2	
	
	image_mid_point = (int(np.max(image)) + 
					   int(np.min(image))) / 2		
	deviation = image_mid_point - source_mid_point
	if deviation >= 0:
		image = image - deviation
	else:
		image = image + abs(deviation)

	max = int(np.max(image))
	min = int(np.min(image))
	if auto_threshold:
		original_max = int(np.max(image))
		percentage_of_image_max = get_percent_between_min_max( image, 
															   128, 
															   original_max )
		max = original_max
		while percentage_of_image_max < clamp_threshold:
			image += 1
			percentage_of_image_max = get_percent_between_min_max( image, 
																   128, 
																   original_max )
			max -= 1

		original_min = int(np.min(image))
		percentage_of_image_min = get_percent_between_min_max( image, 
															   original_min, 
															   128 )
		min = original_min
		while percentage_of_image_min < clamp_threshold:
			image -= 1
			percentage_of_image_min = get_percent_between_min_max( image, 
																   original_min, 
																   128 )
			min += 1

	range = max_range / (max - min + 2)

	image = np.round(range * 
					 np.where(image >= min, 
							  image - min + 1, 
							  0)).clip(max = max_range)
	
	if output_path is None:
		output_path = Path(image_path.parent, 
						f"{image_path.stem}_autolevel.png")
	cv2.imwrite(str(output_path), image)

	
if __name__ == '__main__':
	source_path = Path(sys.argv[1])
	main(source_path)