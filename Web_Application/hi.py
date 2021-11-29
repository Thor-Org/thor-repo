import subprocess
print("hello")
subprocess.run("ldconfig -p | grep mysql")
