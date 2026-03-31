# Super Rigid Skin Tool - Helps with rigid skinning by apply uniform skin weights to selected vertices

import maya.cmds as mc

# - Buttons functions
def buttons(n):
    global vtxsSel, jntSel
    # Convert any selection type to vertices
    if n == 1:
        newSel = mc.polyListComponentConversion(tv=True)
        mc.select(newSel)
    
    # Store point selection
    if n == 2:
        validSel = True
        vtxsSel = mc.ls(sl=True)
        print( vtxsSel )
        # Check if selection is only vertices
        for vtxSel in vtxsSel:
            if( vtxSel.find("vtx") == -1 ):
                validSel = False
        # Save selection and clear selection
        if validSel:
            mc.select(clear=True)
            mc.button(bVS, e=1, bgc=(0,1,0))
            print('Points selected !')
        else:
            mc.warning( "Selection is not valid, please select only vertices, or use 'Convert Selection to Vertices' first." )
    
    # Store joint selection
    if n == 3:
        selection = mc.ls(sl=True)
        jntSel = selection[0]
        # Check if selection is only joint
        if( mc.objectType( jntSel) == "joint" ):
            # Check if lockInfluenceWeights attribute exist ( if not the joint is not binded )
            if( mc.attributeQuery( 'liw', n=jntSel, ex=True ) ):
                # Check if the joint skin weights are locked
                if ( mc.getAttr( jntSel + '.liw' ) == 1 ):
                    mc.warning( "The joint '" + jntSel + "' is locked, please unlock first." )
                # Else save selection and clear selection
                else:
                    mc.select(clear=True)
                    mc.button(bJS, e=1, bgc=(0,1,0))
                    print('Joints selected !')
            # Else the joint need to be added
            else:
                mc.warning( "The joint '" + jntSel + "' might not be binded to the skin cluster, try to 'Add Influence'." )
    
    # Unlock joints
    if n == 4:
        for node in mc.ls(sl=True):
            mc.setAttr((node + '.liw'), 0)
    
    #Button idea add influence :
    #mc.skinCluster( "skinClusterName", edit=True, ai='jointName')

# - Main function : set vertexs skin paint weights per joint
def ApplySkin():
    #Get paint weight field value
    val = mc.floatField(fFPV, q=1, v=1)
    for vtxSel in vtxsSel:
        list = cmds.listConnections(jntSel)
        sCluster = None
        for node in list:
            if mc.objectType(node) == 'skinCluster':
                sCluster = node
        if ( sCluster ):
            # Check and auto set the skin cluster normalizeWeights attribute to Interactive
            if ( mc.getAttr(sCluster + ".normalizeWeights") != 1 ):
                mc.setAttr( (sCluster + ".normalizeWeights"), 1)
                mc.warning( "The attribute 'Normalize Weights' of the Skin Cluster '" + sCluster + "' have been set to 'Interactive'" )
            # Finally apply the paint weight to vertices
            mc.skinPercent(str(sCluster), str(vtxSel), tv=[str(jntSel), val])
        # If not cluster, the joint need to be added
        else:
            mc.warning( "The joint '" + jntSel + "' might not binded to the skin cluster, try to 'Add Influence'." )
    #Reset selection buttons color feedback
    mc.button(bVS, e=1, bgc=(0.35,0.35,0.35))
    mc.button(bJS, e=1, bgc=(0.35,0.35,0.35))

# - Tool user interface
def SuperRigidSkinWin():
    global fFPV, bVS, bJS
    global vtxsSel, jntSel
    vtxsSel = jntSel = ""
    # Width and annotations
    fw = 250
    aTitle = 'Helps with rigid skinning by apply uniform skin weights to selected vertices'
    aCSV = 'Convert any selection type to vertices'
    aGVS = 'Save vertex selection '
    aUJ = 'Unlock selected joints weights'
    aGJS = 'Save joint selection'
    aPV = 'Skin weight value'
    aAS = 'Apply saved joints weight to saved vertices'
    # Delete existing window and create new
    if (mc.window('SuperRigidSkinWin', exists=True)):
        mc.deleteUI('SuperRigidSkinWin')
    SuperRigidSkinWin = mc.window('SuperRigidSkinWin', t=' ', s=0, rtf=1)
    # Layout
    colL = mc.columnLayout()
    mc.separator(style='in',w=fw, h=8, p=colL)
    mc.text(l='Super Rigid Skin Tool', fn='fixedWidthFont', w=fw, al='center', ann=aTitle, p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    # Convert Selection
    bVS = mc.button( l='Convert Selection to Vertices', w=(fw), bgc=(0.35,0.35,0.35), c=('buttons(1)'), ann=aCSV, p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    # Save Vertices
    bVS = mc.button( l='Get Vertex Selection', h = 40, w=(fw), bgc=(0.35,0.35,0.35), c=('buttons(2)'), ann=aGVS, p=colL )
    mc.separator(style='in',w=fw, h=8, p=colL)
    #Unlock Joints
    buttonunlock = mc.button( l='Unlock joints', w=(fw), bgc=(0.35,0.35,0.35), c=('buttons(4)'), ann=aUJ, p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    # Save Joint
    bJS = mc.button( l='Get Joint Selection ', h = 40, w=(fw), bgc=(0.35,0.35,0.35), c=('buttons(3)'), ann=aGJS, p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    rowL = mc.rowLayout(nc=2, p=colL)
    # Paint Value
    mc.text(l='Paint Value', w=(fw/3-1), al='center', ann=aPV, p=rowL)
    fFPV = mc.floatField(v=1, w=((2*fw)/3-1), h=32, ann=aPV, p=rowL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    # Apply skin
    mc.button(l='Apply skin', h = 40, w=(fw), c=('ApplySkin()'), ann=aAS, p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    mc.text(l='Open Source Tool by Anthony CHALLAMEL', h=12, fn='smallObliqueLabelFont', w=fw, al='center', ann='Feel free to contact me on LinkedIn !', p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    mc.showWindow(SuperRigidSkinWin)

SuperRigidSkinWin()