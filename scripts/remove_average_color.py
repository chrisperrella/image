import cv2, numpy, sys
from pathlib import Path

def main(image_path):
    image = cv2.imread(str(image_path))

    try:
        alpha = image[:, :, 3]
    except (IndexError, TypeError):
        alpha = None

    image = image[:, :, :3]
    
    average_color = numpy.copy(image)
    average_row = numpy.ma.average(image, axis=0)
    average_color[:] = numpy.ma.average(average_row, axis=0)
    neutral_diffuse = (image / (average_color + 0.0001)).clip(0, 1) * 255

    try:        
        image = numpy.dstack((neutral_diffuse, alpha))
    except (AttributeError, ValueError):
        image = neutral_diffuse
    cv2.imwrite(str(image_path), image)

if __name__ == '__main__':
    image_path = Path(sys.argv[1])
    main(image_path)