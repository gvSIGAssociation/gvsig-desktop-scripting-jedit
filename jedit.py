# encoding: utf-8

import gvsig
from gvsig import getResource

import thread
import os.path
import subprocess
import shutil

from java.lang import System
from java.io import File
from java.io import FileInputStream
from java.io import FileOutputStream
from java.util import Properties

from org.apache.commons.io import FileUtils
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.scripting.swing.api import ScriptingSwingLocator, JScriptingComposer
from org.gvsig.tools import ToolsLocator

import javax.swing.ImageIcon
import javax.imageio.ImageIO
from javax.swing import AbstractAction, Action
from org.gvsig.scripting import ScriptingLocator

def getDataFolder():
  return ScriptingLocator.getManager().getDataFolder("jedit").getAbsolutePath()

def launchJEdit():
  pluginsManager = PluginsLocator.getManager()
  appfolder = pluginsManager.getApplicationFolder().getAbsolutePath()
  
  java = os.path.join( System.getProperties().getProperty("java.home"), "bin", "java")

  jeditInstallDir = getResource(__file__, "app").replace("\\","/")
  jeditProfileDir = getDataFolder().replace("\\","/")

  CP = "" #jeditInstallDir+"/jedit.jar"
  for fname in os.listdir(jeditInstallDir+"/jars"):
    CP += ":"+jeditInstallDir+"/lib/"+fname
 
  cmd = [
    java,
    "-cp",CP,
    "-splash:"+getResource(__file__, "images","jedit-splash"),
    "-Duser.home="+jeditProfileDir,
    "-jar",
    jeditInstallDir+"/jedit.jar",
    "-settings="+jeditProfileDir,
  ]
  #print cmd
  subprocess.call(cmd)


class JEditAction(AbstractAction):

  def __init__(self):
    AbstractAction.__init__(self,"JEdit")
    self.putValue(Action.ACTION_COMMAND_KEY, "JEdit");
    self.putValue(Action.SMALL_ICON, self.load_icon(getResource(__file__,"images","jedit16x16.png")));
    self.putValue(Action.SHORT_DESCRIPTION, "JEdit");

  def load_icon(self, afile):
    if not isinstance(afile,File):
      afile = File(str(afile))
    return javax.swing.ImageIcon(javax.imageio.ImageIO.read(afile))

  def actionPerformed(self,e):
    composer = e.getSource().getContext()
    thread.start_new_thread(launchJEdit,tuple())

def selfRegister():
  i18nManager = ToolsLocator.getI18nManager()
  manager = ScriptingSwingLocator.getUIManager()
  action = JEditAction()
  manager.addComposerTool(action)
  manager.addComposerMenu(i18nManager.getTranslation("Tools"),action)

def main(*args):
  thread.start_new_thread(launchJEdit,tuple())
