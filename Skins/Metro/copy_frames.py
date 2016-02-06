
import os
import shutil
os.chdir("res/")

for f in os.listdir("."):
    if f.startswith("Popup_") or f.startswith("Frame_") or f.startswith("SunkenFrame_"):
        shutil.copyfile("../flat.png", f)


shutil.copyfile("ButtonDefault.png", "ButtonDefaultFocus.png")
shutil.copyfile("ButtonDefault.png", "ButtonDefaultFocus_Left.png")
shutil.copyfile("ButtonDefault.png", "ButtonDefaultFocus_Right.png")
shutil.copyfile("ButtonDefault.png", "ButtonDefault_Left.png")
shutil.copyfile("ButtonDefault.png", "ButtonDefault_Right.png")

shutil.copyfile("ButtonGreen.png", "ButtonGreenFocus.png")
shutil.copyfile("ButtonGreen.png", "ButtonGreenFocus_Left.png")
shutil.copyfile("ButtonGreen.png", "ButtonGreenFocus_Right.png")
shutil.copyfile("ButtonGreen.png", "ButtonGreen_Left.png")
shutil.copyfile("ButtonGreen.png", "ButtonGreen_Right.png")

shutil.copyfile("Selectbox.png", "Selectbox_Left.png")
shutil.copyfile("Selectbox.png", "SelectboxActive.png")
shutil.copyfile("Selectbox.png", "SelectboxActive_Left.png")
