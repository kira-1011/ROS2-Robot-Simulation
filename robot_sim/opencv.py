import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv_bridge
import cv2
import numpy as np


class OpenCVNode(Node):
    def __init__(self):
        super().__init__("opencv_node")
        self.subscription = self.create_subscription(
            Image, "/camera", self.image_callback, 10
        )

    def image_callback(self, msg):
        bridge = cv_bridge.CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imshow("Image", cv_image)
        cv2.waitKey(1)


def main():
    rclpy.init()
    node = OpenCVNode()
    rclpy.spin(node)
    rclpy.shutdown()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
