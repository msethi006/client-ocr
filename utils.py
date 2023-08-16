import cv2
import numpy as np

def process_ocr_results(image,results):
    output_text = []
    for result_group in results:
        for result in result_group:
            bbox_points = result[0]
            cls_result = result[1][0]
            output_text.append(cls_result)
            bbox = [(int(point[0]), int(point[1])) for point in bbox_points]

            cv2.polylines(image, [np.array(bbox, np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(image, cls_result, (bbox[0][0], bbox[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 10)

    # Convert BGR image to RGB for matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb, output_text