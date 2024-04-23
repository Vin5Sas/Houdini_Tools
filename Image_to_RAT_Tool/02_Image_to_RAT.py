import hou
import os
from PySide2 import QtWidgets, QtGui

class convertImage(QtWidgets.QDialog):
        def __init__(self):
                super(convertImage, self).__init__()
                
                self.setWindowTitle("Image to RAT Converter")
                self.setMinimumWidth(300)
                
                #Set instruction label for user
                mainLabel = QtWidgets.QLabel("\nSelect an image (.jpg, .png, .tiff, .bmp) to convert to .rat format\n")

                #File Path Input
                self.file_path_line_edit = QtWidgets.QLineEdit()
                
                #Browse Button
                browse_button = QtWidgets.QPushButton("Browse Image")
                browse_button.clicked.connect(self.browse_file)
                
                #Import Button
                import_button = QtWidgets.QPushButton("Convert Image")
                import_button.clicked.connect(self.import_image)

                #Create vertical layout using QVBoxLayout and add all the above crated widgets
                layout = QtWidgets.QVBoxLayout()
                layout.addWidget(mainLabel)
                layout.addWidget(self.file_path_line_edit)
                layout.addWidget(browse_button)
                layout.addWidget(import_button)
                
                #set the layout so it appears on the window
                self.setLayout(layout)

        #method for declaring and initializing browse file button using QFileDialog()
        def browse_file(self):
                file_dialog = QtWidgets.QFileDialog()
                file_path, _ = file_dialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg *.bmp *.tiff)")
                
                if file_path:
                        self.file_path_line_edit.setText(file_path)

        #method for import image and convert image fucntions, which are the core functionality
        def import_image(self):
                image_path = self.file_path_line_edit.text()
                if not os.path.isfile(image_path):
                        hou.ui.displayMessage("Invalid file path", severity=hou.severityType.Error)
                        return
                print("ImagePath: ", image_path)
                convert_image_to_RAT(image_path)
                self.close()

def convert_image_to_RAT(image_path):
    #set node in Houdini's img context
    imgContext = hou.node("/img")

    #create a cop Image Network at img level
    copNode = imgContext.createNode("img", node_name="convert_image")

    #create a 'File' Node inside the Image Network and set parameter values
    fileNode = copNode.createNode("file")

    fileNode.parm("filename1").set(image_path)
                
    fileNode.parm("linearize").set(1)
                
    print("Image successfully imported into copnet!")
    
    #create a Rop File Output Node, set its parameters, and link it to the File Node
    rop_node = copNode.createNode("rop_comp")
    
    rop_node.parm("trange").set(0)
    
    rop_node.setInput(0,fileNode)
    
    save_path = image_path.split(".")[0] + ".rat"
    
    rop_node.parm("copoutput").set(save_path)
    
    print("RAT file will be saved at: ", save_path)
    

    #create a Confirmation Window to get user confirmation to convert selected image file
    confirm_window = confirmationWindow()
    confirm_window.exec_()
    confirmationVal = confirm_window.proceedVal
    
    if confirmationVal == 1:
        print("Confirmation to proceed received")
        rop_node.render()
        print("Selected image was converted to RAT and saved at ", save_path)
    else:
        print("Confirmation to be received further")
    
class confirmationWindow(QtWidgets.QDialog):
    def __init__(self):
        super(confirmationWindow, self).__init__()
        
        self.setWindowTitle("Image Conversion Confirmation")
        self.setMinimumWidth(500)
        label = QtWidgets.QLabel("Do you want to proceed Converting the image?", self)
        
        proceed_button = QtWidgets.QPushButton("Proceed", self)
        proceed_button.clicked.connect(self.setProceedVal)
        
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.setCancelVal)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(proceed_button)
        layout.addWidget(cancel_button)
        
        self.setLayout(layout)
        
    def setProceedVal(self):
        self.proceedVal = 1
        self.close()
        
    def setCancelVal(self):
        self.proceedVal = 0
        self.close()
    
window = convertImage()
window.exec_()