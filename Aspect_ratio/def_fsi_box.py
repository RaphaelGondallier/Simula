#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:56:45 2024

@author: Raphael Gondallier de Tugny
"""

# =============================================================================
# Inputs: 
# - Mesh path
# - Parameters of a box in accordance with the definition of the paraview box clip

#
# Action: 
# Modifies the IDs of the points of a mesh which are not inside the defined box. 
# These points become rigid, so the FSI region is inside the box.
# =============================================================================

from dolfin import *
import numpy as np
from math import cos, sin, radians
import pandas as pd

# =============================================================================
# # Inputs
# =============================================================================
mesh_path = "/path/to/mesh.h5"

# Box parameters: (Position, Rotation, Length)
pav_position = 0.0581051762278217, 0.12113347724177015, 0.07047083028173179 # Position of the corner
pav_rotation = -38.357197876882466, -49.451991513570874, -21.137236896999312 # Rotation in degrees
pav_length =  0.001438159201877521, 0.0065222522667031605, 0.004527521944747901 # Length

output_file_name = "boundaries_name.pvd"

# =============================================================================
# Functions
# =============================================================================
# Rotation matrix function
def rotation_matrix(rx, ry, rz):
    R_x = np.array([[1, 0, 0],
                    [0, cos(rx), -sin(rx)],
                    [0, sin(rx), cos(rx)]])
    
    R_y = np.array([[cos(ry), 0, sin(ry)],
                    [0, 1, 0],
                    [-sin(ry), 0, cos(ry)]])
    
    R_z = np.array([[cos(rz), -sin(rz), 0],
                    [sin(rz), cos(rz), 0],
                    [0, 0, 1]])
    
    # Combine rotations
    R = R_z @ R_x @ R_y  # Order might seem counterintuitive but correct
    return R

# Apply inverse rotation to transform points back to box coordinates
def transform_to_local(x, y, z, R, p):
    # Translate point relative to box center
    x_local, y_local, z_local = np.linalg.inv(R) @ np.array([x - p[0], y - p[1], z - p[2]])
    return x_local, y_local, z_local

# =============================================================================
# Main
# =============================================================================
fsi_id = 22  # id for fsi interface
rigid_id = 11  # "rigid wall" id for the fluid and mesh problem
outer_wall_id = 33  # id for the outer surface of the solid

# Read mesh
mesh = Mesh()
hdf = HDF5File(mesh.mpi_comm(), mesh_path, "r")
hdf.read(mesh, "/mesh", False)
boundaries = MeshFunction("size_t", mesh, 2)
hdf.read(boundaries, "/boundaries")
domains = MeshFunction("size_t", mesh, 3)
hdf.read(domains, "/domains")

# Rotation matrix
R = rotation_matrix(*[radians(angle) for angle in pav_rotation])

# Make the points outside of the FSI region rigid
for i, submesh_facet in enumerate(facets(mesh)):
    idx_facet = boundaries.array()[i]
    if idx_facet == fsi_id or idx_facet == outer_wall_id:
        mid = submesh_facet.midpoint()
        x_local, y_local, z_local = transform_to_local(mid.x(), mid.y(), mid.z(), R, pav_position)
        if not all(0 <= coord <= length for coord, length in zip([x_local, y_local, z_local], pav_length)):
            boundaries.array()[i] = rigid_id  # Change ID from "fsi" to "rigid wall"

# Save modified boundaries
File(output_file_name) << boundaries
