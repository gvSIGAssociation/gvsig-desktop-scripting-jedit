# encoding: utf-8

import gvsig
from gvsig import getResource

import thread
from java.io import File
from org.gvsig.andami import PluginsLocator
from org.gvsig.app import ApplicationLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator

from addons.jedit.jedit import launchJEdit

class JEditExtension(ScriptingExtension):
  def __init__(self):
    pass

  def canQueryByAction(self):
    return False

  def isEnabled(self,action=None):
    return True

  def isVisible(self,action=None):
    return True
    
  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "jedit-launch":
      thread.start_new_thread(launchJEdit,tuple())
        
def selfRegister():
  application = ApplicationLocator.getManager()

  #
  # Registramos los iconos en el tema de iconos
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  icon = File(getResource(__file__,"images","jedit16x16.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.JEditExtension", "action", "jedit-launch", None, icon)

  #
  # Creamos la accion 
  actionManager = PluginsLocator.getActionInfoManager()
  extension = JEditExtension()
  
  action = actionManager.createAction(
    extension, 
    "jedit-launch", # Action name
    "JEdit", # Text
    "jedit-launch", # Action command
    "jedit-launch", # Icon name
    None, # Accelerator
    650700600, # Position 
    "_Show_the_JEdit_edior" # Tooltip
  )
  action = actionManager.registerAction(action)
  application.addMenu(action, "tools/JEdit")
