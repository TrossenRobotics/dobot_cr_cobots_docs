======================
User Coordinate System
======================

When the position of a workpiece is changed or a robot program needs to be reused in multiple
processing systems of the same type, user coordinate systems can be created to simplify
programming. DobotStudio Pro supports up to ten user coordinate systems. User coordinate system 0
is defined as the base coordinate system and cannot be changed.

.. note::

    When creating a user coordinate system, make sure that the reference coordinate system is the
    base coordinate system 0.

A user coordinate system is created by a three-point calibration method. The robot is moved to
three points: A (x1, y1, z1), B (x2, y2, z2), and C (x3, y3, z3). Point A is defined as the origin.
The line from point A to point B defines the positive direction of X-axis. The line at which point
C is perpendicular to X-axis defines the positive direction of Y-axis. The Z-axis is defined via
the right-hand rule.

.. image:: images/right_hand_rule.png
    :align: center

Creating a User Coordinate System
=================================

1.  Click **Add**

.. image:: images/user_coord_sys_add.jpg
    :align: center

2.  Select **Three points setting** in the "Add User Frame: index2" page.

.. image:: images/user_coord_sys_three_pts.jpg
    :align: center

.. note::

    *   When creating a user coordinate system, make sure that the reference coordinate system is
        the base coordinate system 0.
    *   Long pressing **Run To** moves the robot to the set points.

3.  Jog the robot to the point P1 and click **obtain** on the P1 panel.
4.  Jog the robot to the point P2 and click **obtain** on the P2 panel.
5.  Jog the robot to the point P3 and click **obtain** on the P3 panel.
6.  Click **OK**. The user coordinate system is created successfully.

The user coordinate system can be selected when jogging the robot arm.

.. image:: images/user_coord_sys_select.jpg
    :align: center

.. note::

    When creating or modifying a user coordinate system, you can also select **Input settings** and
    directly enter X, Y, Z, Rx, Ry and Rz values.

Other operations
================

Modify a coordinate system
--------------------------
Select a coordinate system and click **Modify**. The procedure to modify an existing coordinate
system is the same as adding a new coordinate system.

Copy a coordinate system
------------------------

Create a new coordinate system based another by selecting a coordinate system and clicking
**copy**. This new system will be the same as the copied one.
