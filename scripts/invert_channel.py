import cv2, numpy, sys
from pathlib import Path

def main(image_path):
    image = cv2.imread(str(image_path))
    image[:, :, 1] = 255 - image[:, :, 1]    
    cv2.imwrite(str(image_path), image)

if __name__ == '__main__':
    image_path = Path(sys.argv[1])
    main(image_path)