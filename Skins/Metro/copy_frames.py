
import os
from shutil import copyfile as copy
os.chdir("res/")

for f in os.listdir("."):
    if f.startswith("Popup_") or f.startswith("Frame_") or f.startswith("SunkenFrame_"):
        copy("../flat.png" if "_Mid" in f else "../border.png", f)


copy("ButtonDefault.png", "ButtonDefaultFocus.png")
copy("ButtonDefault.png", "ButtonDefaultFocus_Left.png")
copy("ButtonDefault.png", "ButtonDefaultFocus_Right.png")
copy("ButtonDefault.png", "ButtonDefault_Left.png")
copy("ButtonDefault.png", "ButtonDefault_Right.png")

copy("ButtonGreen.png", "ButtonGreenFocus.png")
copy("ButtonGreen.png", "ButtonGreenFocus_Left.png")
copy("ButtonGreen.png", "ButtonGreenFocus_Right.png")
copy("ButtonGreen.png", "ButtonGreen_Left.png")
copy("ButtonGreen.png", "ButtonGreen_Right.png")

copy("Selectbox.png", "Selectbox_Left.png")
copy("Selectbox.png", "SelectboxActive.png")
copy("Selectbox.png", "SelectboxActive_Left.png")

copy("ProgressbarFg.png", "ProgressbarFg_Right.png")
copy("ProgressbarFg.png", "ProgressbarFg_Left.png")
copy("ProgressbarFg.png", "ProgressbarFg_Finish.png")
copy("ProgressbarBg.png", "ProgressbarBg_Right.png")
copy("ProgressbarBg.png", "ProgressbarBg_Left.png")

copy("SliderBgFill.png", "SliderBgFill_Left.png")
copy("SliderBg.png", "SliderBg_Left.png")
copy("SliderBg.png", "SliderBg_Right.png")

copy("InputField.png", "InputField_Left.png")
copy("InputField.png", "InputField_Right.png")

for align in "TR TL BR BL Top Right Bottom Left".split():
    copy("Selectdrop_Mid.png", "Selectdrop_" + align + ".png")
