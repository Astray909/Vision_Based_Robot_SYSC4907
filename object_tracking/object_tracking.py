import cv2
import sys
import os
 
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    n = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
        # if n == 0:
            cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)
            n += 1
        # elif key == ord('q'):
        elif n == 1:
            break

    cv2.destroyWindow(window_name)

def tracking():
    # Set up tracker.
    # Instead of CSRT, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
             tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.legacy.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
 
    # Read video
    # cap = cv2.VideoCapture("input.mp4")
    cap = cv2.VideoCapture(0) # for using CAM

    # Exit if video not opened.
    if not cap.isOpened():
        print("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = cap.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    # Create CSRT tracker object
    tracker = cv2.TrackerCSRT_create()

    # Set initial bounding box coordinates
    bbox = None

    while True:
        # Capture frame from webcam
        ret, frame = cap.read()

        # Check if frame was successfully captured
        if not ret:
            break

        # If bounding box is not set, prompt user to select object to track
        if bbox is None:
            # ROI box background image
            img = cv2.imread("data/roi_sel/roi_sel_img_0.jpg")
        
            # Uncomment the line below to select a different bounding box
            bbox = cv2.selectROI(img, False)
        
            # Initialize tracker with first frame and bounding box
            tracker.init(frame, bbox)

        # Update tracker with new frame
        success, bbox = tracker.update(frame)

        # If tracking was successful, draw bounding box around object
        if success:
            # Calculate size of object in camera's field of view based on distance
            distance = 100  # Example distance in cm from camera
            object_width = bbox[2]  # Width of object in pixels
            fov_width = 60  # Example field of view width in degrees
            pixel_width = frame.shape[1]  # Width of frame in pixels
            size_in_fov = (object_width / pixel_width) * fov_width
            actual_size = (size_in_fov / 360) * (2 * distance * 100)  # Multiply by 2 to get diameter of object
            
            # Draw bounding box with adjusted size
            bbox = tuple(map(int, bbox))
            cv2.rectangle(frame, bbox, (0, 255, 0), 2)
            cv2.putText(frame, f"Size: {actual_size:.2f} cm", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display frame with bounding box
        cv2.imshow("Frame", frame)

        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__' :
    save_frame_camera_key(0, 'data/roi_sel', 'roi_sel_img')
    tracking()
