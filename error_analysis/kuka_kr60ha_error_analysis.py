#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 13:34:09 2022

@author: shay
"""

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as sql
import numpy as np
import sys

connection = sql.connect(sys.argv[1])
df = pd.read_sql_query("SELECT * FROM Kuka_Messung", connection)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title('Deviation in relation to axis value')
ax.set_xlabel('X [mm]')
ax.set_ylabel('Y [mm]')
ax.set_zlabel('Z [mm]')


# Data for three-dimensional scattered points
xRobotData = np.asarray(list(df.X_robot), dtype=float)
xSimData = np.asarray(list(df.X_sim), dtype=float)
yRobotData = np.asarray(list(df.Y_robot), dtype=float)
ySimData = np.asarray(list(df.Y_sim), dtype=float)
zRobotData = np.asarray(list(df.Z_robot), dtype=float)
zSimData = np.asarray(list(df.Z_sim), dtype=float)
ax.scatter3D(xRobotData, yRobotData, zRobotData, color='g')
ax.scatter3D(xSimData, ySimData, zSimData, color='r')

plt.show()

#get Data for two-dimensional graphs
graphTime = []
graphX = xRobotData - xSimData
graphY = yRobotData - ySimData
graphZ = zRobotData - zSimData
AxisValue = np.asarray(list(df.Axis_1), dtype=float)
totDiff = np.abs(np.sqrt(np.power(graphX,2) + np.power(graphY,2) + np.power(graphZ,2)))
                  
plt.plot(AxisValue, graphX, color="green", linewidth=1, linestyle=":", label="X")
plt.plot(AxisValue, graphY, color="red", linewidth=1, linestyle=":", label="Y")
plt.plot(AxisValue, graphZ, color="blue", linewidth=1, linestyle=":", label="Z")
plt.plot(AxisValue, totDiff, color="black", linewidth=1, linestyle="-", label="total")
plt.xlabel("Axis value [°]")
plt.ylabel("error [mm]")
plt.title("Deviation in relation to axis value")

plt.legend(loc="upper left")
plt.show()

if sys.argv[2] == 'XY':
    plt.plot(xRobotData, yRobotData, color="green", linewidth=1, linestyle=":", label="X/Y-RobotData")
    plt.plot(xSimData, ySimData, color="red", linewidth=1, linestyle=":", label="X/Y-SimData")
    plt.xlabel("X-coordinate [mm]")
    plt.ylabel("Y-coordinate [mm]")
    
elif sys.argv[2] == 'XZ':
    plt.plot(xRobotData, zRobotData, color="green", linewidth=1, linestyle=":", label="X/Z-RobotData")
    plt.plot(xSimData, zSimData, color="#BF5F5F", linewidth=1, linestyle=":", label="X/Z-SimData")
    plt.xlabel("X-coordinate [mm]")
    plt.ylabel("Z-coordinate [mm]")


plt.legend(loc="upper left")
plt.show()