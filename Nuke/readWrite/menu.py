import nuke
import readWrite

nuke.menu("Nuke").addCommand("pyVid Utils/Read from write", "readWrite.createReadFromWrite()", "alt+r")