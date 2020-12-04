import re

def extract_ids_from_bytes_stdout(bytes):
  ids = []
  for occ in str(bytes).split('\n\t\t')[1:]:
    il, ir = re.compile(r'".*"').search(occ).span()
    temp = occ[il:ir]
    ids.append(temp[1:len(temp)-1])
  return ids

