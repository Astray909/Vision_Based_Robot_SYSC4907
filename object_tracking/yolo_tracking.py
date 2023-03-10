import cv2
import numpy as np

# Load YOLOv4 model
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")

# Set the names of the output layers
output_layer_names = net.getLayerNames()
output_layer_names = [output_layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Load video
cap = cv2.VideoCapture(0)

# Define tracker
tracker = cv2.TrackerCSRT_create()

# Initialize bounding box
bbox = None

while True:
    # Read frame from video
    ret, frame = cap.read()
    if not ret:
        break

    # If the bounding box is not set, use YOLOv4 to detect objects in the frame
    if bbox is None:
        # Preprocess the frame for input to the YOLOv4 model
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        # Run inference on the YOLOv4 model to detect objects
        outputs = net.forward(output_layer_names)

        # Find the class IDs, confidence scores, and bounding boxes for each object detected
        class_ids = []
        confidences = []
        boxes = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * frame.shape[1])
                    center_y = int(detection[1] * frame.shape[0])
                    width = int(detection[2] * frame.shape[1])
                    height = int(detection[3] * frame.shape[0])
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Select the bounding box with the highest confidence score
        max_confidence_index = np.argmax(confidences)
        bbox = boxes[max_confidence_index]
        bbox = (bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3])

        # Initialize the tracker with the bounding box
        tracker.init(frame, bbox)

    # If the bounding box is set, update the tracker
    else:
        # Update the tracker with the new frame
        success, bbox = tracker.update(frame)

        # If the update is successful, draw the bounding box on the frame
        if success:
            bbox = (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

    # Display the frame with the bounding box
    cv2.imshow("Object Tracking", frame)

    # Exit on ESC
    if cv2.waitKey(1) == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
