#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Float64
import tf.transformations
from RL import Model  # neural network model

IMU = [0, 0, 0]

def publish_joints(joint_positions):
    publishers = []
    for i in range(1, 7):
        publishers.append(rospy.Publisher('/my_robot/joint{}_position_controller/command'.format(i), Float64, queue_size=10))
    for pub, position in zip(publishers, joint_positions):
        pub.publish(Float64(position))

def imu_callback(data):
    #https://answers.ros.org/question/69754/quaternion-transformations-in-python/
    global IMU
    quaternion = (
        pose.orientation.x,
        pose.orientation.y,
        pose.orientation.z,
        pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    IMU[0] = euler[0]
    IMU[1] = euler[1]
    IMU[2] = euler[2]

def joint_state_callback(msg):
    global IMU
    arms = [position for name, position in zip(msg.name, msg.position) if name[:3].lower() == 'arm']

    input = IMU + arms
    output = Model(input)

    publish_joints(output)

def listener():
    rospy.init_node('robot_listener', anonymous=True)
    rospy.Subscriber("/imu", Imu, imu_callback)
    rospy.Subscriber("/joint_states", JointState, joint_state_callback)
    rospy.spin()

if __name__ == '__main__':
    print('starting\n')
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
