# trace generated using paraview version 5.12.0-RC2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
displacementxdmf = FindSource('displacement.xdmf')

# create a new 'Warp By Vector'
warpByVector1 = WarpByVector(registrationName='WarpByVector1', Input=displacementxdmf)

# find source
displacement_spherexdmf = FindSource('displacement_sphere.xdmf')

UpdatePipeline(time=0.01, proxy=warpByVector1)

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=warpByVector1)

UpdatePipeline(time=0.01, proxy=extractSurface1)

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=extractSurface1)

UpdatePipeline(time=0.01, proxy=slice1)

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=slice1)

# Properties modified on clip1
clip1.Scalars = ['POINTS', '']

UpdatePipeline(time=0.01, proxy=clip1)

# set active source
SetActiveSource(extractSurface1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip1.ClipType)

# create a new 'Clip'
clip2 = Clip(registrationName='Clip2', Input=extractSurface1)

# rename source object
RenameSource('Clip_dome1', clip2)

# Properties modified on clip2
clip2.Scalars = ['POINTS', '']

UpdatePipeline(time=0.01, proxy=clip2)

# set active source
SetActiveSource(warpByVector1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip2.ClipType)

# create a new 'Clip'
clip2_1 = Clip(registrationName='Clip2', Input=warpByVector1)

# rename source object
RenameSource('Clip_sph', clip2_1)

# Properties modified on clip2_1
clip2_1.Scalars = ['POINTS', '']

UpdatePipeline(time=0.01, proxy=clip2_1)

# create a new 'Cell Size'
cellSize1 = CellSize(registrationName='CellSize1', Input=clip2_1)

UpdatePipeline(time=0.01, proxy=cellSize1)

# create a new 'Python Calculator'
pythonCalculator1 = PythonCalculator(registrationName='PythonCalculator1', Input=cellSize1)

# Properties modified on pythonCalculator1
pythonCalculator1.Expression = 'sum(abs(Volume))'
pythonCalculator1.ArrayAssociation = 'Cell Data'

UpdatePipeline(time=0.01, proxy=pythonCalculator1)

# set active source
SetActiveSource(warpByVector1)

# create a new 'Resample With Dataset'
resampleWithDataset1 = ResampleWithDataset(registrationName='ResampleWithDataset1', SourceDataArrays=displacement_spherexdmf,
    DestinationMesh=warpByVector1)

UpdatePipeline(time=0.01, proxy=resampleWithDataset1)

# create a new 'Warp By Vector'
warpByVector2 = WarpByVector(registrationName='WarpByVector2', Input=resampleWithDataset1)

UpdatePipeline(time=0.01, proxy=warpByVector2)

# create a new 'Extract Surface'
extractSurface2 = ExtractSurface(registrationName='ExtractSurface2', Input=warpByVector2)

UpdatePipeline(time=0.01, proxy=extractSurface2)

# create a new 'Slice'
slice2 = Slice(registrationName='Slice2', Input=extractSurface2)

UpdatePipeline(time=0.01, proxy=slice2)

# create a new 'Clip'
clip2_2 = Clip(registrationName='Clip2', Input=slice2)

UpdatePipeline(time=0.01, proxy=clip2_2)

# set active source
SetActiveSource(extractSurface2)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip2_2.ClipType)

# create a new 'Clip'
clip3 = Clip(registrationName='Clip3', Input=extractSurface2)

# rename source object
RenameSource('Clip_dome2', clip3)

UpdatePipeline(time=0.01, proxy=clip3)

# set active source
SetActiveSource(warpByVector2)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip3.ClipType)

# create a new 'Clip'
clip3_1 = Clip(registrationName='Clip3', Input=warpByVector2)

# rename source object
RenameSource('Clip_sph2', clip3_1)

UpdatePipeline(time=0.01, proxy=clip3_1)

# create a new 'Cell Size'
cellSize2 = CellSize(registrationName='CellSize2', Input=clip3_1)

UpdatePipeline(time=0.01, proxy=cellSize2)

# create a new 'Python Calculator'
pythonCalculator2 = PythonCalculator(registrationName='PythonCalculator2', Input=cellSize2)

# Properties modified on pythonCalculator2
pythonCalculator2.Expression = 'sum(abs(Volume))'
pythonCalculator2.ArrayAssociation = 'Cell Data'

UpdatePipeline(time=0.01, proxy=pythonCalculator2)