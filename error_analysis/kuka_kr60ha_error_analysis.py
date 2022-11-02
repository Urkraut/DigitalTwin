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
import os
import re

#specification of path and filename
path = "/Users/shay/Desktop/Plots/"
dirname = os.path.dirname(path)
dbName = re.sub('[.db]','',sys.argv[1])
axName = re.sub('[kuka_errorAnalysis_]','',dbName)

#db connection
connection = sql.connect(sys.argv[1])
df = pd.read_sql_query("SELECT * FROM Kuka_Messung", connection)

#3d plot of raw data
fig = plt.figure()
ax = plt.axes(projection='3d')

ax.set_title('Axis ' + axName + '\n' +'Deviation for each direction')
ax.set_xlabel('X-coordinate [mm]', labelpad=10)
ax.set_ylabel('Y-coordinate [mm]', labelpad=10)
ax.set_zlabel('Z-coordinate [mm]', labelpad=10)

#get data for three-dimensional scattered points
xRobotData = np.asarray(list(df.X_robot), dtype=float)
xSimData = np.asarray(list(df.X_sim), dtype=float)
yRobotData = np.asarray(list(df.Y_robot), dtype=float)
ySimData = np.asarray(list(df.Y_sim), dtype=float)
zRobotData = np.asarray(list(df.Z_robot), dtype=float)
zSimData = np.asarray(list(df.Z_sim), dtype=float)
ax.scatter3D(xRobotData, yRobotData, zRobotData, label='Robot data', color='#276E4F')
ax.scatter3D(xSimData, ySimData, zSimData, label='Simulation data', color='#BF5F5F')

ax.legend(loc='upper left')
plt.show()
fig.savefig(os.path.join(dirname, dbName+'_3Dplot.jpg'),
            format='jpg',
            dpi=300,
            bbox_inches='tight')

#get data for two-dimensional graph
fig = plt.figure()
graphX = xRobotData - xSimData
graphY = yRobotData - ySimData
graphZ = zRobotData - zSimData
AxisNumber = 'Axis_' + axName
AxisValue = np.asarray(list(df[AxisNumber]), dtype=float)
totDiff = np.sqrt(np.power(graphX,2) + np.power(graphY,2) + np.power(graphZ,2))
     
#2D plot of deviation in relation to axis value             
plt.plot(AxisValue, graphX, color="#276E4F", linewidth=1, linestyle=":", label="X-error")
plt.plot(AxisValue, graphY, color="#EE6934", linewidth=1, linestyle=":", label="Y-error")
plt.plot(AxisValue, graphZ, color="blue", linewidth=1, linestyle=":", label="Z-error")
plt.plot(AxisValue, totDiff, color="black", linewidth=1, linestyle="-", label="total error")
plt.xlabel("Axis value [°]")
plt.ylabel("Error [mm]")
plt.title('Axis ' + axName + '\n' +'Error in relation to axis value')

plt.grid(True)
plt.legend(loc="upper left")
plt.show()
fig.savefig(os.path.join(dirname, dbName + '_totalError.jpg'),
            format='jpeg',
            dpi=300,
            bbox_inches='tight')

#get data for two-dimensional graph
fig = plt.figure()
if sys.argv[2] == 'XY':
    plt.plot(xRobotData, yRobotData, color="#276E4F", linewidth=1, linestyle=":", label="X/Y-Robot data")
    plt.plot(xSimData, ySimData, color="#EE6934", linewidth=1, linestyle=":", label="X/Y-Sim data")
    plt.xlabel("X-coordinate [mm]")
    plt.ylabel("Y-coordinate [mm]")
    
elif sys.argv[2] == 'XZ':
    plt.plot(xRobotData, zRobotData, color="#276E4F", linewidth=1, linestyle=":", label="X/Z-Robot data")
    plt.plot(xSimData, zSimData, color="#BF5F5F", linewidth=1, linestyle=":", label="X/Z-Sim data")
    plt.xlabel("X-coordinate [mm]")
    plt.ylabel("Z-coordinate [mm]")
    
elif sys.argv[2] == 'YZ':
    plt.plot(yRobotData, zRobotData, color="#276E4F", linewidth=1, linestyle=":", label="Y/Z-Robot data")
    plt.plot(ySimData, zSimData, color="#BF5F5F", linewidth=1, linestyle=":", label="Y/Z-Sim data")
    plt.xlabel("Y-coordinate [mm]")
    plt.ylabel("Z-coordinate [mm]") 

#2D plot of relevant values of simulation compared to reality
plt.grid(True)
plt.legend(loc="upper left")
plt.title('Axis ' + axName + '\n' + 'Comparison of deviation for relevant axes')
plt.show()
fig.savefig(os.path.join(dirname, dbName + '_relevantAxes.jpg'),
            format='jpeg',
            dpi=300,
            bbox_inches='tight')