import ezdxf
import os
import sys

this = sys.argv[0]
filename = sys.argv[1]

# these are the colors have I been getting from the USGS maps. YMMV
color_dict = { 1 : 'red',
               2 : 'yellow',
               3 : 'green',
               4 : 'light_blue',
               5 : 'dark_blue',
               6 : '6',
               7 : 'white',
               8 : '8'
             }

INSUNITS = { 0 : 'Unitless',            1 : 'Inches',       2 : 'Feet',
             3 : 'Miles',               4 : 'Millimeters',  5 : 'Centimeters',
             6 : 'Meters',              7 : 'Kilometers',   8 : 'Microinches',
             9 : 'Mils',                10 : 'Yards',       11 : 'Angstroms',
             12 : 'Nanometers',         13 : 'Microns',     14 : 'Decimeters',
             15 : 'Decameters',         16 : 'Hectometers', 17 : 'Gigameters',
             18 : 'Astronomical units', 19 : 'Light years', 20 : 'Parsecs' }

def  get_header_attribute(drawing, name):
    try:
        attrib = drawing.header[name]
    except:
        attrib = None
    #print str(name) + " : " + str(attrib)
    return attrib

def main():
    print "Opening file '" + filename + "'..."
    dwg = ezdxf.readfile(filename)
    print "\t... read complete.\n"

    # Check $INSUNITS - Default drawing units for AutoCAD DesignCenter blocks
    units = get_header_attribute(dwg, '$INSUNITS')
    print "Units set to '" + INSUNITS[units] + "'"

    # count objects/colors/existing layers
    objects = 0
    colors = []
    layers = []

    modelspace = dwg.modelspace()
    for e in modelspace:
        objects += 1

        if (e.dxf.color in colors): pass
        else:   colors.append(e.dxf.color)

        if (e.dxf.layer in layers): pass
        else:   layers.append(e.dxf.layer)

    print "Found \t" + str(objects) + " objects, " + str(len(colors)) + " color(s), " + \
          str(len(layers)) + " layer(s).\n"

    print "Adding new layers..."
    for newLayer in colors:
        dwg.layers.new(str(newLayer), dxfattribs=None)

    print "Updated drawing layer count : " + str(dwg.layers.__len__())

    print "Reassigning objects to their new 'color' layer..."
    for e in modelspace:
        e.dxf.layer = str(e.dxf.color)

    filename_out = os.path.splitext(filename)[0] + "_layered" + os.path.splitext(filename)[1]
    print "Saving to file '" + filename_out + "'"
    dwg.saveas(filename_out)

if os.path.isfile(filename):
    main()
else:
    print "ERROR :: File not found."