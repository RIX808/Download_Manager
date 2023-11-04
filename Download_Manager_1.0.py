# Python Download Manager 1.0
# Modified from https://github.com/tuomaskivioja/File-Downloads-Automator/blob/main/fileAutomator.py
# 2023-11-03
# Python Version 3.12.0

import os
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Create env variables to mask path names
# create DLOADS env variable in Windows first!
source_dir = os.environ.get('DLOADS')
# Folders
dest_dir_music =            os.path.join(source_dir, 'MUSIC')           # Merge source dir with file folder to create path
dest_dir_video =            os.path.join(source_dir, 'VIDEOS')          
dest_dir_image =            os.path.join(source_dir, 'IMAGES')          
dest_dir_documents =        os.path.join(source_dir, 'DOCS')            
dest_dir_emails =           os.path.join(source_dir, 'EMAILS')          
dest_dir_compression =      os.path.join(source_dir, 'COMPRESSED')      
dest_dir_exe =              os.path.join(source_dir, 'APPS_EXE')        
dest_dir_ico =              "E:\\PICTURES\\Folder_Icons"
dest_dir_scripts =          os.path.join(source_dir, 'SCRIPTS')         
dest_dir_pyScripts =        os.path.join(source_dir, 'SCRIPTS')         


# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", 
                    ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", 
                    ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", 
                    ".svgz", ".ai", ".eps"]

# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",".mp4", 
                    ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", 
                    ".avchd", ".mkv"]

# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

# ? supported Document types
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", 
                       ".txt", ".pps"]

# ? Supported Email types
email_extensions = [".eml", ".msg", ".ost", ".pst", ".vcf", ".emlx", ".email", ".oft"] 

# ? Supported compression types
compression_extensions = [".zip", ".7zip", ".rar", ".tar", ".zipx", ".ace", ".gz", ".iso", 
                          ".lbr", ".sbx", ".mar", ".a", ".ar", ".br", ".bz2", ".cab", ".dmg", 
                          ".tar.gz", ".tar.Z", ".tar.bz2", ".tbz2", ".tar.lz", ".tar.xz", ".txz",
                          ".bin", ".app", ".pkg", ".z"]

# ? Supported executables 
exe_extensions = [".exe", ".msi", ".deb", ".com"]

# ? Supported icons
icon_extensions = [".ico"]

# Supported Script files
script_extensions = [".ps1", ".ahk", ".bat", ".jar", ".gadget", 
                  ".cgi", ".pl", ".wsf", ".apk", ".html", ".htm", ".js", ".css", ".asp", 
                  ".aspx", ".jsp", ".rss"]

# Supported Script files
pyscript_extensions = [".py"]

# Make filename unique
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

# Moves files
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

class MoverHandler(FileSystemEventHandler):
    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    # ? .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_email_files(entry, name)
                self.check_compression_files(entry, name)
                self.check_exe_files(entry, name)
                self.check_ico_files(entry, name)
                self.check_script_files(entry, name)
                self.check_pyscript_files(entry, name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_music, entry, name)
                logging.info(f"Moved audio file: {name} to {dest_dir_music}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name} to {dest_dir_video}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name} to {dest_dir_image}")
    
    def check_ico_files(self, entry, name):  # * Checks all icon Files
        for icon_extension in icon_extensions:
            if name.endswith(icon_extension) or name.endswith(icon_extension.upper()):
                move_file(dest_dir_ico, entry, name)
                logging.info(f"Moved Icon file: {name} to {dest_dir_ico}")

    def check_script_files(self, entry, name):  # * Checks all script Files
        for script_extension in script_extensions:
            if name.endswith(script_extension) or name.endswith(script_extension.upper()):
                move_file(dest_dir_scripts, entry, name)
                logging.info(f"Moved script file: {name} to {dest_dir_scripts}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name} to {dest_dir_documents}")

    def check_email_files(self, entry, name):  # * Checks all email Files
        for emails_extension in email_extensions:
            if name.endswith(emails_extension) or name.endswith(emails_extension.upper()):
                move_file(dest_dir_emails, entry, name)
                logging.info(f"Moved email file: {name} to {dest_dir_emails}")
                
    def check_compression_files(self, entry, name):  # * Checks all compressed Files
        for compressions_extension in compression_extensions:
            if name.endswith(compressions_extension) or name.endswith(compressions_extension.upper()):
                move_file(dest_dir_compression, entry, name)
                logging.info(f"Moved compressed file: {name} to {dest_dir_compression}")
                
    def check_exe_files(self, entry, name):  # * Checks all exe Files
        for exes_extension in exe_extensions:
            if name.endswith(exes_extension) or name.endswith(exes_extension.upper()):
                move_file(dest_dir_exe, entry, name)
                logging.info(f"Moved executable file: {name} to {dest_dir_exe}")

    def check_pyscript_files(self, entry, name):  # * Checks all exe Files
        for pyscript_extension in pyscript_extensions:
            if name.endswith(pyscript_extension) or name.endswith(pyscript_extension.upper()):
                move_file(dest_dir_pyScripts, entry, name)
                logging.info(f"Moved executable file: {name} to {dest_dir_pyScripts}")         

# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()