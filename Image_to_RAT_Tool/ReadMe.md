Here's a tiny Houdini utility Shelf Tool which let's you convert an image to .rat format, for those who are unfamiliar with copnet compositing to convert images. 

Random Access Texture maps (RAT), one of Houdini's image format, are tuned for texture mapping. The format allows the renderer to access portions of the texture without having to load the whole image into memory at once. (more info about RAT at https://www.sidefx.com/docs/houdini/io/formats/image_formats.html)

This tool was written in Python and the GUI was done with the help of PySide modules. 

Tech Tip: Alternatively, this conversion can be done from Terminal/Houdini Shell with the following command:

iconvert butterfly.pic butterfly.rat

(you may have to cd to your file location and change the file name)

(https://www.sidefx.com/docs/houdini/shade/convert.html)