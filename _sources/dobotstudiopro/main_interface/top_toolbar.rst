===========
Top Toolbar
===========

Toolbar Overview
================

.. image:: images/top_toolbar.jpg
    :width: 70%
    :align: center

.. list-table::
    :align: center
    :widths: 5 60
    :header-rows: 1

    * - No.
      - Description
    * - 1
      - Dropdown menu containing the following submenus:

        * **Settings**: Opens the :doc:`Settings <../settings>` page
        * **Language**: Choose the language of DobotStudio Pro
        * **Help**: Find help about DobotStudio Pro
        * **Check updates**: View version information
        * **About**: View the components of the software
    * - 2
      - Return to the :doc:`Main Interface <../main_interface>`
    * - 3
      - Connection panel. See :ref:`Connecting to the Robot
        <dobotstudiopro-connecting-to-the-robot>` for details. Settings <>`.
    * - 4
      - :ref:`Alarm log <dobotstudiopro-alarm-log>`
    * - 5
      - Enable robot. See :ref:`Enabling Status <dobotstudiopro-enabling-status>` for details.
    * - 6
      - Global Speed Ratio slider. Sets the speed of the robot during operation. See :doc:`Jog
        Setting <>` for details on calculation of the robot's speed.
    * - 7
      - Emergency Stop button. See :ref:`Emergency Stop button
        <dobotstudiopro-emergency-stop-button>` for details.

.. _dobotstudiopro-alarm-log:

Alarm Log
=========

Alarms can be raised for various reasons including collisions, invalid IK solutions, singularities,
and over-temperature. If an alarm is raised when the robot is running, it will stop execution of
whatever program is running and the Alarm Log icon will update to show the number of alarms.

.. image:: images/alarm_log_raised.jpg
    :align: center

Check the status of the Alarms by clicking on the Alarm Log icon. You will be brought to the Alarm
Log page.

.. image:: images/alarm_page.jpg
    :align: center

Double click on an alarm to view the cause and solution. Once an alarm is solved, press the **Clear
Alarm** button to clear it. You can then resume normal operation of the robot.

.. image:: images/alarm_page_status.jpg
    :align: center

.. _dobotstudiopro-enabling-status:

Enabling Status
===============

The **Enable Robot** button's color corresponds to the robot's status:

.. list-table::
    :align: center
    :header-rows: 1
    :widths: 10 5 20

    * - Color
      - Icon
      - Status
    * - :ref:`Solid Blue <dobotstudiopro-enable-solid-blue>`
      - .. image:: images/enable_blue.jpg
      - Robot is disabled
    * - :ref:`Solid Green <dobotstudiopro-enable-solid-green>`
      - .. image:: images/enable_green.jpg
      - Robot is enabled
    * - :ref:`Flashing Blue <dobotstudiopro-enable-flashing-blue>`
      - .. image:: images/enable_blue.jpg
      - Robot is in drag mode

.. _dobotstudiopro-enable-solid-blue:

Solid Blue
----------

Indicates that the robot is disabled. Click the **Enable Robot** button to be brought to the Load
Enable Modification form. Here you will enter the relative position and weight of any end tooling
attached to the robot. After setting the parameters, click **Confirm Modification** to enable the
robot. The arm will move slightly during its startup routine. After the routine, the **Enable
Robot** button and the indicator light at the end of the arm will turn green, indicating that the
robot is enabled.

.. image:: images/load_form.jpg
    :align: center

.. note::

    The Eccentric coordinate of the end load should be set when the J6 axis is 0°.

.. caution::

    The load value should not exceed the maximum payload of the robot.

.. _dobotstudiopro-enable-solid-green:

Solid Green
-----------

Indicates that the robot is enabled. Click the **Enable Robot** button to disable the robot after
confirming your intent. After the confirmation, the robot will disable. The **Enable Robot** button
and the indicator light at the end of the arm will turn blue, indicating that the robot is
disabled.

.. _dobotstudiopro-enable-flashing-blue:

Flashing Blue
-------------

Indicates that the robot is in drag mode. In this mode, you are unable to disable the robot or
operate it normally via projects, the Jog panel, etc. The robot must be put back into the enabled
state first.

.. _dobotstudiopro-emergency-stop-button:

Emergency Stop Button
=====================

When the Emergency Stop button is pressed, the robot will stop operation and power off. The
Emergency Stop icon will turn red. To re-enable the robot, press the Emergency Stop button again,
power on the robot, and enable it using the **Robot Enable** button.

.. note::

    If the physical emergency stop button is pressed, the Emergency Stop button will not change
    appearance. Before clearing the Emergency Stop alarm, the physical button must be reset,
    typically by turning it clockwise.
