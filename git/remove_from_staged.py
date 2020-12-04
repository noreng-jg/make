import subprocess

def get_filenames(lines):
  search_begin='Changes to be committed:'
  search_end=''
  spacer="   "

  return [line.split(spacer)[1] for line in lines[lines.index(search_begin)+1: lines.index(search_end)][1:]]

def exec_command(files):
  for f in files:
    cmd = 'git reset HEAD {file} '.format(file=f)
    subprocess.call(cmd, shell=True)

def receive_status():
  cmd = 'git status'
  data = subprocess.check_output(cmd, shell=True)
  return data.decode('utf-8').split('\n')

if __name__ == "__main__":
  filenames = get_filenames(receive_status())
  exec_command(filenames)

