======
Modbus
======

Modbus Overview
===============

The Modbus module. The robot serves as Modbus master. This menu is used to connect Modbus slave.

.. image:: modbus/images/modbus.png
    :align: center

.. list-table::
    :align: center
    :header-rows: 1
    :widths: 5 60

    * - No.
      - Description
    * - 1
      - Click to hide the panel, and click **Modbus** on the right toolbar to restore it.
    * - 2
      - Click to connect Modbus slave. See :ref:`Connecting to the Modbus Slave
        <modbus-connect-slave>` for details.
    * - 3
      - Click to fold the control panel, and click again to unfold the panel.
    * - 4
      - Display register information of connected slaves.

.. _modbus-connect-slave:

Connecting to Modbus Slave
==========================

.. image:: modbus/images/modbus_slave.png
    :align: center

*   **Slave IP**: IP address of Modbus device.
*   **Port**: Port number of Modbus communication.
*   **Slave ID**: Slave device ID.
*   **Function**: Select the function type of the slave device.
*   **Address/Quantity**: Address and number of registers.
*   **Scanning rate**: Time interval of scanning the slave station by the robot arm.
