#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import rospy
import underworlds
import pygame
from controller import PS4Controller


class ROSPS4Controller(PS4Controller):
    def __init__(self):
        self.init()

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while not rospy.is_shutdown():
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

            rospy.logwarn(self.axis_data)
            rospy.logwarn(self.button_data)
            rospy.logwarn(self.hat_data)

class UwdsTeleop(object):
    def __init__(self, ctx, world):
        self.ctx = ctx
        self.world = world
        controller = ROSPS4Controller()
        controller.listen()


if __name__ == "__main__":
    sys.argv = [arg for arg in sys.argv if "__name" not in arg and "__log" not in arg]
    sys.argc = len(sys.argv)

    parser = argparse.ArgumentParser(description="Control with a PS4 controller a specific node from a given world")
    parser.add_argument("world", help="Underworlds world to create")
    args = parser.parse_args()

    rospy.init_node("uwds_teleop", anonymous=False)

    with underworlds.Context("Environment provider") as ctx:
        UwdsTeleop(ctx, args.world)
