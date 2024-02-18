import sys
import subprocess
import time

from os.path import exists
from os import remove

t = time.time()

path = sys.argv[0]
dirr = path[:path.rfind('\\')]
pxcp = f'{dirr}\\PixelComposer.exe'
args = " ".join(sys.argv[1:])

verbose = False
persist = False

waitInput = False
inputPath = f'{dirr}\\in'
printErr  = False

if exists(inputPath):
    remove(inputPath)

for arg in sys.argv:
    if arg == '-v' or arg == '--verbose':
        verbose = True
    elif arg == '-p' or arg == '--persist':
        persist = True

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(p):
    if(verbose):
        print(p)

log("""
   ___ _          _   ___                                          
  / _ (_)_  _____| | / __\___  _ __ ___  _ __   ___  ___  ___ _ __ 
 / /_)/ \ \/ / _ \ |/ /  / _ \| '_ ` _ \| '_ \ / _ \/ __|/ _ \ '__|
/ ___/| |>  <  __/ / /__| (_) | | | | | | |_) | (_) \__ \  __/ |   
\/    |_/_/\_\___|_\____/\___/|_| |_| |_| .__/ \___/|___/\___|_|   
                                        |_|                        
    
>>>>>>>>>>>>>>>>>>>>> PixelComposer CLI v0.1 <<<<<<<<<<<<<<<<<<<<<
    
""")

if not exists(pxcp):
    log("PixelComposer not found. Please make sure PixelComposer is installed and the CLI is being run from the same directory.\n")
    exit(1)

log(" ▶️ Initializing PixelComposer...")

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

with subprocess.Popen(f'{pxcp} {args} -h -output res  | echo', stdout = subprocess.PIPE, startupinfo = startupinfo) as pxcProcess :
    while pxcProcess.poll() is None:
        lines = pxcProcess.stdout.read1().decode('utf-8').split('\n')
        
        for line in lines:
            #log(line)

            if(line.startswith("CLI:")):
                if(line.startswith("CLI: [Error]")):
                    log(f'{color.FAIL}{line[13:]}{color.ENDC}')
                else:
                    log(" ▶️ " + line[5:])
            
            elif(line.startswith("WAIT")):
                if persist:
                    waitInput = True

            elif(line.startswith("[ERROR BEGIN]")):
                printErr  = True
                
            elif(line.startswith("[ERROR END]")):
                printErr  = False

            elif(line.startswith("###game_end###")):
                log(" ▶️ Closing PixelComposer...")
                break

            elif printErr:
                log(f'{color.FAIL}{line}{color.ENDC}')
        
        if not waitInput:
            time.sleep(0.1)
        else:
            cmd_input = input("> ")
            with open(inputPath, 'x') as f:
                f.write(cmd_input)
            waitInput = False
            
            if cmd_input == "exit":
                pxcProcess.terminate()
                break

log(f" ✔️ Operation completed in {(time.time() - t):.2f}s.\n")