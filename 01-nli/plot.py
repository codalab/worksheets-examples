import json
import argparse
import matplotlib.pyplot as plt

# path
parser = argparse.ArgumentParser(description='NLI plotting')
parser.add_argument("--logpath", type=str, default='log.json', help="JSON log files")
params, _ = parser.parse_known_args()

# dataset assembly
with open(params.logpath, 'r') as f:
    log = json.load(f)
losses = [stats['loss'] for stats in log['log']]
accs = [stats['train_accuracy'] for stats in log['log']]

plt.figure()
plt.plot(losses)
plt.title('Training loss')

plt.figure()
plt.plot(accs)
plt.title('Training accuracy')
plt.show()
