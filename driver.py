import sys
import subprocess
import os

cmd = "./project_bin"

nodes_FN = sys.argv[1]
models_path = sys.argv[2]

with open(nodes_FN, 'r') as nodes_F:
    for root, dirs, files in os.walk(models_path):
        for f in files:
            model = os.path.join(root, f)
            if model.split('.')[-1] == "obj":
                # print(model)
                # for node in nodes_F.readlines():
                node = nodes_F.readline()
                if node == "":
                    nodes_F.seek(0)
                    node = nodes_F.readline()
                print("Doing {} on {}".format(model, node))
                # process = subprocess.Popen([cmd, model[:-4]], stdout=subprocess.PIPE)
                # output, error = process.communicate()
                # print(output)
                # print(error, file=sys.stderr)

