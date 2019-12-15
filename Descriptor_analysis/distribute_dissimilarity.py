import sys
import subprocess
import os
import pickle

# cmd = "ssh -oStrictHostKeyChecking=no {} \"tmux new-session -s {} -d \\\"../project_bin {} \\\"\""
# cmd = "ls"
username = "timothee.darcet"

nodes_FN = sys.argv[1]
n = int(sys.argv[2])
m = int(sys.argv[3])


with open(nodes_FN, 'r') as nodes_F:
    for i in range(n):
        node = ""
        while node == "":
            node = nodes_F.readline()
            while node == "\n":
                node = nodes_F.readline()
            if node == "":
                nodes_F.seek(0)
        node = node.strip()
        print("Doing {}/{} on {}".format(i, n - 1, node))
        cmd = " ".join(["ssh", "-oStrictHostKeyChecking=no", username + "@" + node, "\"tmux", "new-session", "-s", "project_embeddings", "-d", "\\\"cd ~/INF574/Projet_ShapeRetrieval/ && source .venv/bin/activate && python3 ./dissimilarity_mat.py", str(i), str(n), str(m), "\\\"\""])
        print("cmd =", cmd)
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # output, error = process.communicate()
        # print(process)
        # print(process.stderr, file=sys.stderr)

