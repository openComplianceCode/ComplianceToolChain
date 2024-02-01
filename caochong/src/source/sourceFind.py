


import os
import platform
import shlex
import shutil
import subprocess
import time
from util.catchUtil import catch_error
from util.popUtil import popKill


class Source_file(object):

    @catch_error
    def find_source_files(self, directory):
        source_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_source_file(file_path):
                    source_files.append(file_path)
        return source_files
    
    @catch_error
    def cp_source_files(self, directory, cpPath):
        system = platform.system()
        fileList = self.find_source_files(directory)       
        common_prefix = os.path.commonprefix(fileList)
        common_prefix = os.path.dirname(os.path.dirname(common_prefix))
        fileNameList = [s[len(common_prefix):] for s in fileList]
        for index, file in enumerate(fileNameList):
            try:
                fileDir = os.path.dirname(file)
                tempFile = cpPath + "/" + fileDir            
                if os.path.exists(tempFile) is False:
                    os.makedirs(tempFile)                
                if system == 'Windows':
                    shutil.copy(fileList[index], tempFile)                   
                else:
                    command = shlex.split('cp -r %s  %s' % (fileList[index], tempFile))
                    resultCode = subprocess.Popen(command)
                    while subprocess.Popen.poll(resultCode) == None:
                        time.sleep(1)
                    popKill(resultCode)
            except:
                pass
        return "Done"

    @catch_error
    def is_source_file(self, file_path):
        # 判断文件扩展名
        source_extensions = ['.py', '.java', '.cpp', '.h', '.js', '.cs', '.rb', '.go', '.swift', '.html', '.css', '.php', '.sh'
                             'license', 'notice', 'copying', 'third_party_open_source_software_notice', 'copyright', '.spec']
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in source_extensions:
            return True