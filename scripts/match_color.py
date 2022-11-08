import cv2, sys
import numpy as np
from pathlib import Path

def match_color(source, target):
	source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
	target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")
	
	(src_lightness, src_red_green, src_blue_yellow) = cv2.split(source)
	(tar_lightness, tar_red_green, tar_blue_yellow) = cv2.split(target)
	
	(src_lightness_mean, src_lightness_std) = (src_lightness.mean(), src_lightness.std())
	(tar_lightness_mean, tar_lightness_std) = (tar_lightness.mean(), tar_lightness.std())
	
	(src_red_green_mean, src_red_green_std) = (src_red_green.mean(), src_red_green.std())
	(tar_red_green_mean, tar_red_green_std) = (tar_red_green.mean(), tar_red_green.std())
	
	(src_blue_yellow_mean, src_blue_yellow_std) = (src_blue_yellow.mean(), src_blue_yellow.std())
	(tar_blue_yellow_mean, tar_blue_yellow_std) = (tar_blue_yellow.mean(), tar_blue_yellow.std())

	(lightness, red_green, blue_yellow) = cv2.split(target)
	lightness   -= tar_lightness_mean
	red_green   -= tar_red_green_mean
	blue_yellow -= tar_blue_yellow_mean

	lightness   = (src_lightness_std   / tar_lightness_std) * lightness
	red_green   = (src_red_green_std   / tar_red_green_std) * red_green
	blue_yellow = (src_blue_yellow_std / tar_blue_yellow_std) * blue_yellow	

	lightness   += src_lightness_mean
	red_green   += src_red_green_mean
	blue_yellow += src_blue_yellow_mean

	lightness   = np.clip(lightness, 0, 255)
	red_green   = np.clip(red_green, 0, 255)
	blue_yellow = np.clip(blue_yellow, 0, 255)
	
	transfer = cv2.merge([lightness, red_green, blue_yellow])
	transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

	return transfer

def main(source_path, target_path):
	source = cv2.imread(str(source_path))
	target = cv2.imread(str(target_path))
	result = match_color(source, target)

	output_path = Path(target_path.parent, f"{target_path.stem}_recolored.png")
	print(output_path)
	cv2.imwrite(str(output_path), result)

if __name__ == '__main__':
	source_path = Path(sys.argv[1])
	target_path = Path(sys.argv[2])
	main(source_path, target_path)
