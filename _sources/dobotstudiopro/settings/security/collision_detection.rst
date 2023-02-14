===================
Collision Detection
===================

Collision detection is mainly used for reducing the impact on the robot to avoid damage to the
robot or external equipment. If the collision detection feature is activated, the robot arm will
pause its current execution when a collision is detected.

.. image:: images/collision_detection.jpg
    :align: center

After collision detection is enabled, the safety level will be displayed in the connection panel on
the top toolbar.

.. image:: images/collision_detection_status.jpg
    :align: center

When collision is detected when jogging the robot, the "Collision Detection" window will pop up. In
this case, you need to resolve the collision and click **Reset**. If you need to operate the
software to resolve the collision, click **Remind me in a minute** to temporarily close the pop-up
window (a pop-up message will be displayed again in one minute).

.. image:: images/collision_detected.jpg
    :align: center

Post-collision Processing
=========================

Post-collision processing refers to the treatment after collision while the robot arm is running the project:

*   **Stop**: The robot arm stops running the project.
*   **Pause**: The robot arm pauses. You need to select whether to resume the operation after
    solving the cause of the collision according to the actual condition, or stop the operation.
*   **Enter drag mode**: The robot arm stops running the project and automatically enters drag
    mode.
*   **Enter fallback mode**: The robot arm automatically backs off the specified distance according
    to the trajectory before the collision. The fallback distance range is 0~50mm.

.. image:: images/collision_post.jpg
    :align: center
