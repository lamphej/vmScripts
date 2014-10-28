"""resolution_set

Usage:
  resolution_set.py <vmxpath> <X> <Y>

  vmxpath: "[datastore2] Server 2012 Essentials/Server 2012 Essentials.vmx"
  environment variables: ESXI_HOST, ESXI_USER, ESXI_PASS
"""
from docopt import docopt
import paramiko
from os import environ as os_env

if __name__ == "__main__":
    arguments = docopt(__doc__, version='resolution_set')

    x_res = int(arguments["<X>"])
    y_res = int(arguments["<Y>"])
    vRamSize = x_res * y_res * 4

    vmx_path = arguments["<vmxpath>"]
    config_dir = "/vmfs/volumes/" + vmx_path.split('[')[1].split(']')[0].lower() + "/"
    config_dir += vmx_path.split('] ')[1].split('/')[0]
    config_file = vmx_path.split('/')[-1]
    print "[+] Editing '%s' via ssh" % config_file
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(os_env['ESXI_HOST'], username=os_env['ESXI_USER'], password=os_env['ESXI_PASS'])
    commands = [
        "cd %s" % config_dir,
        "echo %s >> %s" % ('svga.autodetect = "FALSE"', config_file),
        "echo %s >> %s" % ('svga.vramSize = %s' % vRamSize, config_file),
        "echo %s >> %s" % ('svga.maxWidth = %s' % x_res, config_file),
        "echo %s >> %s" % ('svga.maxHeight = %s' % y_res, config_file)
    ]
    #paramiko doesn't "save state", so you can't cd in one command,
    #then expect to use the files from that dir in the next one
    full_command = '; '.join(commands)
    ssh.exec_command(full_command)
    print "[+] All Done"