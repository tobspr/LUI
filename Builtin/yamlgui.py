"""
this file implements loading a user interface from a yaml file
"""

from yaml import *
import imp
from copy import *
import gc


# import all lui builtin modules
# using a shortcut script
from LUIEverything import *




class yamlgui:
	def __init__(self, top_node):
		self.default_parent = top_node
		self.gui = {}
		self.script_module = imp.new_module("script_module")	# allows script execution
		
		self.gui_active=False

		


	def extract_kw(self, kw, argname, try_ = True, format=None):
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



	def format_kw(self, kw, format):
		for key in kw.keys():
			if type(kw[key]) is str:
				kw[key]=kw[key].format(*format)





	def loadGui(self,path):
		if self.gui_active:
			self.deleteGui()
		self.script_module.__dict__.clear()
		self.script_module.gui=self
		self.gui_active = True
		ui_data=load_yaml_file(path)
		self.ui_data={}
		code=None
		self.all_binds={}	# {element:{event:func}}
		# first, iterate over the parsed datastructure
		# UI elements will be created immediately
		
		for pair in ui_data:
			assert len(pair) == 1
			name = pair.keys()[0]
			element_data = pair[name]
			

			if name=="python":
				code = element_data
				exec code in self.script_module.__dict__
			else:
				self._loadElement(name, element_data, self.default_parent)
				self.ui_data[name]=element_data
			

		# finally, execute the bind statements, as they might use custom code from yaml
		for element in self.all_binds:
			luiobj = self[element]
			binds = self.all_binds[element]
			for event in binds:
				func = binds[event]
				func = self[func]
				luiobj.bind(event,func)



	def instanceElement(self, name, parent, format):	# allows to instance branches
		self._loadElement(name, deepcopy(self.ui_data[name]), parent, format,True)


	def _loadElement(self, name, element_data, parent, formatlist=None, force_load=False):
		if formatlist:
			name=name.format(*formatlist)
		assert name not in self.gui, "every yamlgui lui element must have a unique name, "+name+" already exists"
		block_load = self.extract_kw(element_data, "block_load")	# only do not automatically load this branch
		if (not block_load) or force_load:
			type = self.extract_kw(element_data, "type", False)
			typedef = LUIWidgeds[type]
			binds  = self.extract_kw(element_data, "bind", format=formatlist)
			children  = self.extract_kw(element_data, "children")


			if binds:
				self.all_binds[name] = binds

			
			args = element_data
			if formatlist:
				self.format_kw(args, formatlist)
			# PROBLEM: LUIHorizontalLayout needs a parent, but shouldn't the parent be specified using parentLayout.add(obj) ????
			parentToLayout = isinstance(parent, LUIBaseLayout)
			layoutChild    = issubclass(typedef, LUIBaseLayout)
			if not parentToLayout:
				args["parent"] = parent
			else:
				if layoutChild:	# LUILayouts need a parent object passed
					parent_dummy = LUIObject()
					args["parent"] = parent_dummy

			

			# finally construct lui element
			obj = typedef(**args)
			self.gui[name] = obj

			if parentToLayout:
				if layoutChild:
					parent.add(parent_dummy)
				else:
					parent.add(obj)

			if children:
				for pair in children:
					#print len(pair)
					assert len(pair)==1

					name = pair.keys()[0]
					data=pair.values()[0]
					self._loadElement(name, data, obj, formatlist)





	def deleteGui(self):
		if self.gui_active:
			for luiobj in self.gui.values():
				if luiobj.has_parent():
					luiobj.clear_parent()
				luiobj.unbind_all()
			self.gui_active = False
			self.gui={}
		gc.collect()


	def __del__(self):
		self.deleteGui()



	# allow functions to acces gui directly
	def __getattr__(self,attr):
		try:
			return self.gui[attr]
		except KeyError:
			return self.script_module.__dict__[attr]

	__getitem__=__getattr__





