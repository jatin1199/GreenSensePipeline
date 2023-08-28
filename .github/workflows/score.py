import os
import json
import sys

print(sys.version)

env_file = os.getenv("updatedFiles")
old_and_new_code = json.dumps(env_file)