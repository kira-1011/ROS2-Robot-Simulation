import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class MoveRobotNode(Node):
    def __init__(self):
        super().__init__("move_robot_node")
        self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
        timer_period = 2
        self.timer = self.create_timer(timer_period, self.publish_velocity_command)

    def publish_velocity_command(self):
        msg = Twist()
        msg._linear._x = 0.1
        msg._angular._z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info(
            f"Publishing cmd_vel: linear.x={msg._linear.x}, angular.z={msg._angular._z}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
