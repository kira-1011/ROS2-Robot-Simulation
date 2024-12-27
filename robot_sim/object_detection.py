import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO


class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__("object_detection_node")

        self.bridge = CvBridge()

        self.model = YOLO("yolov5nu.pt")

        self.publisher = self.create_publisher(Image, "/camera/detections", 10)
        # Create subscription to camera topic
        self.subscription = self.create_subscription(
            Image,
            "/camera/image_raw",
            self.detect_objects,
            10,
        )

        self.get_logger().info("Object Detection Node has been started")

    def detect_objects(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            results = self.model(cv_image)[0]

            # Get the annotated frame
            annotated_frame = results.plot()

            # convert frame to ros2 image message
            image_msg = self.bridge.cv2_to_imgmsg(annotated_frame, "bgr8")
            self.publisher.publish(image_msg)

            # Display results
            # cv2.imshow("YOLOv5 Detections", annotated_frame)
            # cv2.waitKey(1)

            # # Log detections
            # for box in results.boxes:
            #     class_id = int(box.cls[0])
            #     conf = float(box.conf[0])
            #     class_name = self.model.names[class_id]
            #     self.get_logger().info(
            #         f"Detected {class_name} with confidence {conf:.2f}"
            #     )

        except Exception as e:
            self.get_logger().error(f"Error processing image: {str(e)}")


def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
    rclpy.spin(node)
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
