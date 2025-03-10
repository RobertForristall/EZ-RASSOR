#!/usr/bin/env python

"""Listen for POST requests and route data to the appropriate topics.

Written by Tiger Sachse.
Inspired by Camilo Lozano.
"""
import json
import rospy
import threading
import std_msgs.msg
import BaseHTTPServer
import geometry_msgs.msg


def get_custom_handler(publishers):
    """Get a custom HTTP request handler with appropriate publishers."""

    class CustomRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        """Handle JSON POST requests on a simple HTTP server."""

        target_coordinates_publisher = publishers[0]
        autonomous_toggles_publisher = publishers[1]
        wheel_instructions_publisher = publishers[2]
        front_arm_instructions_publisher = publishers[3]
        back_arm_instructions_publisher = publishers[4]
        front_drum_instructions_publisher = publishers[5]
        back_drum_instructions_publisher = publishers[6]
        paver_arm_joint_1_instructions_publisher = publishers[7]
        paver_arm_joint_2_instructions_publisher = publishers[8]
        paver_arm_joint_3_instructions_publisher = publishers[9]
        paver_arm_joint_4_instructions_publisher = publishers[10]
        paver_arm_joint_5_instructions_publisher = publishers[11]
        paver_arm_claw_instructions_publisher = publishers[12]
        paver_arm_controller_instructions_publisher = publishers[13]

        def do_POST(self):
            """Handle all POST requests."""
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            content_length = int(self.headers.getheader("content-length", 0))
            instructions = json.loads(
                self.rfile.read(
                    content_length,
                ),
            )
            self.wfile.write(json.dumps({"status": 200}))
            self._publish_instructions(instructions)

        def _publish_instructions(self, instructions):
            """Publish instructions to their respective topics."""
            if "autonomous_toggles" in instructions:
                self.autonomous_toggles_publisher.publish(
                    int(instructions["autonomous_toggles"]),
                )

            if "target_coordinate" in instructions:
                target_coordinate = geometry_msgs.msg.Point()
                target_coordinate.x = float(
                    instructions["target_coordinate"]["x"]
                )
                target_coordinate.y = float(
                    instructions["target_coordinate"]["y"]
                )
                self.target_coordinates_publisher.publish(target_coordinate)

            if "wheel_instruction" in instructions:
                wheel_instruction = geometry_msgs.msg.Twist()
                if instructions["wheel_instruction"] == "forward":
                    wheel_instruction.linear.x = 1.0
                elif instructions["wheel_instruction"] == "backward":
                    wheel_instruction.linear.x = -1.0
                elif instructions["wheel_instruction"] == "left":
                    wheel_instruction.angular.z = 1.0
                elif instructions["wheel_instruction"] == "right":
                    wheel_instruction.angular.z = -1.0
                self.wheel_instructions_publisher.publish(wheel_instruction)

            if "front_arm_instruction" in instructions:
                self.front_arm_instructions_publisher.publish(
                    instructions["front_arm_instruction"],
                )
            if "back_arm_instruction" in instructions:
                self.back_arm_instructions_publisher.publish(
                    instructions["back_arm_instruction"],
                )
            if "front_drum_instruction" in instructions:
                self.front_drum_instructions_publisher.publish(
                    instructions["front_drum_instruction"],
                )
            if "back_drum_instruction" in instructions:
                self.back_drum_instructions_publisher.publish(
                    instructions["back_drum_instruction"],
                )
            if "paver_arm_joint_1_instruction" in instructions:
                self.paver_arm_joint_1_instructions_publisher.publish(
                    instructions["paver_arm_joint_1_instruction"],
                )
            if "paver_arm_joint_2_instruction" in instructions:
                self.paver_arm_joint_2_instructions_publisher.publish(
                    instructions["paver_arm_joint_2_instruction"],
                )
            if "paver_arm_joint_3_instruction" in instructions:
                self.paver_arm_joint_3_instructions_publisher.publish(
                    instructions["paver_arm_joint_3_instruction"],
                )
            if "paver_arm_joint_4_instruction" in instructions:
                self.paver_arm_joint_4_instructions_publisher.publish(
                    instructions["paver_arm_joint_4_instruction"],
                )
            if "paver_arm_joint_5_instruction" in instructions:
                self.paver_arm_joint_5_instructions_publisher.publish(
                    instructions["paver_arm_joint_5_instruction"],
                )
            if "paver_arm_claw_instruction" in instructions:
                self.paver_arm_claw_instructions_publisher.publish(
                    instructions["paver_arm_claw_instruction"],
                )
            if "robotic_arm_instruction" in instructions:
                base_msg = std_msgs.msg.Float64MultiArray()
                base_msg.data = [0.0, 0.0, 0.0, 0.0, 0.0]
                if instructions["robotic_arm_instruction"] == "armup":
                    base_msg.data[1] = -0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "armdown":
                    base_msg.data[1] = 0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "armleft":
                    base_msg.data[0] = 0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "armright":
                    base_msg.data[0] = -0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "armforward":
                    base_msg.data[2] = -0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "armbackward":
                    base_msg.data[2] = 0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "grabberup":
                    base_msg.data[3] = -0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "grabberdown":
                    base_msg.data[3] = 0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "grabberleft":
                    base_msg.data[0] = 0.1
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "grabberright":
                    base_msg.data[0] = -0.1
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "rotateleft":
                    base_msg.data[4] = 0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == "rotateright":
                    base_msg.data[4] = -0.2
                    self.paver_arm_controller_instructions_publisher.publish(
                        base_msg
                    )
                elif instructions["robotic_arm_instruction"] == 1:
                    self.paver_arm_claw_instructions_publisher.publish(
                        std_msgs.msg.Float32(6)
                    )
                elif instructions["robotic_arm_instruction"] == 0:
                    self.paver_arm_claw_instructions_publisher.publish(
                        std_msgs.msg.Float32(-6)
                    )
                elif instructions["robotic_arm_instruction"] == "pickup":
                    arm_data = std_msgs.msg.Float64MultiArray()
                    arm_data.data = [0.0, 0.0, 0.0, 0.0, 3.0]
                    self.paver_arm_controller_instructions_publisher.publish(
                        arm_data
                    )
                elif instructions["robotic_arm_instruction"] == "place":
                    arm_data = std_msgs.msg.Float64MultiArray()
                    arm_data.data = [1.0, 3.0, 2.0, 0.0, 2.0]
                    self.paver_arm_controller_instructions_publisher.publish(
                        arm_data
                    )
                elif instructions["robotic_arm_instruction"] == "home":
                    arm_data = std_msgs.msg.Float64MultiArray()
                    arm_data.data = [1.0, 2.0, 2.0, 0.0, 5.0]
                    self.paver_arm_controller_instructions_publisher.publish(
                        arm_data
                    )

    return CustomRequestHandler


def kill_server(server, sleep_duration):
    """Wait for roscore to die, then kill the server."""
    try:
        while not rospy.core.is_shutdown():
            rospy.sleep(sleep_duration)
        server.shutdown()
    except Exception:
        server.shutdown()


def start_node(
    default_node_name,
    target_coordinates_topic,
    autonomous_toggles_topic,
    queue_size,
    sleep_duration,
):
    """Start the node and let the fun begin!"""
    try:
        rospy.init_node(default_node_name)

        # Load ROS params into the script.
        port = rospy.get_param(rospy.get_name() + "/port")
        wheel_instructions_topic = rospy.get_param(
            rospy.get_name() + "/wheel_instructions_topic",
        )
        front_arm_instructions_topic = rospy.get_param(
            rospy.get_name() + "/front_arm_instructions_topic",
        )
        back_arm_instructions_topic = rospy.get_param(
            rospy.get_name() + "/back_arm_instructions_topic",
        )
        front_drum_instructions_topic = rospy.get_param(
            rospy.get_name() + "/front_drum_instructions_topic",
        )
        back_drum_instructions_topic = rospy.get_param(
            rospy.get_name() + "/back_drum_instructions_topic",
        )
        paver_arm_joint_1_instructions_topic = rospy.get_param(
            rospy.get_name() + "/paver_arm_joint_1_instructions_topic",
        )
        paver_arm_joint_2_instructions_topic = rospy.get_param(
            rospy.get_name() + "/paver_arm_joint_2_instructions_topic",
        )
        paver_arm_joint_3_instructions_topic = rospy.get_param(
            rospy.get_name() + "/paver_arm_joint_3_instructions_topic",
        )
        paver_arm_joint_4_instructions_topic = rospy.get_param(
            rospy.get_name() + "/paver_arm_joint_4_instructions_topic",
        )
        paver_arm_joint_5_instructions_topic = rospy.get_param(
            rospy.get_name() + "/paver_arm_joint_5_instructions_topic",
        )
        paver_arm_claw_instructions_topic = rospy.get_param(
            rospy.get_name() + "/paver_arm_claw_instructions_topic",
        )
        paver_arm_controller_instructions_topic = rospy.get_param(
            rospy.get_name() + "/paver_arm_controller_instructions_topic"
        )

        # Create a whole heap of publishers.
        target_coordinates_publisher = rospy.Publisher(
            target_coordinates_topic,
            geometry_msgs.msg.Point,
            queue_size=queue_size,
        )
        autonomous_toggles_publisher = rospy.Publisher(
            autonomous_toggles_topic,
            std_msgs.msg.Int8,
            queue_size=queue_size,
        )
        wheel_instructions_publisher = rospy.Publisher(
            wheel_instructions_topic,
            geometry_msgs.msg.Twist,
            queue_size=queue_size,
        )
        front_arm_instructions_publisher = rospy.Publisher(
            front_arm_instructions_topic,
            std_msgs.msg.Float32,
            queue_size=queue_size,
        )
        back_arm_instructions_publisher = rospy.Publisher(
            back_arm_instructions_topic,
            std_msgs.msg.Float32,
            queue_size=queue_size,
        )
        front_drum_instructions_publisher = rospy.Publisher(
            front_drum_instructions_topic,
            std_msgs.msg.Float32,
            queue_size=queue_size,
        )
        back_drum_instructions_publisher = rospy.Publisher(
            back_drum_instructions_topic,
            std_msgs.msg.Float32,
            queue_size=queue_size,
        )
        paver_arm_joint_1_instructions_publisher = rospy.Publisher(
            paver_arm_joint_1_instructions_topic,
            std_msgs.msg.Float64,
            queue_size=queue_size,
        )
        paver_arm_joint_2_instructions_publisher = rospy.Publisher(
            paver_arm_joint_2_instructions_topic,
            std_msgs.msg.Float64,
            queue_size=queue_size,
        )
        paver_arm_joint_3_instructions_publisher = rospy.Publisher(
            paver_arm_joint_3_instructions_topic,
            std_msgs.msg.Float64,
            queue_size=queue_size,
        )
        paver_arm_joint_4_instructions_publisher = rospy.Publisher(
            paver_arm_joint_4_instructions_topic,
            std_msgs.msg.Float64,
            queue_size=queue_size,
        )
        paver_arm_joint_5_instructions_publisher = rospy.Publisher(
            paver_arm_joint_5_instructions_topic,
            std_msgs.msg.Float64,
            queue_size=queue_size,
        )
        paver_arm_claw_instructions_publisher = rospy.Publisher(
            paver_arm_claw_instructions_topic,
            std_msgs.msg.Float32,
            queue_size=queue_size,
        )
        paver_arm_controller_instructions_publisher = rospy.Publisher(
            paver_arm_controller_instructions_topic,
            std_msgs.msg.Float64MultiArray,
            queue_size=queue_size,
        )

        rospy.loginfo("Creating HTTP server...")

        # Create an HTTP server.
        server = BaseHTTPServer.HTTPServer(
            ("", port),
            get_custom_handler(
                (
                    target_coordinates_publisher,
                    autonomous_toggles_publisher,
                    wheel_instructions_publisher,
                    front_arm_instructions_publisher,
                    back_arm_instructions_publisher,
                    front_drum_instructions_publisher,
                    back_drum_instructions_publisher,
                    paver_arm_joint_1_instructions_publisher,
                    paver_arm_joint_2_instructions_publisher,
                    paver_arm_joint_3_instructions_publisher,
                    paver_arm_joint_4_instructions_publisher,
                    paver_arm_joint_5_instructions_publisher,
                    paver_arm_claw_instructions_publisher,
                    paver_arm_controller_instructions_publisher,
                )
            ),
        )

        rospy.loginfo("Creating server kill thread...")

        # Launch a kill thread that kills the server when roscore dies.
        kill_thread = threading.Thread(
            target=kill_server,
            args=(
                server,
                sleep_duration,
            ),
        )
        kill_thread.start()

        rospy.loginfo("Controller server initialized.")

        # Run the server infinitely.
        server.serve_forever(poll_interval=sleep_duration)

    # If anything goes wrong, make sure to shut down the server.
    except Exception:
        server.shutdown()
