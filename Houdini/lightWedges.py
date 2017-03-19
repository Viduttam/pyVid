def fetch_user_data():
    input_labels = ("Number of slices/wedges (Either 3 or 5)", "Range of rotation (in degrees)?", "Change in Sun elevation (in degrees)", "Frame number to start keyframing")
    user_input = hou.ui.readMultiInput("Please enter the below data", input_labels, buttons=('OK','Cancel'),title = "Vikings light Wedges")

    if(user_input[0]==1):
        return
    elif(user_input[1][0]=="3" or user_input[1][0]=="5"):
        set_light_wedges(user_input)
    else:
        error_input = hou.ui.displayMessage("Number of slices/wedges entered is not 3 or 5\n Please re-enter data correctly", buttons=('OK','Cancel'),title="User Input Error")
        if(error_input == 0):
            fetch_user_data()
        else:
            return



def set_light_wedges(user_input):
    from time import time
    start = time()
    # If user clicks 'OK' execute code else return none

    slices = int(user_input[1][0])
    print("Slices => %s \n"%slices)

    rotRange = float (user_input[1][1])
    print("rotRange => %s \n"%rotRange)

    elevChange = float(user_input[1][2])
    print("elevChange => %s \n"%elevChange)

    userFrame = int(user_input[1][3])-1
    print("userFrame => %s \n" %(userFrame+1))

    #Python code to create slices of rotations for a given HDR and sun pair by Vkatkar
    obj_context = hou.node('obj').children()
    for child in obj_context:

        name = child.name()
        type_name = child.type().name()

        if type_name.find("envlight") != -1:
            hdrNode = child
        if type_name.find("hlight") != -1:
            sunNode = child

    print ("\nHDR node => %s" %hdrNode)
    print ("\nSun node => %s" %sunNode)



    hdrRotParm = hdrNode.parm("ry")

    #Not working for Houdini 14 and below
    #checks if current houdini version is 14 or 15 and accordingly calls the corresponding parameters
    # this is because the light object is different in Houdini versions 14 and 15
    #if hou.expandString("$HFS").find("15") == -1:
    #    sunRotParm = [sunNode.parm("l_rx"),sunNode.parm("l_ry"),sunNode.parm("l_rz")]
    #else:
    sunRotParm = [sunNode.parm("rx"),sunNode.parm("ry"),sunNode.parm("rz")]


    """
    user_input_1 = hou.ui.readInput("Enter number of slices? (Enter either 3 or 5)")
    slices = int(user_input_1[1])
    print slices

    user_input_2 = hou.ui.readInput("Enter range of rotation (in degrees)?")
    rotRange = float(user_input_2[1])
    print rotRange


    user_input_3 = hou.ui.readInput("Enter change in elevation (in degrees)?")
    elevChange = float(user_input_3[1])
    print elevChange

    #userFrame is basically a frame offset which is added to the bottom frame logic
    user_input_4 = hou.ui.readInput("Enter frame number to start keyframing?")
    userFrame = int(user_input_4[1])-1
    print userFrame
    """

    increment = rotRange/(slices-1) # calculate increment

    if slices == 5:
            midFrame = (slices - 2) + userFrame
    elif slices == 3:
            midFrame = (slices - 1) + userFrame

    initAzimuth = hdrRotParm.eval()
    initElevation = sunRotParm[0].eval()

    #print initAzimuth, initElevation
    #print "Hello World"
    #print hdrRotParm, sunRotParm[0]


    #set last keyframe with initial elevation value
    currentFrame = slices + userFrame
    key = hou.Keyframe()
    key.setFrame(currentFrame)
    key.setValue(initElevation)
    sunRot = sunRotParm[0]
    #print sunRot
    sunRot.setKeyframe(key)

    # set middle value keyframe for azimuthal rotation
    currentFrame = midFrame
    key = hou.Keyframe()
    key.setFrame(currentFrame)
    key.setValue(initAzimuth)
    hdrRotParm.setKeyframe(key)

    #slices -= 1 # As frame numbers begin from 1 while counting starts from 0

    # set remaining keyframes for azimuthal rotation
    timeline = list(range(userFrame+1,userFrame + (slices+1)))

    for frame in timeline:
            if (frame) < midFrame:
                currentFrame = frame
                newAzimuth = initAzimuth - ((midFrame-frame)*increment)
                key = hou.Keyframe()
                key.setFrame(currentFrame)
                key.setValue(newAzimuth)
                hdrRotParm.setKeyframe(key)

            if (frame) > midFrame:
                currentFrame = frame
                newAzimuth = initAzimuth + ((frame-midFrame)*increment)
                key = hou.Keyframe()
                key.setFrame(currentFrame)
                key.setValue(newAzimuth)
                hdrRotParm.setKeyframe(key)


    #set last+1 keframe with the elevation change
    currentFrame = slices + 1 + userFrame
    key = hou.Keyframe()
    key.setFrame(currentFrame)
    key.setValue(initElevation + elevChange)
    sunRot = sunRotParm[0]
    #print sunRot
    sunRot.setKeyframe(key)


    midFrame = midFrame + slices # shift midFrame by 5 for the new set of azimuthal changes for the new elevation change

    # set middle value keyframe for azimuthal rotation
    currentFrame = midFrame
    key = hou.Keyframe()
    key.setFrame(currentFrame)
    key.setValue(initAzimuth)
    hdrRotParm.setKeyframe(key)


    nextTimeline = list(range((slices+1) + userFrame,slices+(slices+1) + userFrame))

    for frame in nextTimeline:
            if (frame) < midFrame:
                currentFrame = frame
                newAzimuth = initAzimuth - ((midFrame-frame)*increment)
                key = hou.Keyframe()
                key.setFrame(currentFrame)
                key.setValue(newAzimuth)
                hdrRotParm.setKeyframe(key)

            if (frame) > midFrame:
                currentFrame = frame
                newAzimuth = initAzimuth + ((frame-midFrame)*increment)
                key = hou.Keyframe()
                key.setFrame(currentFrame)
                key.setValue(newAzimuth)
                hdrRotParm.setKeyframe(key)

    print("Total time = %s secs" %(round(time() - start,6)))

#Main execution

fetch_user_data()