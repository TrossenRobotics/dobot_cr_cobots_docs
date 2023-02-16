===================
Protocol Definition
===================

This section provides a description of the protocol used to communicate with the Dobot CR-Series
cobot through a remote workstation over a network.

.. note::

    Your CR-Series cobot must be running on firmware ``v3.5.1.19`` or greater.

Message Format
==============

According to the design, CR robots will use ports ``29999``, ``30003``, ``30004``, ``30005`` and
``30006``.

*   Server port ``29999`` (hereinafter referred to as Dashboard port) is responsible for receiving
    some simple commands by sending and receiving one by one. That is, after receiving the agreed
    message format from the client, the Dashboard port will give feedback to the client.
*   Server port ``30003`` (hereinafter referred to as the real-time feedback port) feeds back the
    robot information. It only receives the agreed message format from the client but does not give
    feedback. (Note: Port ``30003`` port is split into port ``30003`` and port ``30004``, which is
    expected to be implemented in controller version 3.5.2. Controller version 3.5.1 currently has
    only one ``30003`` port for real-time feedback or sending motion commands.)
*   Server port ``30004`` (hereinafter referred to as real-time feedback port) feeds back robot
    information every 8ms. Port ``30005`` provides robot information every 200ms. Port ``30006`` is
    a configurable port to feed back robot information. By default, port ``30006`` provides
    feedback every 50ms.

.. note::

    Commands are not case-sensitive. ``ENABLEROBOT()``, ``enablerobot()``, and ``eNabLErobOt()``
    are treated the same and will all enable the robot.

Format When Sending Messages
----------------------------

::

    Message name(Param1,Param2,Param3,...Paramn)

The message format is shown as above. It consists of a message name with parameters in a bracket.
Each parameter is separated by an English comma “,”. A complete message ends with a right
parenthesis.

Both message commands and message responses are in ASCII format (string).

Format When Receiving Messages
------------------------------

::

    "ErrorID,{value,...,valuen},Message name(Param1,Param2,Param3,...Paramn);"

The return message format is shown above. An ``ErrorID`` of zero indicates that the command was
received successfully. If the ErrorID is non-zero value, it indicates an error has occurred in the
command. See :ref:`Error Code Descriptions <tcpip-protocol-error-code-descriptions>` for a detailed
description.

``{value1,value2,value3,...Valuen}`` represents the return value. If there is no return value,
``{}`` will be returned.

``Message name (Param1,Param2,Param3......Paramn)`` reflects the content delivered.

For example, the command:

::

    MovL(-500,100,200,150,0,90)

returns:

::

    "0,{},MovL(-500,100,200,150,0,90); //0"

This return value indicates that the command was received successfully. If there is no return
value, ``{}`` will be returned.

The command:

::

    Mov(-500,100,200,150,0,90)

returns:

::

    "-10000,{},Mov(-500,100,200,150,0,90); //-10000"

This return value indicates a command error. If there is no return value, ``{}`` will be returned.

Dashboard Port Commands
=======================

The upper computer can directly send some simple commands to the robot through port ``29999``. The
Dashboard commands can be used to control the robot like enabling/disabling the robot, resetting
the robot, and setting I/O statuses.

EnableRobot
-----------

*   **Function**: ``EnableRobot()``
*   **Description**: Enable the robot
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},EnableRobot();``
*   **Optional parameters**: Number of optional parameters: 0, 1, or 4. The one parameter command
    provides the payload weight. The four parameters command provides the payload weight, centerX,
    centerY, and centerZ respectively.

.. list-table::
    :header-rows: 1
    :widths: 20 10 40

    * - Parameter
      - Type
      - Description
    * - load
      - double
      - Payload weight (kg):

        * CR3/CR3L load range: 3kg
        * CR5/CR5D load range: 5kg
        * CR7 load range: 7kg
        * CR10 load range: 10kg
        * CR12 load range: 12kg
        * CR16 load range: 16kg
    * - centerX
      - double
      - Payload offset distance in X direction: -500mm - 500mm
    * - centerY
      - double
      - Payload offset distance in Y direction: -500mm - 500mm
    * - centerZ
      - double
      - Payload offset distance in Z direction: -500mm - 500mm

::

    EnableRobot()

DisableRobot
------------

*   **Function**: ``DisableRobot()``
*   **Description**: Disable the robot
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},DisableRobot();``
*   **Parameters**: None

::

    DisableRobot()

ClearError
----------

*   **Function**: ``ClearError()``
*   **Description**: Clear robot alarms. After clearing alarms, the user can check whether the
    robot is still in the alarm state using `RobotMode`_. For alarms that cannot be cleared,
    restart the control cabinet. (Refer to `GetErrorID`_)
*   **Return**: ``ErrorID,{},ClearError();``
*   **Supported Port**: ``29999``
*   **Parameters**: None

::

    ClearError()

ResetRobot
----------

*   **Function**: ``ResetRobot()``
*   **Description**: Stop the robot's current execution
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},ClearError();``
*   **Parameters**: None

::

    ResetRobot()

SpeedFactor
-----------

*   **Function**: ``SpeedFactor(ratio)``
*   **Description**: Set the global speed ratio
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SpeedFactor(ratio);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 15 10 40

    * - Parameter
      - Type
      - Description
    * - ratio
      - int
      - speed ratio, range: 0 - 100 exclusive

::

    SpeedFactor(80)

User
----

*   **Function**: ``User(index)``
*   **Description**: Select the specified user coordinate system
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},User(index); //ErrorID: -1 indicates that the user coordinate index
    does not exist.``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 15 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Select the specified user coordinate system, range: 0 - 9

::

    User(1)

Tool
----

*   **Function**: ``Tool(index)``
*   **Description**: Select the specified tool coordinate system
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},Tool(index); //ErrorID: -1 indicates that the tool coordinate index
    does not exist.``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 15 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Select the specified tool coordinate system, range: 0 - 9

::

    Tool(1)

RobotMode
---------

*   **Function**: ``RobotMode()``
*   **Description**: Get the current mode of robot
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{Value},RobotMode(); //Value is the robot mode value``
*   **Parameters**: None

::

    RobotMode()

*   Return:

.. list-table::
    :header-rows: 1
    :widths: 5 10 40

    * - Mode
      - Description
      - Note
    * - 1
      - ROBOT_MODE_INIT
      - Initialization
    * - 2
      - ROBOT_MODE_BRAKE_OPEN
      - Brake is released
    * - 3
      -
      - Reserved
    * - 4
      - ROBOT_MODE_DISABLED
      - Robot is disabled (brake is not released)
    * - 5
      - ROBOT_MODE_ENABLE
      - Robot is enable (idle)
    * - 6
      - ROBOT_MODE_BACKDRIVE
      - Robot is in dragging state
    * - 7
      - ROBOT_MODE_RUNNING
      - Robot is running
    * - 8
      - ROBOT_MODE_RECORDING
      - Robot is in dragging recording mode
    * - 9
      - ROBOT_MODE_ERROR
      - Robot is in alarm state
    * - 10
      - ROBOT_MODE_PAUSE
      - Robot is paused
    * - 11
      - ROBOT_MODE_JOG
      - Robot is in jogging state

.. note::

    In order to maintain compatibility with controller version 3.5.1, the return value of robot
    status is not modified, such as: idle, drag, running, alarm state. Brake releasing, trajectory
    recording, pause and jog are added.

PayLoad
-------

*   **Function**: ``PayLoad(weight,inertia)``
*   **Description**: Set the current payload
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},PayLoad(weight,inertia);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 15 10 40

    * - Parameter
      - Type
      - Description
    * - weight
      - double
      - load weight kg
    * - inertia
      - double
      - load inertia kg*m^2

::

    PayLoad(3,0.4)

.. note::

    TCP commands LoadSet in Lua. Using LoadSet is the same as calling PayLoad. LoadSet should be
    used with the LoadSwitch command

DO
--

*   **Function**: ``DO(index,status)``
*   **Description**: Set the status of a digital output port on the controller (queue command)
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},DO(index,status);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - digital output index, range: 1 to 16 or 100 to 1000. The value ranges from 100 to 1000 with
        the support of the hardware of the extended I/O module
    * - status
      - bool
      - Status of the digital output port. 1: High level; 0: Low level

::

    DO(1,1)

DOExecute
---------

*   **Function**: ``DOExecute(index,status)``
*   **Description**: Set the status of a digital output port on the controller (immediate execution)
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},DOExecute(index,status);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - digital output index, range: 1 to 16 or 100 to 1000. The value ranges from 100 to 1000 with
        the support of the hardware of the extended I/O module
    * - status
      - bool
      - Status of the digital output port. 1: High level; 0: Low level

::

    DOExecute(1,1)

ToolDO
------

*   **Function**: ``ToolDO(index,status)``
*   **Description**: Set the status of a digital output port on the tool (queue command)
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},ToolDO(index,status);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - digital output index, range: 1 to 16 or 100 to 1000. The value ranges from 100 to 1000 with
        the support of the hardware of the extended I/O module
    * - status
      - bool
      - status of digital output port. 1: high level, 0: low level

::

    ToolDO(1,1)

ToolDOExecute
-------------

*   **Function**: ``ToolDOExecute(index,status)``
*   **Description**: set the status of digital output port of the tool (immediate command)
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},ToolDOExecute(index,status);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - digital output index, range: 1 or 2
    * - 0/1
      - bool
      - status of the digital output port. 1: high level; 0: low level

::

    ToolDOExecute(1,1)

AO
--

*   **Function**: ``AO(index,value)``
*   **Description**: Set the voltage of an analog output port on the controller (queue command)
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},AO(index,value);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - analog output index, range: 1 or 2
    * - value
      - double
      - voltage of corresponding index, range: 0 - 10

::

    AO(1,2)

AOExecute
---------

*   **Function**: ``AOExecute(index,value)``
*   **Description**: Set the voltage of an analog output port on the controller (immediate execution)
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},AOExecute(index,value);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - analog output index, range: 1 or 2
    * - value
      - double
      - voltage of corresponding index, range: 0 - 10

::

    AOExecute(1,2)

AccJ
----

*   **Function**: ``AccJ(R)``
*   **Description**: Set the joint acceleration rate. This command is valid only when the motion
    mode is MovJ, MovJIO, MovJR, or JointMovJ
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},AccJ(R);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - R
      - int
      - joint acceleration rate, range: 1 - 100

::

    AccJ(50)

AccL
----

*   **Function**: ``AccL(R)``
*   **Description**: Set the Cartesian acceleration rate. This command is valid only when the
    motion mode is MovL, MovLIO, MovLR, Jump, Arc, or Circle
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},AccL(R);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - R
      - int
      - Cartesian acceleration rate, range: 1 - 100

::

    AccL(50)

SpeedJ
------

*   **Function**: ``SpeedJ(R)``
*   **Description**: Set the joint velocity rate. This command is valid only when the motion mode
    is MovJ, MovJIO, MovJR, or JointMovJ
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SpeedJ(R);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - R
      - int
      - joint velocity rate, range: 1 - 100

::

    SpeedJ(50)

SpeedL
------

*   **Function**: ``SpeedL(R)``
*   **Description**: Set the Cartesian velocity rate. This command is valid only when the motion
    mode is MovL, MovLIO, MovLR, Jump, Arc, or Circle
*   **Supported Port**: ``29999``
*   **Return**: ````
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - R
      - int
      - Cartesian velocity rate, range: 1 - 100

::

    SpeedL(50)

Arch
----

*   **Function**: ``Arch(Index)``
*   **Description**: Set the index of arc parameters (StartHeight, zLimit, EndHeight) for the Jump
    motion mode
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},Arch(Index);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - Index
      - int
      - arc parameters index, range: 0 - 9

::

    Arch(1)

CP
--

*   **Function**: ``CP(R)``
*   **Description**: Set continuous path (CP) rate. When the robot arm reaches the end point from
    the starting point through an intermediate point, it passes through the intermediate point in a
    right angle or in a curve. This command is invalid for Jump mode.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},CP(R);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - R
      - int
      - continuous path rate, range: 1 - 100

::

    CP(50)

SetArmOrientation
-----------------

*   **Function**: ``SetArmOrientation(LorR,UorD,ForN,Config6)``
*   **Description**: Set the orientation of the arm
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SetArmOrientation(LorR,UorD,ForN,Config6);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 15 10 40

    * - Parameter
      - Type
      - Description
    * - LorR
      - int
      - Arm direction: forward/backward (1/-1)

        * 1: Forward
        * -1: backward

    * - UorD
      - int
      - Arm direction: up the elbow/down the elbow (1/-1)

        * 1: up the elbow
        * -1: down the elbow

    * - ForN
      - int
      - Whether the wrist is reversed (1/-1)

        * 1: wrist is not reversed
        * -1: wrist is reversed

    * - Config6
      - int
      - Sixth axis angle sign

        * -1,-2...

            * -1: Axis 6 Angle is [0,-90], Config6 is -1;
            * -2: Axis 6 Angle is [90, 180], and so on

        * 1,2...

            * 1: axis 6 Angle is [0,90], Config6 is 1;
            * 2: axis 6 Angle is [90180], Config6 is 2, and so on

::

    SetArmOrientation(1,1,-1,1)

PowerOn
-------

*   **Function**: ``PowerOn()``
*   **Description**: Power on the robot
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},PowerOn();``
*   **Parameters**: None

.. note::

  Once the robot is powered on, you can enable the robot after about 10 seconds.

::

    PowerOn()

RunScript
---------

*   **Function**: ``RunScript(projectName)``
*   **Description**: Run the named script
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},RunScript(projectName);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - projectName
      - string
      - script name

::

    RunScript(demo)

StopScript
----------

*   **Function**: ``StopScript()``
*   **Description**: Stop the running script
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},StopScript();``
*   **Parameters**: None

::

    StopScript()

PauseScript
-----------

*   **Function**: ``PauseScript()``
*   **Description**: Pause the running script
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},PauseScript();``
*   **Parameters**: None

::

    PauseScript()

ContinueScript
--------------

*   **Function**: ``ContinueScript()``
*   **Description**: Continue the paused script
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},ContinueScript();``
*   **Parameters**: None

::

    ContinueScript()

SetSafeSkin
-----------

*   **Function**: ``SetSafeSkin(status)``
*   **Description**: Set the state of safe skin
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SetSafeSkin(status));``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - status
      - int
      - safe skin status:

        *   0: Turn off safe skin
        *   1: Turn on safe skin

::

    SetSafeSkin(1)

GetTraceStartPose
-----------------

*   **Function**: ``GetTraceStartPose(traceName)``
*   **Description**: Get the first point of the named trajectory.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{x,y,z,a,b,c},GetTraceStartPose(traceName); //{x,y,z,a,b,c} refers to the
    point coordinates``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - traceName
      - string
      - name of the trajectory file (with the suffix)

::

    GetTraceStartPose(recv_string)

.. note::

    This command is supported in CR controller version 3.5.2 and above

GetPathStartPose
----------------

*   **Function**: ``GetPathStartPose(traceName)``
*   **Description**: Get the first point in the named trajectory playback.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{j1,j2,j3,j4,j5,j6},GetTraceStartPose(traceName); //{j1,j2,j3,j4,j5,j6}
    is the coordinates of joints``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - traceName
      - string
      - name of the trajectory file (with the suffix)

::

    GetPathStartPose(recv_string)

.. note::

    This command is supported in CR controller version 3.5.2 and above.

PositiveSolution
----------------

*   **Function**: ``PositiveSolution(J1,J2,J3,J4,J5,J6,User,Tool)``
*   **Description**: Get the positive solution. Calculate the spatial position of the end of the
    robot based on the given angle of each joint of the robot. The arm direction of the robot is
    required to be known by `SetArmOrientation`_
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{x,y,z,a,b,c},PositiveSolution(J1,J2,J3,J4,J5,J6,User,Tool);
    //{x,y,z,a,b,c} refers to the returned spatial position``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - J1
      - double
      - Position of axis J1 in degrees
    * - J2
      - double
      - Position of axis J2 in degrees
    * - J3
      - double
      - Position of axis J3 in degrees
    * - J4
      - double
      - Position of axis J4 in degrees
    * - J5
      - double
      - Position of axis J5 in degrees
    * - J6
      - double
      - Position of axis J6 in degrees
    * - User
      - int
      - Select the calibrated user coordinate system
    * - Tool
      - int
      - Select the calibrated tool coordinate system

::

    PositiveSolution(0,0,-90,0,90,0,1,1)
    # 0,{473.000000,-141.000000,469.000000,-180.000000,-0.000000,-90.000000},PositiveSolution(0,0,-90,0,90,0,0,0);

InverseSolution
---------------

*   **Function**: ``InverseSolution(X,Y,Z,Rx,Ry,Rz,User,Tool,isJointNear,JointNear)``
*   **Description**: Get the inverse solution. Calculate the angle values of each joint of the
    robot based on the position and attitude of the end of the robot
*   **Supported Port**: ``29999``
*   **Return**:
    ``ErrorID,{J1,J2,J3,J4,J5,J6},InverseSolution(X,Y,Z,Rx,Ry,Rz,User,Tool,isJointNear,JointNear);
    //{J1,J2,J3,J4,J5,J6} is the angle values of each joint. isJointNear,JointNear will be returned
    if there are values delivered``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - X
      - double
      - X-axis position, unit: mm
    * - Y
      - double
      - Y-axis position, unit: mm
    * - Z
      - double
      - Z-axis position, unit: mm
    * - Rx
      - double
      - Position of the Rx axis, units: degrees
    * - Ry
      - double
      - Position of the Ry axis, units: degrees
    * - Rz
      - double
      - Position of the Rx axis, units: degrees
    * - User
      - int
      - Select the calibrated user coordinate system
    * - Tool
      - int
      - Select the calibrated tool coordinate system

*   **Optional Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - isJointNear
      - int
      - Whether to choose the Angle solution. If the value is 1, JointNear data is valid. If the
        value is 0, JointNear data is invalid. The algorithm selects solutions according to the
        current Angle. The default value is 0.
    * - JointNear
      - string
      - Select the Angle values of six joints

Get the Cartesian coordinate value without the selected joint angle to return the joint angle value of the robot.

::

    InverseSolution(473.000000,-141.000000,469.000000,-180.000000,0.000,-90.000,0,0)
    # 0,{0,0,-90,0,90,0},InverseSolution(473.000000,-141.000000,469.000000,-180.000000,0.000,-90.000,0,0);

Get the Cartesian coordinate value of the selected joint angle to return the joint angle value of the robot:

::

    InverseSolution(473.000000,-141.000000,469.000000,-180.000000,0.000,-90.000,0,0,1,{0,0,-90,0,90,0})
    # 0,{0,0,-90,0,90,0},InverseSolution(0,-247,1050,-90,0,180,0,0,1,{0,0,-90,0,90,0});

SetCollisionLevel
-----------------

*   **Function**: ``SetCollisionLevel(level)``
*   **Description**: Set the collision level.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SetCollisionLevel(level);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - level
      - int
      - collision level

        *   0: turn collision detection off
        *   1 - 5: level of sensitivity

::

    SetCollisionLevel(1)

HandleTrajPoints
----------------

*   **Function**: ``HandleTrajPoints(traceName)``
*   **Description**: Preprocessing of trajectory files.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},HandleTrajPoints(traceName);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - traceName
      - string
      - name of the trajectory file (with the suffix)

Deliver ``recv_string`` for preprocessing, and query the preprocessing result at a certain period.

::

    HandleTrajPoints(recv_string)
    HandleTrajPoints()

.. note::

    As the trajectory preprocessing results vary according to the size of the file, and the
    processing time of algorithms will be different. If the user sends this command without
    parameters, it refers to querying the result of the current command. Return: -3 indicates that
    the file content is incorrect; -2 indicates that the file does not exist; -1 indicates that the
    preprocessing is not completed; 0 indicates that preprocessing is completed with no errors; and
    a value greater than 0 indicates that the point corresponding to the current result is fault.

.. note::

    This command is supported in CR controller version 3.5.2 and above.

GetSixForceData
---------------

*   **Function**: ``GetSixForceData()``
*   **Description**: Get six-axis force data
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{Fx,Fy,Fz,Mx,My,Mz},GetSixForceData(); //{Fx,Fy,Fz,Mx,My,Mz} represents
    the original value of six-axis force.``
*   **Parameters**: None

::

    GetSixForceData()
    # Return: 0,{0.0,0.0,0.0,0.0,0.0,0.0},GetSixForceData();

GetAngle
--------

*   **Function**: ``GetAngle()``
*   **Description**: Get the current pose of the robot under the Joint coordinate system
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{J1,J2,J3,J4,J5,J6},GetAngle(); //{J1,J2,J3,J4,J5,J6} refers to the joint
    coordinate of the current pose``
*   **Parameters**: None

::

    GetAngle()
    # 0,{0.0,0.0,90.0,0.0,-90.0,0.0},GetAngle();

GetPose
-------

*   **Function**: ``GetPose(user,tool)``
*   **Description**: get the current pose of the robot under the Cartesian coordinate system


*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{X,Y,Z,Rx,Ry,Rz},GetPose(); //{X,Y,Z,Rx,Ry,Rz} represents the coordinates
    of the current pose under the Cartesian coordinate system``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - user
      - int
      - index of User coordinate system
    * - tool
      - int
      - index of Tool coordinate system

Get the default parameter to the upper computer. Select the pose of the coordinate system. Pass the
index values of user and tool, and return the pose under the specified coordinate system

::

    GetPose()
    # 0,{-473.0,-141.0,469.0,-180.0,0.0,90.0},GetPose();

.. note::

    If you have set the User or Tool coordinate system, the current pose is under the current User
    or Tool coordinate system

EmergencyStop
-------------

*   **Function**: ``EmergencyStop()``
*   **Description**: Trigger an emergency stop
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},EmergencyStop();``
*   **Parameters**: None

::

    EmergencyStop()

ModbusCreate
------------

*   **Function**: ``ModbusCreate(ip,port,slave_id,isRTU)``
*   **Description**: Create a Modbus master, establish connection with the slave.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{index},ModbusCreate(ip,port,slave_id,isRTU);``
*   **Parameters**:


.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - ip
      - string
      - IP address of slave station
    * - port
      - int
      - slave station port
    * - slave_id
      - int
      - ID of slave station
    * - isRTU
      - int
      - This parameter is optional. The value range is 0/1.

        * If the value is null or 0, establish modbusTCP communication.
        * If it is 1, establish modbusRTU communication.

ErrorID: 0 indicates that the Modbus master station is created successfully. -1 indicates that the
Modbus master station fails to be created. For other values, refer to the error code description

index: master station index, which supports a maximum of 5 devices, ranging from 0 to 4.

Establish RTU communication master station (60000 terminal transparent port)

::

    ModbusCreate(127.0.0.1,60000,1,1)

.. note::

    This command is supported in CR controller version 3.5.2 and above.

ModbusClose
-----------

*   **Function**: ``ModbusClose(index)``
*   **Description**: Disconnect from Modbus slave station
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},ModbusClose(index);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Internal index
::

    ModbusClose(0)

.. note::

    This command is supported in CR controller version 3.5.2 and above.

GetInBits
---------

*   **Function**: ``GetInBits(index,addr,count)``
*   **Description**: Read discrete input data
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value1,value2,...,valuen},GetInBits(index,addr,count); //table, it gets
    results {value1,value2...,valuen} by bit``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Internal index
    * - addr
      - int
      - Depending on the slave station configuration
    * - count
      - int
      - The value ranges from 1 to 16

::

    GetInBits(0,3000,5)
    # Normal return: 0,{1,0,1,1,0},GetInBits(0,3000,5);
    # If error: -1,{},GetInBits(0,3000,5);

.. note::

    This command is supported in CR controller version 3.5.2 and above.

GetInRegs
---------

*   **Function**: ``GetInRegs(index,addr,count,valType)``
*   **Description**: read the input register value
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value1,value2,...,valuen},GetInRegs(index,addr,count,valType); //For
    ErrorID, 0 means normal, and -1 means failing to be obtained; For table, it returns
    {value1,value2...,valuen} by variable type``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Internal index
    * - addr
      - int
      - Depending on the slave station configuration
    * - count
      - int
      - The value ranges from 1 to 4
    * - valType
      - string
      - Optional parameters:

        *   U16: read 16-bit unsigned integer ( two bytes, occupy one register)
        *   U32: read 32-bit unsigned integer (four bytes, occupy two registers)
        *   F32: read 32-bit single-precision floating-point number (four bytes, occupy two
            registers)
        *   F64: read 64-bit double-precision floating-point number (eight bytes, occupy four
            registers)

::

    GetInRegs(0,4000,3)
    # Normal: 0,{5,18,12},GetInRegs(0,4000,3);
    # Error: -1,{},GetInRegs(0,4000,3);

.. note::

    This command is supported in CR controller version 3.5.2 and above.

GetCoils
--------

*   **Function**: ``GetCoils(index,addr,count)``
*   **Description**: read the coil register
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value1,value2,…,valuen},GetCoils(index,addr,count); //For ErrorID, 0
    means normal, and -1 means failing to be obtained; For table, it returns
    {value1,value2...,valuen} by variable type``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Internal index
    * - addr
      - int
      - Depending on the slave station configuration
    * - count
      - int
      - The value ranges from 1 to 16

::

    GetCoils(0,1000,3)
    # Normal: 0,{1,1,0},GetCoils(0,1000,3);
    # Error: -1,{},GetCoils(0,1000,3);

.. note::

    This command is supported in CR controller version 3.5.2 and above.

SetCoils
--------

*   **Function**: ``SetCoils(index,addr,count,valTab)``
*   **Description**: write the coil register.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SetCoils(index,addr,count,valTab); //For ErrorID, 0 means normal, and
    -1 means failing to be set``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Internal index
    * - addr
      - int
      - Depending on the slave station configuration
    * - count
      - int
      - The value ranges from 1 to 16
    * - valTab
      - string
      - address of the coils

::

    SetCoils(0,1000,3,{1,0,1})
    # Normal: 0,{},SetCoils(0,1000,3,{1,0,1});
    # Error: -1,{},SetCoils(0,1000,3,{1,0,1});

.. note::

    This command is supported in CR controller version 3.5.2 and above.

GetHoldRegs
-----------

*   **Function**: ``GetHoldRegs(index,addr, count,valType)``
*   **Description**: read the holding register value
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value1,value2,…,valuen},GetHoldRegs(index,addr, count,valType); //For
    ErrorID, 0 means normal, and -1 means failing to be obtained; For table, it returns
    {value1,value2...,valuen} by variable type``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Internal index, supporting at most five devices, range: 0~4

    * - addr
      - int
      - address of the holding registers. Depending on the slave station configuration
    * - count
      - int
      - number of the holding registers
    * - valType
      - string
      - *   U16: read 16-bit unsigned integer ( two bytes, occupy one register)
        *   U32: read 32-bit unsigned integer (four bytes, occupy two registers)
        *   F32: read 32-bit single-precision floating-point number (four bytes, occupy two
            registers)
        *   F64: read 64-bit double-precision floating-point number (eight bytes, occupy four
            registers)

Read a 16-bit unsigned integer starting at address 3095

::

    GetHoldRegs(0,3095,1)
    # Normal: 0,{13},GetHoldRegs(0,3095,1);
    # Error: -1,{},GetHoldRegs(0,3095,1);

.. note::

    This command is supported in CR controller version 3.5.2 and above.

SetHoldRegs
-----------

*   **Function**: ``SetHoldRegs(index,addr, count,valTab,valType)``
*   **Description**: write to a holding register
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SetHoldRegs(index,addr, count,valTab,valType);//For ErrorID, 0 means
    normal, and -1 means failing to be set``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - Internal index, supporting at most five devices, range: 0 - 4
    * - addr
      - int
      - address of the holding registers. Depending on the slave station configuration
    * - count
      - int
      - number of the holding registers to read. The value ranges from 1 to 4.
    * - valTab
      - int
      - number of the holding registers
    * - valType
      - string
      - *   U16: read 16-bit unsigned integer ( two bytes, occupy one register)
        *   U32: read 32-bit unsigned integer (four bytes, occupy two registers)
        *   F32: read 32-bit single-precision floating-point number (four bytes, occupy two registers)
        *   F64: read 64-bit double-precision floating-point number (eight bytes, occupy four registers)


Starting at address 3095, write two 16-bit unsigned integer values 6000,300

.. code-block:: text

    SetHoldRegs(0,3095,2,{6000,300}, U16)
    # Normal: 0,{},SetHoldRegs(0,3095,2,{6000,300}, U16);
    # Error: -1,{},SetHoldRegs(0,3095,2,{6000,300}, U16);

.. note::

    This command is supported in CR controller version 3.5.2 and above.

GetErrorID
----------

*   **Function**: ``GetErrorID()``
*   **Description**: Get the robot error code
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{[[id,…,id], [id], [id], [id], [id], [id], [id]]},GetErrorID();//[id,...,
    id] is the alarm information of the controller and algorithm, where the collision detection
    value is -2, the safe skin collision detection value is -3. The last six [id] represent the
    alarm information of six servos respectively.``
*   **Parameters**: None

::

    GetErrorID()
    # 0,{[[-2],[],[],[],[],[]]},GetErrorId();

.. node::

    Note: For error code description, see `alarm_controller.json`_ and `alarm_servo.json`_

.. note::

    This command is supported in CR controller version 3.5.2 and above.

DI
--

*   **Function**: ``DI(index)``
*   **Description**: get the status of the digital input port.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value},DI(index);//value: the current index status value. The value
    range is 0/1.``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - digital input index, range: 1 - 32 or 100 - 1000. The value range is 100 - 1000 only when
        you configure the extended I/O module

::

    DI(1)
    # 0,{0},DI(1);

ToolDI
------

*   **Function**: ``ToolDI(index)``
*   **Description**: get the status of tool digital input port
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value},ToolDI(index); //value: port status of corresponding index,
    range: 1 or 0``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - digital input index, range: 1 or 2

::

    ToolDI(2)
    # 0,{1},ToolDI(2);

AI
--------------

*   **Function**: ``AI(index)``
*   **Description**: get the voltage of analog input port of controller (immediate command).
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value},AI(index); //value: voltage of corresponding index``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - index of controller, range: 1 or 2
::

    AI(2)
    # 0,{3.5},AI(2);

ToolAI
--------------

*   **Function**: ``ToolAI(index)``
*   **Description**: get the voltage of terminal analog input (immediate command).
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value},ToolAI(index); //value: voltage of corresponding index``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index
      - int
      - index of terminal analog input, range: 1 or 2

::

    ToolAI(1)
    # 0,{1.5},ToolAI(1);

DIGroup
--------------

*   **Function**: ``DIGroup(index_1,index_2,...,index_n)``
*   **Description**: get the state of a group of digital input ports
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{value1,value2,...,valuen},DIGroup(index_1,index_2,...,index_n);
    //value1...valuen: current voltage from index_1 to index_n``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 5 5 40

    * - Parameter
      - Type
      - Description
    * - index_1
      - int
      - index of digital input port, range: 1 - 32 or 100 - 1000. The value range is 100 - 1000
        only when you configure the extended I/O module
    * - ...
      - ...
      - ...
    * - index_n
      - int
      - index of digit input port, range: 1 - 32 or 100 - 1000. The value range is 100 - 1000 only
        when you configure the extended I/O module

::

    DIGroup(4,6,2,7)
    # 0,{1,0,1,1},DIGroup(4,6,2,7);

The obtained level of input ports [4, 6, 2, 7] is [1, 0, 1, 1] respectively

DOGroup
--------------

*   **Function**: ``DOGroup(index_1,value_1,index2,value2,...,index_n,value_n)``
*   **Description**: set the state of a group of digital output ports
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},DOGroup(index_1,value_1,index2,value2,...,index_n,value_n);``
*   **Parameters**: the maximum number of parameters is 64

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - index_1
      - int
      - index of digit output port, range: 1 - 16 or 100 - 1000.
    * - value_1
      - int
      - the status of the digital output port. The value is 0 or 1
    * - ...
      - ...
      - ...
    * - index_n
      - int
      - index of digit output port, range: 1 - 16 or 100 - 1000.
    * - value_n
      - int
      - the status of the digital output port. The value is 0 or 1

Set output ports 4, 6, 2, and 7 to 1, 0, 1 and 0 respectively

::

    DOGroup(4,1,6,0,2,1,7,0)
    # 0,{},DOGroup(4,1,6,0,2,1,7,0);

BrakeControl
--------------

*   **Function**: ``BrakeControl(axisID,value)``
*   **Description**: Control brake. The control of the brake should be carried out under the
    condition that the robot is enabled, otherwise the robot will return -1 by error.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},BrakeControl(axisID,value);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - axisID
      - int
      - ID of the joint axis
    * - value
      - int
      - brake status:

        *   0: disable the brake
        *   1: enable the brake

Open the brake on joint 1.

::

    BrakeControl(1,1)
    # 0,{},BrakeControl(1,1);

.. note::

    This command is supported in CR controller version 3.5.2 and above.

StartDrag
--------------

*   **Function**: ``StartDrag()``
*   **Description**: Enter drag mode(in error state, can not enter drag mode).
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},StartDrag();``
*   **Parameters**: None

::

    StartDrag()

.. note::

    This command is supported in CR controller version 3.5.2 and above.

StopDrag
--------------

*   **Function**: ``StopDrag()``
*   **Description**: Stop Drag mode
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},StopDrag();``
*   **Parameters**: None

::

    StopDrag()

.. note::

    This command is supported in CR controller version 3.5.2 and above.

SetCollideDrag
--------------

*   **Function**: ``SetCollideDrag(status)``
*   **Description**: Set whether drag is forced to enter (can enter drag even in error state).
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SetCollideDrag(status);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - status
      - int
      - force drag switch state:

        *   0: disables the brake
        *   1: enable the brake

Forcibly entry drag mode.

::

    SetCollideDrag(0)

.. note::

    This command is supported in CR controller version 3.5.2 and above.

SetTerminalKeys
--------------

*   **Function**: ``SetTerminalKeys(status)``
*   **Description**: Set the terminal button to enable.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},SetTerminalKeys(status);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - status
      - int
      - status of terminal button:

        *   0: disable
        *   1: enable

The terminal button is disabled

::

    SetTerminalKeys(0)

.. note::

    This command is supported in CR controller version 3.5.2 and above.

SetTerminal485
--------------

*   **Function**: ``SetTerminal485(baudRate, dataLen, parityBit, stopBit)``
*   **Description**: set the terminal 485 parameter
*   **Supported Port**: ``29999``
*   **Return**: ````
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - baudRate
      - int
      - baud rate
    * - dataLen
      - int
      - data bit, currently fixed to 8
    * - parityBit
      - string
      - it is fixed to N, indicating no parity
    * - stopBit
      - int
      - stop bit, currently fixed to 1

Set the baud rate to 115200

::

    SetTerminal485(115200, 8, N, 1)

.. note::

    This command is supported only in certain versions.

GetTerminal485
--------------

*   **Function**: ``GetTerminal485()``
*   **Description**: get the terminal 485 parameter
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{baudRate, dataLen, parityBit, stopBit},GetPose(); //{baudRate, dataLen,
    parityBit, stopBit} represents baud rate, data bit, parity check bit and stop bit
    respectively.``
*   **Parameters**: None

::

    GetTerminal485()
    # 0,{115200, 8, N, 1},GetTerminal485();

.. note::

    This command is supported only in certain versions.

LoadSwitch
--------------

*   **Function**: ``LoadSwitch(status)``
*   **Description**: set the load setting state.
*   **Supported Port**: ``29999``
*   **Return**: ``ErrorID,{},LoadSwitch(status);``
*   **Parameters**:

.. list-table::
    :header-rows: 1
    :widths: 10 10 40

    * - Parameter
      - Type
      - Description
    * - status
      - int
      - set the load setting state:

        *   0: off
        *   1: on. Enabling load Settings increases collision sensitivity

::

    LoadSwitch(1)


Communication Protocol — Real-time Feedback Port
================================================

Port 30003 (real-time feedback port) is not only used to send motion-related protocols, but has
other functions. The client can receive the robot information every 20ms, as shown in the following
table. Each packet received through the real-time feedback port has 1440 bytes, which are arranged
in a standard format. The following table shows the order of the bytes.

+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Meaning                     | Type             | Number of values   | Size in bytes   | Byte position value   | Notes                                                                                                                                         |
+=============================+==================+====================+=================+=======================+===============================================================================================================================================+
| Message Size                | unsigned short   | 1                  | 2               | 0000 ~ 0001           | Total message length in bytes                                                                                                                 |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
|                             | unsigned short   | 3                  | 6               | 0002 ~ 0007           | Reserved bits                                                                                                                                 |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Digital input bits          | double           | 1                  | 8               | 0008 ~ 0015           | Current state of the digital inputs                                                                                                           |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Digital outputs             | double           | 1                  | 8               | 0016 ~ 0023           | digital output                                                                                                                                |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Robot Mode                  | double           | 1                  | 8               | 0024 ~ 0031           | Robot mode                                                                                                                                    |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Controller Timer            | double           | 1                  | 8               | 0032 ~ 0039           | Controller realtime thread execution time                                                                                                     |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Time                        | double           | 1                  | 8               | 0040 ~ 0047           | Time elapsed since the controller was started                                                                                                 |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| test\_value                 | double           | 1                  | 8               | 0048 ~ 0055           | Standard values for memory structure test: 0x0123 4567 89AB CDEF                                                                              |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Safety Mode                 | double           | 1                  | 8               | 0056 ~ 0063           | Safety mode                                                                                                                                   |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Speed scaling               | double           | 1                  | 8               | 0064 ~ 0071           | Speed scaling of the trajectory limiter                                                                                                       |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Linear momentum norm        | double           | 1                  | 8               | 0072 ~ 0079           | Norm of Cartesian linear momentum                                                                                                             |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| V main                      | double           | 1                  | 8               | 0080 ~ 0087           | Masterboard: Main voltage                                                                                                                     |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| V robot                     | double           | 1                  | 8               | 0088 ~ 0095           | Masterboard: Robot voltage (48V)                                                                                                              |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| I robot                     | double           | 1                  | 8               | 0096 ~ 0103           | Masterboard: Robot current                                                                                                                    |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Program state               | double           | 1                  | 8               | 0104 ~ 0111           | Program state                                                                                                                                 |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Safety Status               | double           | 1                  | 8               | 0112 ~ 0119           | Safety status                                                                                                                                 |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Tool Accelerometer values   | double           | 3                  | 24              | 0120 ~ 0143           | Tool x,y and z accelerometer values                                                                                                           |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Elbow position              | double           | 3                  | 24              | 0144 ~ 0167           | Elbow position                                                                                                                                |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Elbow velocity              | double           | 3                  | 24              | 0168 ~ 0191           | Elbow velocity                                                                                                                                |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| q target                    | double           | 6                  | 48              | 0192 ~ 0239           | Target joint positions                                                                                                                        |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| qd target                   | double           | 6                  | 48              | 0240 ~ 0287           | Target joint velocities                                                                                                                       |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| qdd target                  | double           | 6                  | 48              | 0288 ~ 0335           | Target joint accelerations                                                                                                                    |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| I target                    | double           | 6                  | 48              | 0336 ~ 0383           | Target joint currents                                                                                                                         |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| M target                    | double           | 6                  | 48              | 0384 ~ 0431           | Target joint moments (torques)                                                                                                                |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| q actual                    | double           | 6                  | 48              | 0432 ~ 0479           | Actual joint positions                                                                                                                        |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| qd actual                   | double           | 6                  | 48              | 0480 ~ 0527           | Actual joint velocities                                                                                                                       |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| I actual                    | double           | 6                  | 48              | 0528 ~ 0575           | Actual joint currents                                                                                                                         |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| I control                   | double           | 6                  | 48              | 0576 ~ 0623           | Joint control currents(temporally replaced by 0)                                                                                              |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Tool vector actual          | double           | 6                  | 48              | 0624 ~ 0671           | Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation   |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| TCP speed actual            | double           | 6                  | 48              | 0672 ~ 0719           | Actual speed of the tool given in Cartesian coordinates                                                                                       |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| TCP force                   | double           | 6                  | 48              | 0720 ~ 0767           | Generalised forces in the TCP                                                                                                                 |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Tool vector target          | double           | 6                  | 48              | 0768 ~ 0815           | Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation   |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| TCP speed target            | double           | 6                  | 48              | 0816 ~ 0863           | Target speed of the tool given in Cartesian coordinates                                                                                       |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Motor temperatures          | double           | 6                  | 48              | 0864 ~ 0911           | Temperature of each joint in degrees celsius                                                                                                  |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Joint Modes                 | double           | 6                  | 48              | 0912 ~ 0959           | Joint control modes                                                                                                                           |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| V actual                    | double           | 6                  | 48              | 960 ~ 1007            | Actual joint voltages                                                                                                                         |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
|                             | double           | 54                 | 432             | 1008 ~ 1439           | Reserved bits                                                                                                                                 |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| TOTAL                       |                  | 183                | 1440            |                       | 183 values in a 1440-byte package                                                                                                             |
+-----------------------------+------------------+--------------------+-----------------+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+

Robot Mode returns the mode of robo as follows:

  +--------+-----------------------------------+------------------------------+
  | Mode   | Description                       | Note                         |
  +========+===================================+==============================+
  | -1     | ROBOT\_MODE\_NO\_CONTROLLER       | No controller                |
  +--------+-----------------------------------+------------------------------+
  | 0      | ROBOT\_MODE\_DISCONNECTED         | Disconnect                   |
  +--------+-----------------------------------+------------------------------+
  | 1      | ROBOT\_MODE\_CONFIRM\_SAFETY      | Configure safety parameter   |
  +--------+-----------------------------------+------------------------------+
  | 2      | ROBOT\_MODE\_BOOTING              | Start                        |
  +--------+-----------------------------------+------------------------------+
  | 3      | ROBOT\_MODE\_POWER\_OFF           | Power off                    |
  +--------+-----------------------------------+------------------------------+
  | 4      | ROBOT\_MODE\_POWER\_ON            | Power on                     |
  +--------+-----------------------------------+------------------------------+
  | 5      | ROBOT\_MODE\_IDLE                 | Idle                         |
  +--------+-----------------------------------+------------------------------+
  | 6      | ROBOT\_MODE\_BACKDRIVE            | Drag                         |
  +--------+-----------------------------------+------------------------------+
  | 7      | ROBOT\_MODE\_RUNNING              | Run                          |
  +--------+-----------------------------------+------------------------------+
  | 8      | ROBOT\_MODE\_UPDATING\_FIRMWARE   | Update firmware              |
  +--------+-----------------------------------+------------------------------+
  | 9      | ROBOT\_MODE\_ERROR                | Alarm                        |
  +--------+-----------------------------------+------------------------------+

- Description:

  - If the robot is powered off, the mode is 3.
  - If the robot is powered on but not enabled, the mode is 4;
  - If the robot is enabled successfully, the mode is 5.
  - If the robot enters drag mode (enabled state), the mode is 6;
  - If the robot moves, the mode is 7;
  - Priority: Power on < Idle < Drag = Run < Power off < Alarm
  - Alarm is the top priority. When other modes exist simultaneously, if there is an alarm, the mode is set to 9 first;

The following table shows the motion command protocols supported by the
real-time feedback port. The real-time feedback port only receives
commands but does not give feedback.

+-------------+-------------------------------------------------------------------------------------------------------------+
| Command     | Description                                                                                                 |
+=============+=============================================================================================================+
| `MovJ`_     | point to point movement, the target point is Cartesian point                                                |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `MovL`_     | linear movement, the target point is Cartesian point                                                        |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `JointMovJ`_| point to point movement, the target point is joint point                                                    |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `Jump`_     | Jump movement, only supports Cartesian points                                                               |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `RelMovJ`_  | move to the Cartesian offset position in a point-to-point mode                                              |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `RelMovL`_  | move to the Cartesian offset position in a straight line                                                    |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `MovLIO`_   | set the status of digital output port in straight line movement (can set several groups)                    |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `MovJIO`_   | set the status of digital output port in point-to-point movement, and the target point is Cartesian point   |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `Arc`_      | arc movement, needs to combine with other motion commands                                                   |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `Circle`_   | circular movement, needs to combine with other motion commands                                              |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `ServoJ`_   | dynamic following command based on joint space                                                              |
+-------------+-------------------------------------------------------------------------------------------------------------+
| `ServoP`_   | dynamic following command based on Cartesian space                                                          |
+-------------+-------------------------------------------------------------------------------------------------------------+

MovJ
----

*   **Function**: ``MovJ(X,Y,Z,A,B,C)``
*   **Description**: point to point movement, the target point is Cartesian point
*   **Parameters**:

  +-------------+----------+--------------------------------+
  | Parameter   | Type     | Description                    |
  +=============+==========+================================+
  | X           | double   | X-axis coordinates, unit: mm   |
  +-------------+----------+--------------------------------+
  | Y           | double   | Y-axis coordinates, unit: mm   |
  +-------------+----------+--------------------------------+
  | Z           | double   | Z-axis coordinates, unit: mm   |
  +-------------+----------+--------------------------------+
  | A           | double   | A-axis coordinates, unit: °    |
  +-------------+----------+--------------------------------+
  | B           | double   | B-axis coordinates, unit: °    |
  +-------------+----------+--------------------------------+
  | C           | double   | C-axis coordinates, unit: °    |
  +-------------+----------+--------------------------------+

*   **Supported Port**: ``30003``

::

    MovJ(-500,100,200,150,0,90)

MovL
----

*   **Function**: ``MovL(X,Y,Z,A,B,C)``
*   **Description**: linear movement, the target point is Cartesian point
*   **Parameters**:

  +-------------+----------+--------------------------------+
  | Parameter   | Type     | Description                    |
  +=============+==========+================================+
  | X           | double   | X-axis coordinates, unit: mm   |
  +-------------+----------+--------------------------------+
  | Y           | double   | Y-axis coordinates, unit: mm   |
  +-------------+----------+--------------------------------+
  | Z           | double   | Z-axis coordinates, unit: mm   |
  +-------------+----------+--------------------------------+
  | A           | double   | A-axis coordinates, unit: °    |
  +-------------+----------+--------------------------------+
  | B           | double   | B-axis coordinates, unit: °    |
  +-------------+----------+--------------------------------+
  | C           | double   | C-axis coordinates, unit: °    |
  +-------------+----------+--------------------------------+

*   **Supported Port**: ``30003``

::

    MovL(-500,100,200,150,0,90)

JointMovJ
---------

*   **Function**: ``JointMovJ(J1,J2,J3,J4,J5,J6)``
*   **Description**: point to point movement, the target point is joint point
*   **Parameters**:

  +-------------+----------+---------------------------+
  | Parameter   | Type     | Description               |
  +=============+==========+===========================+
  | J1          | double   | J1 coordinates, unit: °   |
  +-------------+----------+---------------------------+
  | J2          | double   | J2 coordinates, unit: °   |
  +-------------+----------+---------------------------+
  | J3          | double   | J3 coordinates, unit: °   |
  +-------------+----------+---------------------------+
  | J4          | double   | J4 coordinates, unit: °   |
  +-------------+----------+---------------------------+
  | J5          | double   | J5 coordinates, unit: °   |
  +-------------+----------+---------------------------+
  | J6          | double   | J6 coordinates, unit: °   |
  +-------------+----------+---------------------------+

*   **Supported Port**: ``30003``

::

    JointMovJ(0,0,-90,0,90,0)

Jump
----

Not yet implemented!

RelMovJ
-------

*   **Function**: ``RelMovJ(offset1,offset2,offset3,offset4,offset5,offset6)``
*   **Description**: move to the Cartesian offset position in a point-to-point mode
*   **Parameters**:

  +-------------+----------+---------------------------+
  | Parameter   | Type     | Description               |
  +=============+==========+===========================+
  | offset1     | double   | J1-axis offset, unit: °   |
  +-------------+----------+---------------------------+
  | offset2     | double   | J2-axis offset, unit: °   |
  +-------------+----------+---------------------------+
  | offset3     | double   | J3-axis offset, unit: °   |
  +-------------+----------+---------------------------+
  | offset4     | double   | J4-axis offset, unit: °   |
  +-------------+----------+---------------------------+
  | offset5     | double   | J5-axis offset, unit: °   |
  +-------------+----------+---------------------------+
  | offset6     | double   | J6-axis offset, unit: °   |
  +-------------+----------+---------------------------+

*   **Supported Port**: ``30003``

::

    RelMovJ(10,10,10,10,10,10)

RelMovL
-------

*   **Function**: ``RelMovL(offsetX,offsetY,offsetZ)``
*   **Description**: move to the Cartesian offset position in a straight line
*   **Parameters**:

  +-------------+----------+--------------------------------------------------------------+
  | Parameter   | Type     | Description                                                  |
  +=============+==========+==============================================================+
  | offsetX     | double   | X-axis offset in the Cartesian coordinate system; unit: mm   |
  +-------------+----------+--------------------------------------------------------------+
  | offsetY     | double   | Y-axis offset in the Cartesian coordinate system; unit: mm   |
  +-------------+----------+--------------------------------------------------------------+
  | offsetZ     | double   | Z-axis offset in the Cartesian coordinate system; unit: mm   |
  +-------------+----------+--------------------------------------------------------------+

*   **Supported Port**: ``30003``

::

    RelMovL(10,10,10)

MovLIO
------

*   **Function**: ``MovLIO(X,Y,Z,A,B,C,{Mode,Distance,Index,Status},...,{Mode,Distance,Index,Status})``
*   **Description**: set the status of digital output port in straight line movement, and the target point is Cartesian point
*   **Parameters**:

  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Parameter   | Type     | Description                                                                                                                                                                                                                                                                                                               |
  +=============+==========+===========================================================================================================================================================================================================================================================================================================================+
  | X           | double   | X-axis coordinates, unit: mm                                                                                                                                                                                                                                                                                              |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Y           | double   | Y-axis coordinates, unit: mm                                                                                                                                                                                                                                                                                              |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Z           | double   | Z-axis coordinates, unit: mm                                                                                                                                                                                                                                                                                              |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | A           | double   | A-axis coordinates, unit: °                                                                                                                                                                                                                                                                                               |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | B           | double   | B-axis coordinates, unit: °                                                                                                                                                                                                                                                                                               |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | C           | double   | C-axis coordinates, unit: °                                                                                                                                                                                                                                                                                               |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Mode        | int      | mode of Distance. 0: distance percentage; 1: distance away from the starting point or target point                                                                                                                                                                                                                        |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Distance    | int      | move specified distance. If Mode is 0, Distance refers to the distance percentage between the starting point and target point; range: 0~100. If Distance value is positive, it refers to the distance away from the starting point; If Distance value is negative, it refers to the distance away from the target point   |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Index       | int      | digital output index, range: 1~24                                                                                                                                                                                                                                                                                         |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Status      | int      | digital output status, range: 0 or 1                                                                                                                                                                                                                                                                                      |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

*   **Supported Port**: ``30003``

::

    MovLIO(-500,100,200,150,0,90,{0,50,1,0})

MovJIO
------

*   **Function**: ``MovJIO(X,Y,Z,A,B,C,{Mode,Distance,Index,Status},...,{Mode,Distance,Index,Status})``
*   **Description**: set the status of digital output port in point-to-point movement, and the
    target point is Cartesian point
*   **Parameters**:

  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Parameter   | Type     | Description                                                                                                                                                                                                                                                                                                               |
  +=============+==========+===========================================================================================================================================================================================================================================================================================================================+
  | X           | double   | X-axis coordinates, unit: mm                                                                                                                                                                                                                                                                                              |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Y           | double   | Y-axis coordinates, unit: mm                                                                                                                                                                                                                                                                                              |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Z           | double   | Z-axis coordinates, unit: mm                                                                                                                                                                                                                                                                                              |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | A           | double   | A-axis coordinates, unit: °                                                                                                                                                                                                                                                                                               |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | B           | double   | B-axis coordinates, unit: °                                                                                                                                                                                                                                                                                               |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | C           | double   | C-axis coordinates, unit: °                                                                                                                                                                                                                                                                                               |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Mode        | int      | mode of Distance. 0: distance percentage; 1: distance away from the starting point or target point                                                                                                                                                                                                                        |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Distance    | int      | move specified distance. If Mode is 0, Distance refers to the distance percentage between the starting point and target point; range: 0~100. If Distance value is positive, it refers to the distance away from the starting point; If Distance value is negative, it refers to the distance away from the target point   |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Index       | int      | digital output index, range: 1~24                                                                                                                                                                                                                                                                                         |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Status      | int      | digital output status, range: 0 or 1                                                                                                                                                                                                                                                                                      |
  +-------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

*   **Supported Port**: ``30003``

::

    MovJIO(-500,100,200,150,0,90,{0,50,1,0})

Arc
---

*   **Function**: ``Arc(X1,Y1,Z1,A1,B1,C1,X2,Y2,Z2,A2,B2,C2)``
*   **Description**: move from the current position to a target position in an arc interpolated
    mode under the Cartesian coordinate system This command needs to combine with other motion
    commands to obtain the starting point of an arc trajectory

*   **Parameters**:

  +-------------+----------+-----------------------------------------------------+
  | Parameter   | Type     | Description                                         |
  +=============+==========+=====================================================+
  | X1          | double   | X1-axis coordinates of arc center point, unit: mm   |
  +-------------+----------+-----------------------------------------------------+
  | Y1          | double   | Y1-axis coordinates of arc center point, unit: mm   |
  +-------------+----------+-----------------------------------------------------+
  | Z1          | double   | Z1-axis coordinates of arc center point, unit: mm   |
  +-------------+----------+-----------------------------------------------------+
  | A1          | double   | A1-axis coordinates of arc center point, unit: °    |
  +-------------+----------+-----------------------------------------------------+
  | B1          | double   | B1-axis coordinates of arc center point, unit: °    |
  +-------------+----------+-----------------------------------------------------+
  | C1          | double   | C1-axis coordinates of arc center point, unit: °    |
  +-------------+----------+-----------------------------------------------------+
  | X2          | double   | X2-axis coordinates of arc ending point, unit: mm   |
  +-------------+----------+-----------------------------------------------------+
  | Y2          | double   | Y2-axis coordinates of arc ending point, unit: mm   |
  +-------------+----------+-----------------------------------------------------+
  | Z2          | double   | Z2-axis coordinates of arc ending point, unit: mm   |
  +-------------+----------+-----------------------------------------------------+
  | A2          | double   | A2-axis coordinates of arc ending point, unit: °    |
  +-------------+----------+-----------------------------------------------------+
  | B2          | double   | B2-axis coordinates of arc ending point, unit: °    |
  +-------------+----------+-----------------------------------------------------+
  | C2          | double   | C2-axis coordinates of arc ending point, unit: °    |
  +-------------+----------+-----------------------------------------------------+

*   **Supported Port**: ``30003``

Circle
------

*   **Function**: ``Circle(count,X1,Y1,Z1,A1,B1,C1,X2,Y2,Z2,A2,B2,C2)``
*   **Description**: circular movement. This command needs to combine with other motion commands
*   **Parameters**:

  +-------------+----------+---------------------------------+
  | Parameter   | Type     | Description                     |
  +=============+==========+=================================+
  | count       | int      | number of circles               |
  +-------------+----------+---------------------------------+
  | X1          | double   | X1-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | Y1          | double   | Y1-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | Z1          | double   | Z1-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | A1          | double   | A1-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+
  | B1          | double   | B1-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+
  | C1          | double   | C1-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+
  | X2          | double   | X2-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | Y2          | double   | Y2-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | Z2          | double   | Z2-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | A2          | double   | A2-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+
  | B2          | double   | B2-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+
  | C2          | double   | C2-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+

*   **Supported Port**: ``30003``

ServoJ
------

*   **Function**: ``ServoJ(J11,J12,J13,J14,J15,J16)``
*   **Description**: dynamic following command based on joint space
*   **Parameters**:

  +-------------+----------+----------------------------------+
  | Parameter   | Type     | Description                      |
  +=============+==========+==================================+
  | J11         | double   | J11 coordinates of P1, unit: °   |
  +-------------+----------+----------------------------------+
  | J12         | double   | J12 coordinates of P1, unit: °   |
  +-------------+----------+----------------------------------+
  | J13         | double   | J13 coordinates of P1, unit: °   |
  +-------------+----------+----------------------------------+
  | J14         | double   | J14 coordinates of P1, unit: °   |
  +-------------+----------+----------------------------------+
  | J15         | double   | J15 coordinates of P1, unit: °   |
  +-------------+----------+----------------------------------+
  | J16         | double   | J16 coordinates of P1, unit: °   |
  +-------------+----------+----------------------------------+

*   **Supported Port**: ``30003``

::

    ServoJ(0,0,-90,0,90,0)

ServoP
------

*   **Function**: ``ServoP(X1,Y1,Z1,A1,B1,C1)``
*   **Description**: dynamic following command based on Cartesian space
*   **Parameters**:

  +-------------+----------+---------------------------------+
  | Parameter   | Type     | Description                     |
  +=============+==========+=================================+
  | X1          | double   | X1-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | Y1          | double   | Y1-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | Z1          | dou      | Z1-axis coordinates, unit: mm   |
  +-------------+----------+---------------------------------+
  | A1          | double   | A1-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+
  | B1          | double   | B1-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+
  | C1          | double   | C1-axis coordinates, unit: °    |
  +-------------+----------+---------------------------------+

*   **Supported Port**: ``30003``

::

    ServoP(-500,100,200,150,0,90)
