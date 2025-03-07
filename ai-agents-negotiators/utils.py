import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def plot_trace(ax, trace, color, direction='vertical', label=None):
  xs = list(range(len(trace)))
  
  trace = list(trace)

  if direction == 'horizontal':
    ax.plot(xs, trace, color=color, label=label)
  else:
    ax.plot(trace, xs, color=color, label=label)


def plot_traces(ax, traces, color, label=None, direction='vertical'):
  for i, t in enumerate(traces):
    plot_trace(ax, t, color, direction=direction, label=label if i == 0 else None)


def make_figure(direction='vertical', size=(800, 800)):
  px = 1/plt.rcParams['figure.dpi']  # pixel in inches

  w, h = size

  fig, ax = plt.subplots(1, 1, figsize=(w*px, h*px))

  if direction == 'vertical':
    ax.invert_yaxis()

    ax.set_ylabel('Negotiation step')

    ax.set_xlabel('Price')

  else:
    ax.set_xlabel('Negotiation step')

    ax.set_ylabel('Price')

  return fig, ax


COLORS = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']


def plot_multi_traces(trace_sets, labels=None, direction='vertical', delta_scatter=0.2, loc='upper right', figsize=(1400, 1100), skip_traces=False):
  matplotlib.rc('font', size=20)

  fig, ax = make_figure(direction=direction, size=figsize)

  has_legend = False

  final_values = {}

  for i, ts in enumerate(trace_sets):
    color = COLORS[i]

    for t in ts:
      v = t[-1]

      if v not in final_values:
        final_values[v] = []

      final_values[v].append(color)

  dots_base = 0

  if not skip_traces:
    max_step = max(len(trace) for traces in trace_sets for trace in traces)

    dots_base = max_step

    for i, traces in enumerate(trace_sets):
      color = COLORS[i]
      plot_traces(ax, traces, color, label=labels[i] if labels else None, direction=direction)

    ax.legend(loc=loc)

    has_legend = True

    ax.set_ylim(max_step + 0.2, -1)
  else:
    ax.set_xlim(0, 10)
    ax.set_ylim(0.25, -1.5)

  scatter_x = []
  scatter_y = []
  scatter_colors = []

  print('final_values', final_values)

  for v, colors in final_values.items():
    for i, c in enumerate(colors):
      scatter_x.append(v)
      scatter_y.append(dots_base - i * delta_scatter)
      scatter_colors.append(c)

  ax.scatter(scatter_x, scatter_y, color=scatter_colors)

  plot_min_max_prices(ax, [0, dots_base])

  if not has_legend:
    ax.legend(loc=loc, labelcolor=COLORS[:len(trace_sets)])

  plt.show()

  return fig, ax


def plot_min_max_prices(ax, ys, left_pos=0.7, right_pos=8.2):
  ax.vlines([2, 8], ys[0] - 5, ys[1] + 5, color='black', linestyle='--')

  ax.annotate('Seller\'s\nmin price', (left_pos, ys[1] - 0.5), annotation_clip=True, color='black')
  ax.annotate('Buyer\'s\nmax price', (right_pos, ys[1] - 0.5), annotation_clip=True, color='black')


def plot_example_trace(prices, texts, direction='vertical', show=True, fname=None, size=(2200, 800), max_step=None):
  matplotlib.rc('font', size=20)

  fig, ax = make_figure(direction=direction, size=size)

  n_texts = len(texts)

  original_n_texts = n_texts

  ax.set_ylim(-1, n_texts)

  ax.set_xlim(0, 24)

  ax.invert_yaxis()

  ax.autoscale(False, tight=True)

  n_texts = min(n_texts, max_step) if max_step is not None else n_texts

  prices = prices[:n_texts]

  for i in range(n_texts):
    ax.annotate(texts[i], (11.5, i), fontsize=20, annotation_clip=True, color='black', clip_on=True) 

  plot_trace(ax, prices, color='red', direction=direction)

  ax.scatter(prices, range(len(prices)), color='red')

  for i, p in enumerate(prices):
    ax.annotate(f'${p:.2f}', (p, i), fontsize=20, annotation_clip=True, color='red')

  plot_min_max_prices(ax, [0, original_n_texts], left_pos=0.1, right_pos=8.2)

  if fname is not None:
    fig.tight_layout()
    fig.savefig(fname, pad_inches=0.1)

  if show:
    plt.show()

  return fig, ax


def plot_density(trace_sets, labels=None):
  matplotlib.rc('font', size=20)
  data = [[t[-1] for t in ts] for ts in trace_sets]

  sns.kdeplot(data, fill=False, common_norm=False, palette=COLORS[:len(trace_sets)], legend=False)

  plt.legend(labels)

  plt.show()