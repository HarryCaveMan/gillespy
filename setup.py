from setuptools import setup
from setuptools.command.install import install
import os

class Install(install):
    def do_egg_install(self):
        print "Install.do_egg_install()"
        success=False
        cmd = "echo 'from .gillespy import *' > gillespy/__init__.py"
        cmd += "\necho 'import os' >> gillespy/__init__.py"
        if os.environ.get('STOCHSS_HOME') is not None:
            cmd += "\necho 'os.environ[\'PATH\'] += os.pathsep + \"{0}/StochKit/\"' >> gillespy/__init__.py".format(os.environ['STOCHSS_HOME'])
            cmd += "\necho 'os.environ[\'PATH\'] += os.pathsep + \"{0}/ode/\"' >> gillespy/__init__.py".format(os.environ['STOCHSS_HOME'])
            success=True
        if os.environ.get('STOCHKIT_HOME') is not None:
            cmd += "\necho 'os.environ[\"PATH\"] += os.pathsep + \"{0}\"' >> gillespy/__init__.py".format(os.environ['STOCHKIT_HOME'])
            success=True
        if os.environ.get('STOCHKIT_ODE_HOME') is not None:
            cmd += "\necho 'os.environ[\"PATH\"] += os.pathsep + \"{0}\"' >> gillespy/__init__.py".format(os.environ['STOCHKIT_ODE_HOME'])
            success=True
        if success is False:
           raise Exception("StochKit not found, to simulate GillesPy models either StochKit or StochSS must to be installed")
        print cmd        
        os.system(cmd)
        install.do_egg_install(self)



setup(name = "gillespy",
      version = "0.1",
      packages = ['gillespy'],
      description = 'Python interface to the Gillespie StochKit2 solvers',
      
      install_requires = ["numpy",
                          "matplotlib",
                          "scipy"],
      
      author = "John H. Abel, Brian Drawert, Andreas Hellander",
      author_email = ["jhabel01@gmail.com", "briandrawert@gmail.com", "andreas.hellander@gmail.com"],
      license = "GPL",
      keywords = "gillespy, gillespie algorithm, stochkit, stochastic simulation",

      url = "http://www.github.com/JohnAbel/GillesPy", # we don't really yet have one

      download_url = "https://github.com/JohnAbel/GillesPy/tarball/master/",
      
      cmdclass = {'install':Install}
      
      )
