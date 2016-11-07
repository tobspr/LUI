[![Build Status](https://travis-ci.org/tobspr/LUI.svg?branch=master)](https://travis-ci.org/tobspr/LUI)

# Lightweight User Interface

<img src="http://fs5.directupload.net/images/151207/ltl76bsj.png" align="right" />


### Requirements

- **Panda3D SDK** (recent devel version)
- **CMake**

### Installation

Run `python update_module_builder.py`. This will create a build file in the current directory, which you can then run with `python build.py`.
Now there should be a `lui.pyd` or `lui.so` depending on your system.

If you are on **windows**, copy the .pyd into `PATH_TO_PANDA_SDK/panda3d/lui.pyd`.

If you are on **linux**, copy the .so into `usr/lib/panda3d/lui.so`


### Running the Samples

You can find various samples for the different LUI components in the `Demos` folder.

### Documentation

There is no official documentation yet, however if you look at the `Demos` folder, there should be a lot of self-explanatory code.
