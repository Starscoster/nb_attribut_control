Type of attribute	Flag and argument to use
boolean	-at bool
32 bit integer	-at long
16 bit integer	-at short
8 bit integer	-at byte
char	-at char
enum	-at enum (specify the enum names using the enumName flag)
float	-at "float" (use quotes since float is a mel keyword)
double	-at double
angle value	-at doubleAngle
linear value	-at doubleLinear
string	-dt "string" (use quotes since string is a mel keyword)
array of strings	-dt stringArray
compound	-at compound
message (no data)	-at message
time	-at time
4x4 double matrix	-dt "matrix" (use quotes since matrix is a mel keyword)
4x4 float matrix	-at fltMatrix
reflectance	-dt reflectanceRGB
reflectance (compound)	-at reflectance
spectrum	-dt spectrumRGB
spectrum (compound)	-at spectrum
2 floats	-dt float2
2 floats (compound)	-at float2
3 floats	-dt float3
3 floats (compound)	-at float3
2 doubles	-dt double2
2 doubles (compound)	-at double2
3 doubles	-dt double3
3 doubles (compound)	-at double3
2 32-bit integers	-dt long2
2 32-bit integers (compound)	-at long2
3 32-bit integers	-dt long3
3 32-bit integers (compound)	-at long3
2 16-bit integers	-dt short2
2 16-bit integers (compound)	-at short2
3 16-bit integers	-dt short3
3 16-bit integers (compound)	-at short3
array of doubles	-dt doubleArray
array of floats	-dt floatArray
array of 32-bit ints	-dt Int32Array
array of vectors	-dt vectorArray
nurbs curve	-dt nurbsCurve
nurbs surface	-dt nurbsSurface
polygonal mesh	-dt mesh
lattice	-dt lattice
array of double 4D points	-dt pointArray