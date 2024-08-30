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

# set active source
SetActiveSource(displacementxdmf)

# create a new 'Warp By Vector'
warpByVector1 = WarpByVector(registrationName='WarpByVector1', Input=displacementxdmf)
warpByVector1.Vectors = ['POINTS', 'Displacement']

# find source
displacement_spherexdmf = FindSource('displacement_sphere.xdmf')

UpdatePipeline(time=1.110000000000001, proxy=warpByVector1)

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=warpByVector1)

UpdatePipeline(time=1.110000000000001, proxy=extractSurface1)

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=extractSurface1)
clip1.ClipType = 'Plane'
clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = [None, '']

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [0.0802716501057148, 0.1285030022263527, 0.06063699908554554]

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip1.HyperTreeGridClipper.Origin = [0.0802716501057148, 0.1285030022263527, 0.06063699908554554]

# rename source object
RenameSource('Clip_dome1', clip1)

# Properties modified on clip1
clip1.Scalars = ['POINTS', '']

UpdatePipeline(time=1.110000000000001, proxy=clip1)

# set active source
SetActiveSource(extractSurface1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip1.ClipType)

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=extractSurface1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1.PointMergeMethod = 'Uniform Binning'

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0802716501057148, 0.1285030022263527, 0.06063699908554554]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [0.0802716501057148, 0.1285030022263527, 0.06063699908554554]

UpdatePipeline(time=1.110000000000001, proxy=slice1)

# create a new 'Clip'
clip1_1 = Clip(registrationName='Clip1', Input=slice1)
clip1_1.ClipType = 'Plane'
clip1_1.HyperTreeGridClipper = 'Plane'
clip1_1.Scalars = [None, '']

# init the 'Plane' selected for 'ClipType'
clip1_1.ClipType.Origin = [0.0802716463804245, 0.13012881577014923, 0.060179637745022774]

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip1_1.HyperTreeGridClipper.Origin = [0.0802716463804245, 0.13012881577014923, 0.060179637745022774]

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip1_1.ClipType)

# Properties modified on clip1_1
clip1_1.ClipType = 'Sphere'
clip1_1.Scalars = ['POINTS', '']

UpdatePipeline(time=1.110000000000001, proxy=clip1_1)

# set active source
SetActiveSource(clip1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip1_1.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip1.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip1.ClipType)

# Properties modified on clip1
clip1.ClipType = 'Sphere'

# set active source
SetActiveSource(warpByVector1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip1.ClipType)

# create a new 'Clip'
clip2 = Clip(registrationName='Clip2', Input=warpByVector1)
clip2.ClipType = 'Plane'
clip2.HyperTreeGridClipper = 'Plane'
clip2.Scalars = [None, '']

# init the 'Plane' selected for 'ClipType'
clip2.ClipType.Origin = [0.0802716501057148, 0.1285030022263527, 0.06063699908554554]

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip2.HyperTreeGridClipper.Origin = [0.0802716501057148, 0.1285030022263527, 0.06063699908554554]

# Properties modified on clip2
clip2.Scalars = ['POINTS', '']

UpdatePipeline(time=1.110000000000001, proxy=clip2)

# rename source object
RenameSource('Clip_sph', clip2)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip2.ClipType)

# Properties modified on clip2
clip2.ClipType = 'Sphere'

# create a new 'Cell Size'
cellSize1 = CellSize(registrationName='CellSize1', Input=clip2)

UpdatePipeline(time=1.110000000000001, proxy=cellSize1)

# create a new 'Python Calculator'
pythonCalculator1 = PythonCalculator(registrationName='PythonCalculator1', Input=cellSize1)
pythonCalculator1.Expression = ''

# Properties modified on pythonCalculator1
pythonCalculator1.Expression = 'sum(abs(Volume))'
pythonCalculator1.ArrayAssociation = 'Cell Data'

UpdatePipeline(time=1.110000000000001, proxy=pythonCalculator1)

# set active source
SetActiveSource(warpByVector1)

# create a new 'Resample With Dataset'
resampleWithDataset1 = ResampleWithDataset(registrationName='ResampleWithDataset1', SourceDataArrays=displacement_spherexdmf,
    DestinationMesh=warpByVector1)
resampleWithDataset1.CellLocator = 'Static Cell Locator'

UpdatePipeline(time=1.110000000000001, proxy=resampleWithDataset1)

# create a new 'Warp By Vector'
warpByVector2 = WarpByVector(registrationName='WarpByVector2', Input=resampleWithDataset1)
warpByVector2.Vectors = ['POINTS', 'Displacement']

UpdatePipeline(time=1.110000000000001, proxy=warpByVector2)

# create a new 'Extract Surface'
extractSurface2 = ExtractSurface(registrationName='ExtractSurface2', Input=warpByVector2)

UpdatePipeline(time=1.110000000000001, proxy=extractSurface2)

# create a new 'Clip'
clip2_1 = Clip(registrationName='Clip2', Input=extractSurface2)
clip2_1.ClipType = 'Plane'
clip2_1.HyperTreeGridClipper = 'Plane'
clip2_1.Scalars = ['POINTS', 'vtkValidPointMask']
clip2_1.Value = 0.5

# init the 'Plane' selected for 'ClipType'
clip2_1.ClipType.Origin = [0.0802716501057148, 0.12863695621490479, 0.06046945974230766]

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip2_1.HyperTreeGridClipper.Origin = [0.0802716501057148, 0.12863695621490479, 0.06046945974230766]

# rename source object
RenameSource('Clip_dome2', clip2_1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip2_1.ClipType)

# Properties modified on clip2_1
clip2_1.ClipType = 'Sphere'

UpdatePipeline(time=1.110000000000001, proxy=clip2_1)

# set active source
SetActiveSource(extractSurface2)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip2_1.ClipType)

# create a new 'Slice'
slice2 = Slice(registrationName='Slice2', Input=extractSurface2)
slice2.SliceType = 'Plane'
slice2.HyperTreeGridSlicer = 'Plane'
slice2.SliceOffsetValues = [0.0]
slice2.PointMergeMethod = 'Uniform Binning'

# init the 'Plane' selected for 'SliceType'
slice2.SliceType.Origin = [0.0802716501057148, 0.12863695621490479, 0.06046945974230766]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice2.HyperTreeGridSlicer.Origin = [0.0802716501057148, 0.12863695621490479, 0.06046945974230766]

UpdatePipeline(time=1.110000000000001, proxy=slice2)

# create a new 'Clip'
clip2_2 = Clip(registrationName='Clip2', Input=slice2)
clip2_2.ClipType = 'Plane'
clip2_2.HyperTreeGridClipper = 'Plane'
clip2_2.Scalars = ['POINTS', 'vtkValidPointMask']
clip2_2.Value = 1.0

# init the 'Plane' selected for 'ClipType'
clip2_2.ClipType.Origin = [0.0802716463804245, 0.13012881577014923, 0.060179637745022774]

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip2_2.HyperTreeGridClipper.Origin = [0.0802716463804245, 0.13012881577014923, 0.060179637745022774]

UpdatePipeline(time=1.110000000000001, proxy=clip2_2)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip2_2.ClipType)

# set active source
SetActiveSource(warpByVector2)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip2_2.ClipType)

# create a new 'Clip'
clip3 = Clip(registrationName='Clip3', Input=warpByVector2)
clip3.ClipType = 'Plane'
clip3.HyperTreeGridClipper = 'Plane'
clip3.Scalars = ['POINTS', 'vtkValidPointMask']
clip3.Value = 0.5

# init the 'Plane' selected for 'ClipType'
clip3.ClipType.Origin = [0.0802716501057148, 0.12863695621490479, 0.06046945974230766]

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip3.HyperTreeGridClipper.Origin = [0.0802716501057148, 0.12863695621490479, 0.06046945974230766]

# rename source object
RenameSource('Clip_sph2', clip3)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip3.ClipType)

# Properties modified on clip2_2
clip2_2.ClipType = 'Sphere'

# Properties modified on clip3
clip3.ClipType = 'Sphere'

UpdatePipeline(time=1.110000000000001, proxy=clip3)

# create a new 'Cell Size'
cellSize2 = CellSize(registrationName='CellSize2', Input=clip3)

UpdatePipeline(time=1.110000000000001, proxy=cellSize2)

# create a new 'Python Calculator'
pythonCalculator2 = PythonCalculator(registrationName='PythonCalculator2', Input=cellSize2)
pythonCalculator2.Expression = ''

# Properties modified on pythonCalculator2
pythonCalculator2.Expression = 'sum(abs(Volume))'
pythonCalculator2.ArrayAssociation = 'Cell Data'

UpdatePipeline(time=1.110000000000001, proxy=pythonCalculator2)