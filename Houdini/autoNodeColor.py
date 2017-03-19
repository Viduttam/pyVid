"""Function to Auto color nodes in Houdini based on a user defined color dictionary"""
__author__ = "Mattudiv"

import time
def autoNodeColor():

    node_dict = {"light":(1,1,0), "geo":(0.8,0.8,0.8), "cam":(0.36,0.36,0.36), 
                        "null":(0,0,0),"geometryvopglobal::2.0":(1,0,0),"output":(0,0,1), 
                        "dopnet":(1,0,0), "import": (1,0.2,0.2), "cache":(0,0.5,1),
                        "vop":(0.4,1,0.4), "wrangle":(0.4,1,0.4),
                        "xform":(0,0.4,0),"alembic":(1,1,1),"shopnet":(0.6,0.4,0.2)}


    all_nodes = hou.node("/obj").allSubChildren(top_down=True)

    for node in all_nodes:
        node_type = node.type().name()



        for k,v in node_dict.items():
                if(node_type.find(k) != -1):
                        node.setColor(hou.Color(v))
start = time.time()
autoNodeColor()
print("Total time = %s secs" %round((time.time() - start),4))