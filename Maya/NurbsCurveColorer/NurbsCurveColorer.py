# Nurbs Curves Colorer Tool - Easily add color to rig controllers, also work for mesh wireframe

import maya.cmds as mc

# Get shapes from selection
def selectedShapesProc():
    nodes = []
    selected = mc.ls(sl=True)
    for sel in selected :
        if mc.nodeType(sel) == 'transform':
            children = mc.listRelatives(sel, s=1, f=1)
            for child in children :
                nodes.append(child)
        else :
            nodes.append(sel)
    return nodes

# Check if attribute have connections : if so dialogue to confirm auto disconnect
def unlockAndCheckConnections(attr):
    mc.setAttr(attr, l=0)
    connections = mc.listConnections(attr, d=True, p=1)
    if connections:
        result = mc.confirmDialog(  title='Break Connections',
                                    message='The attribute "{}" of node "{}" has connections. Do you want to break them?'.format(attr.split('.')[1],attr.split('.')[0]),
                                    button=['Yes', 'No'],
                                    defaultButton='Yes',
                                    cancelButton='No',
                                    dismissString='No')
        if result == 'Yes':
                mc.disconnectAttr(connections[0], attr)
                return True
        else:
            return False
    return True

# Main change color def : set color override attributes
def changeColorProc(value) :
    nodes = selectedShapesProc()
    for node in nodes :
        # 'Enable Overrides' attribute
        if unlockAndCheckConnections((str(node)+'.overrideEnabled')):
            mc.setAttr((str(node)+'.overrideEnabled'), 1)
            if type(value) == int :
                if value == 0 :
                    mc.setAttr((str(node)+'.overrideEnabled'), 0)
        # Override color attributes
        if unlockAndCheckConnections((str(node)+'.overrideRGBColors')):
            if type(value) == int :
                mc.setAttr((str(node)+'.overrideRGBColors'), 0)
                if unlockAndCheckConnections((str(node)+'.overrideColor')):
                    mc.setAttr((str(node)+'.overrideColor'), (max(int(value)-1,0)))
            else :
                mc.setAttr((str(node)+'.overrideRGBColors'), 1)
                if unlockAndCheckConnections((str(node)+'.overrideColorRGB')):
                    if unlockAndCheckConnections((str(node)+'.overrideColorR')):
                        mc.setAttr((str(node)+'.overrideColorR'), value[0])
                    if unlockAndCheckConnections((str(node)+'.overrideColorG')):
                        mc.setAttr((str(node)+'.overrideColorG'), value[1])
                    if unlockAndCheckConnections((str(node)+'.overrideColorB')):
                        mc.setAttr((str(node)+'.overrideColorB'), value[2])

# On Index color slider change
def setColorIndexProc():
    global colorType
    colorType = 1
    changeColorProc(mc.colorIndexSliderGrp('cISG', q=1, v=1))

# On RGB color picker change
def setColorRGBProc():
    global colorType
    colorType = 2
    changeColorProc(mc.colorSliderGrp('cSG', q=1, rgb=1))

# On favorite color clicked
def setColorFavProc(bfav):
    colorType = 3
    saved = mc.optionVar( q='NCC_Fav'+str(bfav) )
    changeColorProc( eval(saved) )

# Clear Color : reset color override attributes
def resetColorProc():
    changeColorProc(0)

# On add favorite [+] button cliked : add favorite color from last color change
def changeColorFav(fcvalue):
    if(colorType == 1):
        cI = int(mc.colorIndexSliderGrp('cISG', query=True, value=True))-1
        cRGB = mc.colorIndex(cI, query=True)
        mc.button(('Fav_' + str(fcvalue)), edit=True, bgc=[cRGB[0],cRGB[1],cRGB[2]])
    if(colorType == 2):
        cRGB = mc.colorSliderGrp('cSG', query=True, rgb=True)
        mc.button(('Fav_' + str(fcvalue)), edit=True, bgc=[cRGB[0],cRGB[1],cRGB[2]])
    if(colorType != 0):
        mc.button(('Fav_' + str(fcvalue)), edit=True, en=1)
        mc.optionVar( sv=('NCC_Fav'+str(fcvalue), str( cRGB ) ) )
    else:
        mc.error('Can`t add Favorite : Select a color first')

#On reset favorite [-] button cliked : remove favorite color
def removeFav( nFav ):
    bcommand = ('changeColorFav(' + str(nFav) + ')')
    mc.button(('Fav_' + str(nFav)), edit=True, l=' ', bgc=[0.3,0.3,0.3], en=0, c=bcommand)
    mc.optionVar( remove='NCC_Fav'+str(nFav) )

#On reset favorites button cliked : remove all favorites
def removeFavotites():
    for val in range(1, 10):
        removeFav( val )

# Main function : Init and Create Window
def nurbsColorer():
    global colorType, favmat
    colorType = 0
    # Width and annotations
    fw = 520
    aCISG = 'Slide the slider to change value'
    aCSG = 'Click on the box to edit color'
    aBCC = 'Click to rest color to default'
    aBF = 'Click to use this color'
    aBFP = 'Click to add last color as favorite'
    aBFM = 'Click to remove this favorite'
    aBFR = 'Click to remove all favorite colors'
    # Delete existing window and create new
    if (mc.window('colorWin', exists=True)):
        mc.deleteUI('colorWin')
    colorWin = mc.window('colorWin', t=' ', s=0, rtf=1)
    # Layout
    colL = mc.columnLayout()
    mc.separator(style='in',w=fw, h=8, p=colL)
    mc.text(l='Nurbs Curves Colorer Tool', fn='fixedWidthFont', w=fw, al='center', p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    # Color slider and color box
    mc.colorIndexSliderGrp('cISG', l='Index Color : ', min=2, max=31, v=2, h=30, w=(int(fw)-50), cc='setColorIndexProc()', ann=aCISG, p=colL)
    mc.colorSliderGrp('cSG', l='RGB Color : ', rgb=[1,1,1], h=30, w=230, cc='setColorRGBProc()', ann=aCSG, p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    # Favorites : load optionVar saved favorite colors
    rowL1 = mc.rowLayout(nc=10, p=colL)
    rowL2 = mc.rowLayout(nc=20, p=colL)
    # Loop create all buttons > assign commands with button index
    for val in range(1, 11):
        bName = 'Fav_' + str(val)
        bCommand = ('setColorFavProc('+str(val)+')')
        saved = mc.optionVar( q='NCC_Fav'+str(val) )
        # Favorite button
        if ( saved != 0 ):
            mc.button(bName, l=' ',w=50, h=50, bgc=eval(saved), en=1, c=bCommand, p=rowL1)
        else:
            mc.button(bName, l=' ',w=50, h=50, bgc=[0.3,0.3,0.3], en=0, c=bCommand, ann=aBF, p=rowL1)
        # Add favorite button
        bCommand = ('changeColorFav('+str(val)+')')
        mc.button(bName+'+', l='+',w=24, h=15, c=bCommand, ann=aBFP, p=rowL2)
        # Remove favorite button
        bCommand = ('removeFav('+str(val)+')')
        mc.button(bName+'-', l='-',w=24, h=15, c=bCommand, ann=aBFM, p=rowL2,)
    # Remove all favorites and Reset color buttons
    mc.separator(style='in',w=fw, h=8, p=colL)
    rowL3 = mc.rowLayout(nc=2, p=colL)
    mc.button(l='Remove All Favorites', w=(fw/2-1), c='removeFavotites()', ann=aBFR, p=rowL3)
    mc.button(l='Clear color', w=(fw/2-1), c='resetColorProc()', ann=aBCC, p=rowL3)
    mc.separator(style='in',w=fw, h=8, p=colL)
    mc.text(l='Open Source Tool by Anthony CHALLAMEL', h=12, fn='smallObliqueLabelFont', w=fw, al='center', ann='Feel free to contact me on LinkedIn !', p=colL)
    mc.separator(style='in',w=fw, h=8, p=colL)
    # Show the window
    mc.showWindow(colorWin)

nurbsColorer()