import json
from utils import *

FNAME = 'runs.json'

# SELECTED_KEYS = None
SELECTED_KEYS = ["sw", "bwo"]
# SELECTED_KEYS = ["sw", "bw"]

LABEL_MAP = {
  'bw': 'Buyer suggests first price',
  'sw': 'Seller suggests first price',
  'bwo': 'Buyer starts negotiation without suggestion',
  'swo': 'Seller starts negotiation without suggestion'
}

EXAMPLE_RUN = [
'Buyer says: "I\'ll offer $1 for the egg."',

'Seller says: "Ten dollars."',

'Buyer says: "That\'s too high for me.  How about $2?"',

'Seller says: "Five dollars.  It\'s a very special egg."',

'Buyer says: "Hmm, $3?  What makes it so special?"',

'Seller says: "Three fifty.  It\'s organic, free-range... from a prize-winning hen."',

'Buyer says: "I\'ll offer $3.75.  Is it fresh?"',

'Seller says: "Fine.  $3.75.  EXIT"',
]

EXAMPLE_PRICES = [1, 10, 2, 5, 3, 3.50, 3.75]

with open(FNAME, 'r') as f:
  runs = json.load(f)

if SELECTED_KEYS is not None:
  runs = {k: v for k, v in runs.items() if k in SELECTED_KEYS}

keys, values = zip(*runs.items())

labels = [LABEL_MAP[k] for k in keys]

plot_multi_traces(values, labels=labels, loc='upper left')

# plot_example_trace(EXAMPLE_PRICES, EXAMPLE_RUN)

# plot_density(values, labels=labels)