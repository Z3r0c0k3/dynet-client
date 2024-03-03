from func import *

# git pull
print("- Checking for latest updates...")
pull_rst = git_pull()
if pull_rst == 0:
    print("~ lasted update complete")
elif pull_rst == 2:
    print("! Canceled the update check")
else:
    print("! The update failed because an unknown error occurred.")
    print("  Check your internet connection, etc.")

# requirements.txt install
print("- requirements.txt installing . . . ")
inst_reqi_rst = install_requirements()
if inst_reqi_rst == 0:
    print("~ requirements.txt install complete")
elif inst_reqi_rst == 2:
    print("! Canceled the requirements.txt install")
else:
    print("! The requirements.txt install failed because an unknown error occurred.")
    print("  Check your internet connection, etc.")
    