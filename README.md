
![LUI Draft](http://fs1.directupload.net/images/141226/qd6z8ysu.png)

===

Lightweight user interface for Panda3D


### Installation

First, grab a recent Panda3D build <a href="https://github.com/panda3d/panda3d">here</a>. After you downloaded it, replace the following files with the ones provided in the repositority:

- `/makepanda/makepanda.py`
- `/panda/src/pandabase/pandasymbols.h`

After you did this, create the folder `panda/src/lui/` and copy the contents of the `Source/` folder into it.
Now you should able to compile panda, if you do not use `--everything` you have to add `--use-lui` to compile with LUI.

### Running the Samples

You can find the first sample at `Builtin/main.py`. More will follow!
