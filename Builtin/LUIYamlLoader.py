"""
file: LUIYamlLoader.py
created by: tosh007 (7.5.2016)

This file implements loading a user interface from a yaml file
"""

import sys,re
from copy import *
from yaml import *
from .LUIEverything import *
from direct.directnotify.DirectNotify import DirectNotify

notify = DirectNotify().newCategory("LUIYamlLoader")

class LUIYamlLoader:
    """Transforms a yaml file into a LUI-based user interface"""
    def __init__(self, top_node):
        self.default_parent = top_node
        self._gui = {}
        self.gui_active=False

    def load_gui(self, description):
        """loads gui from a .yaml file under description.filename"""
        self.delete_gui()
        if issubclass(description, LUIYamlDescription):
            description = description()
            path = description.filename
            self.description = description
        else:
            path = description
            self.description = LUIYamlDescription()
        self.description.gui=self
        self.gui_active = True
        ui_data=load_yaml_file(path)
        self.ui_data={}
        code=None
        self.all_binds={}    # {element:{event:func}}
        for pair in ui_data:
            name = pair.keys()[0]
            element_data = pair[name]
            fname = re.sub(r"\{[0-9]+\}","", name)
            self.ui_data[fname]=(name,element_data)
            self._load_element(name, element_data, self.default_parent)
        if self.description.handle_creation:self.description.handle_creation()
        # finally, execute the bind statements
        for element in self.all_binds:
            luiobj = self._gui[element]
            binds = self.all_binds[element]
            for event in binds:
                func = binds[event]
                func = self.get_handler(func)
                luiobj.bind(event,func)

    def delete_gui(self):
        """delete all gui elements created"""
        if self.gui_active:
            if self.description.handle_destruction:self.handle_destruction()
            del self.description.gui
            for luiobj in self._gui.values():
                self._delete_lui_object(luiobj)
            self.gui_active = False
            self._gui={}

    def instance_element(self, name, parent, format):
        """creates a subtree from a template given its name, a parent node, and a formatting list"""
        unformatted_name, element_data = deepcopy(self.ui_data[name])
        self._load_element(unformatted_name, element_data, parent, format,True)

    def delete_instanced_element(self, name, formatlist):     # give the same format and name as to instance_element()
        fname, element_data = deepcopy(self.ui_data[name])
        self._delete_branch(fname,element_data, formatlist)

    def _load_element(self, name, element_data, parent, formatlist=None, force_load=False):
        """loads a lui node, recursively loading children"""
        if formatlist:
            name=name.format(*formatlist)
            self._format_kw(element_data, formatlist)
        if name in self._gui:
            notify.error("every yamlgui lui element must have a unique name, "+name+" already exists")
        block_load = self._extract_kw(element_data, "instancing_template")    # do not automatically load this branch
        if (not block_load) or force_load:
            type = self._extract_kw(element_data, "type", False)
            typedef = LUIWidgets[type]
            binds  = self._extract_kw(element_data, "bind", format=formatlist)
            children  = self._extract_kw(element_data, "children")
            if binds:
                self.all_binds[name] = binds
            args = element_data
            # problem: LUIHorizontalLayout needs a parent, but shouldn't the parent be specified using parentLayout.add(obj)
            parentToLayout = isinstance(parent, LUIBaseLayout)
            layoutChild    = issubclass(typedef, LUIBaseLayout)
            if not parentToLayout:
                args["parent"] = parent
            else:
                if layoutChild:
                    parent_dummy = LUIObject()
                    args["parent"] = parent_dummy
            # finally construct lui element
            obj = typedef(**args)
            self._gui[name] = obj
            if parentToLayout:
                if layoutChild:
                    parent.add(parent_dummy)
                else:
                    parent.add(obj)
            if children:
                for pair in children:
                    name = pair.keys()[0]
                    data=pair.values()[0]
                    self._load_element(name, data, obj, formatlist)

    def _delete_branch(self, name, element_data, formatlist):
        children = self._extract_kw(element_data,"children")
        fname = name.format(*formatlist)
        try:
            self._delete_lui_object(self._gui[fname])
            del self._gui[fname]
        except KeyError:
            notify.error("Tried to delete nonexisting LUI Widget")
        if children:
            for pair in children:
                name=pair.keys()[0]
                data=pair.values()[0]
                self._delete_branch(name, data, formatlist)

    def _delete_lui_object(self,luiobj):
        if luiobj.has_parent():
            luiobj.clear_parent()
        if isinstance(luiobj, LUIBaseLayout):
            luiobj.reset()
        luiobj.unbind_all()

    def _extract_kw(self, kw, argname, try_ = True, format=None):
        """helper function for keyword argument assembly"""
        try:
            value = kw[argname]
            del kw[argname]
        except KeyError:
            if not try_:
                raise KeyError(argname + " is required for constructing an ui element")
            value = None
        if (type(value) is str) and format:
            value=value.format(*format)
        return value

    def _format_kw(self, kw, format):
        """helper function for keyword argument assembly"""
        for key in kw.keys():
            if type(kw[key]) is str:
                kw[key]=kw[key].format(*format)

    def __del__(self):
        self.delete_gui()

    # allow functions to acces gui directly
    def __getattr__(self,attr):    
        return self._gui[attr]

    def get_handler(self, name):
        return getattr(self.description, name)


class LUIYamlDescription(object):
    """
    For every UI to load, create a subclass of this,
    You should define all handler functions you need here
    filename is the path to the .yaml file
    handle_creation is called after loading the ui, just before binding events
    handle_destruction is called when the gui is deleted
    """
    filename = ""
    handle_creation=None
    handle_destruction=None
