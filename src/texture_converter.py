import os
import glob
import subprocess

DDS_SOURCE_PATH = r'F:\Zunk\TextureTests\SRC'
TGA_DEST_PATH = r'F:\Zunk\TextureTests\DEST'


def ListSubdirs(DirPath):
    """
    Returns a list of all subdirectories in the given DirPath.\n
    The list returned contains all sub-directories inside the sub-directories too.
    """
    DirContent = os.listdir(DirPath)

    # If there is no content (files or folders) inside DirPath, return empty list
    if not DirContent:
        return []
    
    # Sub directories in current DirPath
    SubDirs = [os.path.join(DirPath, sd) for sd in os.listdir(DirPath) if
               os.path.isdir(os.path.join(DirPath, sd))]

    # Directories inside subdirectory's subdirectory
    SubDirs_SD = []
    for SubDir in SubDirs:
        SubDirs_SD += ListSubdirs(SubDir)
    
    SubDirs += SubDirs_SD
    return SubDirs


def FindFiles(DirPath, FileExtension=""):
    """
    Returns the list of all files inside the given directory (DirPath) and all
    of it's sub-directories. If FileExtension is provided then only files 
    with the given FileExtension are returned.\n
    File extension should be provided as .ext, not ext
    """
    FilesList = []
    FilesList += glob.glob(DirPath + '\\*' + FileExtension)

    SubDirs = ListSubdirs(DirPath)
    for SubDir in SubDirs:
        FilesList += glob.glob(SubDir + '\\*' + FileExtension)
    
    return FilesList


def ConvertAndExportTextures(TextureFilesList):
    for SourceFilePath in TextureFilesList:
        SourceDir = os.path.dirname(SourceFilePath)
        DestDir = SourceDir.replace(DDS_SOURCE_PATH, TGA_DEST_PATH)
        if os.path.exists(DestDir):
            assert os.path.isdir(DestDir)
        else:
            os.makedirs(DestDir)

        # source file name in lower case
        SourceFileName = os.path.basename(SourceFilePath).lower()
        DestFileName = "T_" + SourceFileName.split(".")[0] + ".tga"
        DestFilePath = DestDir + os.sep +  DestFileName

        ConvertToolPath = r'C:\Program Files\ImageMagick-7.0.7-Q16\convert.exe'

        print(SourceFilePath, DestFilePath)
        subprocess.call(r'{0} "{1}" "{2}"'.format(ConvertToolPath, SourceFilePath, DestFilePath))


if __name__ == "__main__":
    TextureFilesList = FindFiles(DDS_SOURCE_PATH, ".dds")
    ConvertAndExportTextures(TextureFilesList)
    
