import sys
import subprocess
import os

# cmd = "ssh -oStrictHostKeyChecking=no {} \"tmux new-session -s {} -d \\\"../project_bin {} \\\"\""
# cmd = "ls"
username = "timothee.darcet"

nodes_FN = sys.argv[1]
models_path = sys.argv[2]

with open(nodes_FN, 'r') as nodes_F:
    for root, dirs, files in os.walk(models_path):
        for f in files:
            model = os.path.join(root, f)
            if model.split('.')[-1] == "obj":
                # print(model)
                # for node in nodes_F.readlines():
                node = ""
                while node == "":
                    node = nodes_F.readline()
                    while node == "\n":
                        node = nodes_F.readline()
                    if node == "":
                        nodes_F.seek(0)
                node = node.strip()
                print("Doing {} on {}".format(model, node))
                process = subprocess.Popen(" ".join(["ssh", "-oStrictHostKeyChecking=no", username + "@" + node, '"tmux', "new-session", "-s", "project_embeddings", "-d", '\"../project_bin', model, '\""']), stdout=subprocess.PIPE)
                output, error = process.communicate()
                print(output)
                print(error, file=sys.stderr)

