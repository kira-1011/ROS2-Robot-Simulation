import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32


class KeyboardListener(Node):
    def __init__(self):
        super().__init__("keyboard_listener")
        self.subscription = self.create_subscription(
            Int32, "/keyboard/keypress", self.move_by_key, 10
        )
        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)

    def move_by_key(self, msg):
        key = msg.data
        if key == 16777235:
            self.get_logger().info("Key pressed: Up")
            msg = Twist()
            msg.linear.x = -0.5
            self.publisher.publish(msg)
        elif key == 16777237:
            self.get_logger().info("Key pressed: Down")
            msg = Twist()
            msg.linear.x = 0.5
            self.publisher.publish(msg)
        elif key == 16777234:
            self.get_logger().info("Key pressed: Left")
            msg = Twist()
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.publisher.publish(msg)
        elif key == 16777236:
            self.get_logger().info("Key pressed: Right")
            msg = Twist()
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardListener()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
