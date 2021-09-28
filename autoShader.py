import maya.cmds as cmds


'''
Option linearize ou pas
Procedural
PxrT_DUVAL_Spec
Auto blender
lookdev base scene qui peut se scale

udim = asset.1001

pxrT + remap pour mask

entre hair et marschner, mettre hsl avant TT
add id_XP
'''


####################
## USER INTERFACE ##
####################

class mainWindow():
    

    
    
    def __init__(self):

        
        
        #window
        if (cmds.window("mainWindow", q=1, exists=True)):
            cmds.deleteUI("mainWindow")
            
        self.baseWindow = cmds.window("mainWindow", title="OCTOPUS_v0.1", w= 300, h= 200, sizeable=True, bgc = [0.1, 0.2, 0.3 ])
        
        #LAYERS HIERARCHY ###############################################################
        self.root = cmds.formLayout()
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout( self.root, edit=True, attachForm=((self.tabs, 'top', 0), (self.tabs, 'left', 0), (self.tabs, 'bottom', 0), (self.tabs, 'right', 0)) )
        
        
        #self.root = cmds.frameLayout("root")  
        self.tabBase01 = cmds.frameLayout("SHADING", p= self.tabs)
        self.asset = cmds.rowColumnLayout(numberOfColumns = 2, w=200, p= self.tabBase01)  
        #material
        self.rootMat = cmds.columnLayout("asset", p=self.tabBase01, adjustableColumn=True)
        self.mat = cmds.rowColumnLayout(numberOfColumns = 3, p= self.tabBase01)
        self.mat4 = cmds.rowColumnLayout(numberOfColumns = 4, p= self.tabBase01)
        #param
        self.rootParam = cmds.columnLayout("param", p=self.tabBase01, adjustableColumn=True)
        self.param = cmds.rowColumnLayout(numberOfColumns = 2, p= self.tabBase01)
        #disp
        self.rootDisp = cmds.columnLayout("disp", p=self.tabBase01, adjustableColumn=True)
        self.disp = cmds.rowColumnLayout(numberOfColumns = 2, p= self.tabBase01)
        #buttons
        self.buttons = cmds.columnLayout("buttons", p=self.tabBase01, adjustableColumn=True)
        
        
        
        self.tabBase02 = cmds.frameLayout("LOOKDEV", p= self.tabs)
        

        


        #ASSIGN BUTTONS ################################################################
        
        #choose asset
        cmds.setParent(self.asset)
        cmds.text(label = "Enter Asset Name", w=100)
        self.assetName = cmds.textField(w=200)
        
        #choose material
        cmds.setParent(self.rootMat)
        cmds.separator(height = 10, style = "in")
        cmds.text(label = "MATERIAL")
        
        cmds.setParent(self.mat)
        self.pxrS = cmds.checkBox( label = "PxrSurface", align="center")
        self.pxrLS = cmds.checkBox( label = "PxrLayerSurface", align="center")
        self.marschner = cmds.checkBox( label = "PxrMarschnerHair", align="center")
        
        cmds.setParent(self.mat4)
        self.layer1 = cmds.checkBox( label = "BL + Layer 1", align="center")
        self.layer2 = cmds.checkBox( label = "+ Layer 2", align="center")
        self.layer3 = cmds.checkBox( label = "+ Layer 3", align="center")
        self.layer4 = cmds.checkBox( label = "+ Layer 4", align="center")
        
        #choose param
        cmds.setParent(self.rootParam)
        cmds.separator(height = 10, style = "in")
        cmds.text(label = "PARAMETERS")
        
        cmds.setParent(self.param)
        self.diff = cmds.checkBox( label = "Diffuse", align="center")
        self.sss = cmds.checkBox( label = "SSS", align="center")
        self.spec = cmds.checkBox( label = "Specular EdgeColor", align="center")
        self.specRough = cmds.checkBox( label = "Specular Roughness", align="center")
        self.roughSpec = cmds.checkBox( label = "RoughSpecular EdgeColor", align="center")
        self.roughSpecRough = cmds.checkBox( label = "RoughSpecular Roughness", align="center")
        self.bump = cmds.checkBox( label = "Bump", align="center")
        self.normal = cmds.checkBox( label = "Normal", align="center")
        
        #choose disp
        cmds.setParent(self.rootDisp)
        cmds.separator(height = 10, style = "in")
        cmds.text(label = "DISPLACEMENT")
        
        cmds.setParent(self.disp)
        self.scalar = cmds.checkBox( label = "Scalar", align="center")
        self.vector = cmds.checkBox( label = "Vector", align="center")
        
        #pushButtons
        cmds.setParent(self.buttons)
        cmds.text(label = "    ")
        self.create = cmds.button( label = "CREATE AND ASSIGN SHADER", bgc = [0.0, 0.5, 0.5 ], c = self.autoShade )
        #self.reload = cmds.button( label = "RELOAD", bgc = [0.0, 0.5, 0.5 ])
        cmds.text(label = "    ")
        
        
       
        cmds.showWindow(self.baseWindow)
       
       
       
       
       
       
       
       
        
        
    #################    
    ## DEFINITIONS ##
    #################    
        
    def autoShade(self, pxrS):
        
        #NOMENCLATURE DES NODES
        
        pxrSurface = "PxrS_"
        pxrLayerSurface = "PxrLS_"
        PxrLayerMixer = "PxrLM_"
        PxrBaseLayer = "BL_"
        PxrLayer1 = "PxrL_01_"
        PxrTexture = "PxrT_"
        PxrHSL = "PxrHSL_"
        PxrRemap = "PxrRmp_"
        PxrBump = "PxrBump_"
        PxrAdjustNormal = "PxrAdjustNormal_"
        PxrNormal = "PxrNormal_"
        PxrDisplace = "PxrDisp_"
        PxrDispTransform = "PxrDispTransform_"
        
        shadingGroup = "_SG"
        diffuse = "_Diff"
        sss = "_SSS"
        spec = "_Spec"
        specRough = "_SpecRough"
        roughSpec = "_roughSpec"
        roughSpecRough = "_roughSpecRough"
        bump = "_bmp"
        normal = "_norm"
        
        #NOM DU SHADER
        assetName = cmds.textField(self.assetName, q=1, tx=1)
        print ( assetName )
        
        #Create Lambert
        lamb = cmds.shadingNode("lambert",asShader=True, n= "lambert" + assetName)
        
        #Create pxrSurface ####################################################################################
        #######################################################################################################
        if cmds.objExists(pxrSurface + assetName):
            print ("PxrSurface already exists")
          
        else :
            if cmds.checkBox(self.pxrS, q=1, v=1):
                print ("create pxrSurface")
                #create nodes
                shaderS = cmds.shadingNode("PxrSurface",asShader=True, n= pxrSurface + assetName)
                shading_group = cmds.sets(renderable=True,noSurfaceShader=True,empty=True, n= pxrSurface + assetName + shadingGroup)
                #connect attr
                cmds.connectAttr("%s.outColor" %shaderS ,"%s.rman__surface" %shading_group)
                cmds.connectAttr("%s.outColor" %lamb ,"%s.surfaceShader" %shading_group)
            
            
        if cmds.objExists(pxrLayerSurface + assetName):
            print ("PxrLayerSurface already exists")
            #Create pxrLayerSurface ################################################################################
            ########################################################################################################
        else:
            if cmds.checkBox(self.pxrLS, q=1, v=1):
                print ("create pxrLayerSurface")
                #create nodes
                shaderLS = cmds.shadingNode("PxrLayerSurface",asShader=True, n= pxrLayerSurface + assetName)
                shading_group = cmds.sets(renderable=True,noSurfaceShader=True,empty=True, n= pxrLayerSurface + assetName + shadingGroup)
                
                BL = cmds.shadingNode("PxrLayer", asTexture=True, n= PxrBaseLayer + assetName)
                #connect attr
                cmds.connectAttr("%s.outColor" %shaderLS ,"%s.rman__surface" %shading_group)
                cmds.connectAttr("%s.outColor" %lamb ,"%s.surfaceShader" %shading_group)
                
                
                #LAYER MIXER
                if cmds.objExists(PxrLayerMixer + assetName):
                    print ("PxrLayerMixer already exists")
                
                else:
                    layerMixer = cmds.shadingNode("PxrLayerMixer",asTexture=True, n= PxrLayerMixer + assetName)
                    cmds.connectAttr("%s.pxrMaterialOut" %layerMixer , pxrLayerSurface + assetName + ".inputMaterial" )
                    cmds.connectAttr("%s.pxrMaterialOut" %BL ,"%s.baselayer" %layerMixer)
                    #set attr
                    cmds.setAttr(layerMixer + ".layer1Enabled", 0)
            
        #LAYER 1
        if cmds.objExists(PxrLayer1 + assetName):
            print ("layer 1 already exists")
                
        else:
            if cmds.checkBox(self.layer1, q=1, v=1):
                layer1 = cmds.shadingNode("PxrLayer", asTexture=True, n= PxrLayer1 + assetName)
                cmds.connectAttr("%s.pxrMaterialOut" %layer1 , PxrLayerMixer + assetName + ".layer1")
                print ("Create PxrLayer 1")
            
            
        
        
        
        
        #DIFFUSE    ##############################################################
        if cmds.objExists(PxrTexture + assetName + diffuse):
            print ("Diffuse already on BaseLayer")
            
                
        else :
            if cmds.checkBox(self.diff, q=1, v=1):
                #create nodes for pxrSurface or BaseLayer
                tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName + diffuse )
                hsl = cmds.shadingNode("PxrHSL",asTexture=True, n= PxrHSL + assetName + diffuse )
                #connect attr pxrSurface or BaseLayer
                cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %hsl)
                #pxrSurface
                if cmds.checkBox(self.pxrS, q=1, v=1):
                    cmds.connectAttr("%s.resultRGB" %hsl ,"%s.diffuseColor" %shaderS)
                    cmds.setAttr(shaderS + ".diffuseGain", 1)
                #BaseLayer
                elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                    cmds.connectAttr("%s.resultRGB" %hsl ,"%s.diffuseColor" %BL)
                    cmds.setAttr(BL + ".diffuseGain", 1)
                    #Layer1
                    if cmds.checkBox(self.layer1, q=1, v=1):
                        tex1 = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrLayer1 + PxrTexture + assetName + diffuse )
                        hsl1 = cmds.shadingNode("PxrHSL",asTexture=True, n= PxrLayer1 + PxrHSL + assetName + diffuse )
                        #connect attr
                        cmds.connectAttr("%s.resultRGB" %tex1 ,"%s.inputRGB" %hsl1)
                        cmds.connectAttr("%s.resultRGB" %hsl1 ,"%s.diffuseColor" %layer1)
                        cmds.setAttr(layer1 + ".diffuseGain", 1)
                    
                #setAttr
                cmds.setAttr(tex + ".linearize", 1)
            
            
                print ("add Diff")
            
        
        #SSS    ################################################################
        if cmds.checkBox(self.sss, q=1, v=1):
            #create nodes
            tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName + sss )
            hsl = cmds.shadingNode("PxrHSL",asTexture=True, n= PxrHSL + assetName + sss )
            #connect attr
            cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %hsl)
            if cmds.checkBox(self.pxrS, q=1, v=1):
                cmds.connectAttr("%s.resultRGB" %hsl ,"%s.subsurfaceColor" %shaderS)
                #setAttr
                cmds.setAttr(shaderS + ".diffuseGain", 0)
                cmds.setAttr(shaderS + ".subsurfaceType", 4)
                cmds.setAttr(shaderS + ".subsurfaceGain", 1)
                cmds.setAttr(shaderS + ".subsurfaceDmfp", 4)
                cmds.setAttr(shaderS + ".subsurfaceDirectionality", 0.8)
                
            elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                cmds.connectAttr("%s.resultRGB" %hsl ,"%s.subsurfaceColor" %layer1)
                #setAttr
                #baseLayer
                cmds.setAttr(layer1 + ".enableDiffuse", 0)
                cmds.setAttr(layer1 + ".enableSubsurface", 1)
                cmds.setAttr(layer1 + ".subsurfaceGain", 1)
                cmds.setAttr(layer1 + ".subsurfaceDmfp", 4)
                cmds.setAttr(layer1 + ".subsurfaceDirectionality", 0.8)
                #layerSurface
                cmds.setAttr(shaderLS + ".subsurfaceType", 4)
            #setAttr
            cmds.setAttr(tex + ".linearize", 1)
            
            
            print ("add SSS")
            
            
        #SPECULAR EDGE COLOR #################################################### 
        if cmds.objExists(PxrTexture + assetName + spec):
            print ("Schema conservÃ©")
            
                
        else :  
            if cmds.checkBox(self.spec, q=1, v=1):
                #create nodes
                tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName + spec)
                rmp = cmds.shadingNode("PxrRemap",asTexture=True, n= PxrRemap + assetName + spec)
                #connect attr
                cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %rmp)
            
                if cmds.checkBox(self.pxrS, q=1, v=1):
                    
                    ######
                    ## ATTENTION ##
                    #################################################
                   
                    cmds.connectAttr("%s.resultRGB" %rmp , pxrSurface + assetName + ".specularEdgeColor")
                    #setAttr pxrSurface
                    cmds.setAttr(shaderS + ".specularFresnelMode", 1)
                    cmds.setAttr(shaderS + ".specularModelType", 1)
                
                elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                    cmds.connectAttr("%s.resultRGB" %rmp ,"%s.specularEdgeColor" %layer1)
                    #setAttr pxrLayerSurface
                    #BaseLayer
                    cmds.setAttr(layer1 + ".enableSpecular", 1)
                    cmds.setAttr(layer1 + ".specularGain", 1)
                    #ShaderLS
                    cmds.setAttr(shaderLS + ".specularFresnelMode", 1)
                    cmds.setAttr(shaderLS + ".specularModelType", 1)
                #setAttr
                cmds.setAttr(tex + ".linearize", 1)
            
                print ("add SPEC")
            
            
        #SPECULAR ROUGHNESS  #########################################################
        if cmds.checkBox(self.specRough, q=1, v=1):
            #create nodes
            tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName + specRough)
            rmp = cmds.shadingNode("PxrRemap",asTexture=True, n= PxrRemap + assetName + specRough)
            #connect attr
            cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %rmp)
            if cmds.checkBox(self.pxrS, q=1, v=1):
                cmds.connectAttr("%s.resultR" %rmp ,"%s.specularRoughness" %shaderS)
            elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                cmds.connectAttr("%s.resultR" %rmp ,"%s.specularRoughness" %layer1)
            #setAttr
            cmds.setAttr(tex + ".linearize", 1)
            
            print ("add SPEC ROUGHNESS")
            
        
        #ROUGH SPECULAR EDGE COLOR    #####################################################
        if cmds.checkBox(self.roughSpec, q=1, v=1):
            #create nodes
            tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName + roughSpec)
            rmp = cmds.shadingNode("PxrRemap",asTexture=True, n= PxrRemap + assetName + roughSpec)
            #connect attr
            cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %rmp)
            if cmds.checkBox(self.pxrS, q=1, v=1):
                cmds.connectAttr("%s.resultRGB" %rmp ,"%s.roughSpecularEdgeColor" %shaderS)
                #setAttr pxrSurface
                cmds.setAttr(shaderS + ".roughSpecularFresnelMode", 1)
                cmds.setAttr(shaderS + ".roughSpecularModelType", 1)
                
            elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                cmds.connectAttr("%s.resultRGB" %rmp ,"%s.roughSpecularEdgeColor" %layer1)
                #setAttr pxrLayerSurface
                #BaseLayer
                cmds.setAttr(layer1 + ".enableRoughSpecular", 1)
                cmds.setAttr(layer1 + ".roughSpecularGain", 1)
                #ShaderLS
                cmds.setAttr(shaderLS + ".roughSpecularFresnelMode", 1)
                cmds.setAttr(shaderLS + ".roughSpecularModelType", 1)
            #setAttr
            cmds.setAttr(tex + ".linearize", 1)
            
            print ("add ROUGH SPEC")
            
            
        #ROUGH SPECULAR ROUGHNESS  ###############################################################
        if cmds.checkBox(self.roughSpecRough, q=1, v=1):
            #create nodes
            tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName + roughSpecRough)
            rmp = cmds.shadingNode("PxrRemap",asTexture=True, n= PxrRemap + assetName + roughSpecRough)
            #connect attr
            cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %rmp)
            if cmds.checkBox(self.pxrS, q=1, v=1):
                cmds.connectAttr("%s.resultR" %rmp ,"%s.roughSpecularRoughness" %shaderS)
            elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                cmds.connectAttr("%s.resultR" %rmp ,"%s.roughSpecularRoughness" %layer1)
            #setAttr
            cmds.setAttr(tex + ".linearize", 1)
            
            print ("add ROUGH SPEC ROUGHNESS")
            
          
        #BUMP #############################################################################
        if cmds.checkBox(self.bump, q=1, v=1):
            #create nodes
            tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName + bump)
            rmp = cmds.shadingNode("PxrRemap",asTexture=True, n= PxrRemap + assetName + bump)
            bmp = cmds.shadingNode("PxrBump",asTexture=True, n= PxrBump + assetName + bump)
            #connect attr
            cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %rmp)
            cmds.connectAttr("%s.resultR" %rmp ,"%s.inputBump" %bmp)
            if cmds.checkBox(self.pxrS, q=1, v=1):
                cmds.connectAttr("%s.resultN" %bmp ,"%s.bumpNormal" %shaderS)
            elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                cmds.connectAttr("%s.resultN" %bmp ,"%s.bumpNormal" %layer1)
            #setAttr
            cmds.setAttr(tex + ".linearize", 1)
            
            print ("add BUMP")
            
        
        #NORMAL ################################################################################
        if cmds.checkBox(self.normal, q=1, v=1):
            #create nodes
            tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName + normal)
            adj = cmds.shadingNode("PxrAdjustNormal",asTexture=True, n= PxrAdjustNormal + assetName + normal)
            norm = cmds.shadingNode("PxrNormalMap",asTexture=True, n= PxrNormal + assetName + normal)
            #connect attr
            cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputNormal" %adj)
            cmds.connectAttr("%s.resultN" %adj ,"%s.inputRGB" %norm)
            if cmds.checkBox(self.pxrS, q=1, v=1):
                cmds.connectAttr("%s.resultN" %norm ,"%s.bumpNormal" %shaderS)
            elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                cmds.connectAttr("%s.resultN" %norm ,"%s.bumpNormal" %layer1)
            print ("add NORMAL")
            
            
            
        #SCALAR DISPLACE #########################################################################
        if cmds.checkBox(self.scalar, q=1, v=1):
            #create nodes
            tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName)
            rmp = cmds.shadingNode("PxrRemap",asTexture=True, n= PxrRemap + assetName)
            dispTrans = cmds.shadingNode("PxrDispTransform",asTexture=True, n= PxrDispTransform + assetName)
            disp = cmds.shadingNode("PxrDisplace",asShader=True, n= PxrDisplace + assetName)
            #connect attr
            cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %rmp)
            cmds.connectAttr("%s.resultR" %rmp ,"%s.dispScalar" %dispTrans)
            cmds.connectAttr("%s.resultF" %dispTrans ,"%s.dispScalar" %disp)
            
            if cmds.checkBox(self.pxrS, q=1, v=1):
                cmds.connectAttr("%s.outColor" %disp ,"%s.rman__displacement" %shading_group)
            elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                cmds.connectAttr("%s.outColor" %disp ,"%s.rman__displacement" %shading_group)
            print ("add SCALAR DISPLACEMENT")
            
            
        #VECTOR DISPLACE ############################################################################
        if cmds.checkBox(self.vector, q=1, v=1):
            #create nodes
            tex = cmds.shadingNode("PxrTexture",asTexture=True, n= PxrTexture + assetName)
            rmp = cmds.shadingNode("PxrRemap",asTexture=True, n= PxrRemap + assetName)
            dispTrans = cmds.shadingNode("PxrDispTransform",asTexture=True, n= PxrDispTransform + assetName)
            disp = cmds.shadingNode("PxrDisplace",asShader=True, n= PxrDisplace + assetName)
            #connect attr
            cmds.connectAttr("%s.resultRGB" %tex ,"%s.inputRGB" %rmp)
            cmds.connectAttr("%s.resultRGB" %rmp ,"%s.dispVector" %dispTrans)
            cmds.connectAttr("%s.resultXYZ" %dispTrans ,"%s.dispVector" %disp)
            
            if cmds.checkBox(self.pxrS, q=1, v=1):
                cmds.connectAttr("%s.outColor" %disp ,"%s.rman__displacement" %shading_group)
            elif cmds.checkBox(self.pxrLS, q=1, v=1) :
                cmds.connectAttr("%s.outColor" %disp ,"%s.rman__displacement" %shading_group)
            print ("add VECTOR DISPLACEMENT")
           
           





mainWindow()