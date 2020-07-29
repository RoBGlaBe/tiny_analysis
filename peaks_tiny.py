import numpy as np
import matplotlib.pyplot as plt
import analysis_tools as at
import tiny_analysis as ta


@ta.tiny_analysis(requires=('peaks', 'peak_classification'))
def plot_peaks(peaks,
               time_range=None,
               t_reference=None,
               peak_idx=None,
               s0_color='gray',
               s1_color='b',
               s2_color='g',
               title='',
               xlabel='t [us]',
               ylabel="Intensity [PE/ns]",
               figsize=(10, 4),
               is_log=False,
               **kwargs):
    """Plots peak waveforms in given selection.

    Arguments for decorator:
    context -- straxbra context
    run_id  -- 5-digit zero padded run-id (str)

    Arguments:
    peaks   -- Provided by decorator (ndarray)

    Keyword arguments:
    time_range -- Time range (ns: Unix timestamp) in that peaks
                  are plotted (default None, tuple)
    t_reference-- Reference time. Starttime of plotting (ns, Unix timestamp)
                  (default None, int)
    peak_idx   -- Index / Indecies or boolean array to select peaks to plot
                  (default None, int / list of ints / bool list with len of peaks)
    s0_color   -- Plot color of peaks (default 'gray')
    s1_color   -- Plot color of main S1 (default 'b')
    s2_color   -- Plot color of main S2 (default 'g')
    title      -- Title of Plot   (str)
    xlabel     -- Label of x-axis (str)
    ylabel     -- Label of y-axis (str)
    figsize    -- mpl figsize (default (10,4), tuple)
    is_log     -- Wheather or not to plot y-axis logarithmicly (default False)
    kwargs     -- Any kwargs plt.plot accepts, except color.
    """

    if time_range is None and peak_idx is None:
        raise RuntimeError('Kwarg missing. Give either time_range or peak_idx.')
    elif time_range is not None and peak_idx is not None:
        raise ValueError('Expected time_range OR peak_idx kwarg, got both.')

    if 'color' in kwargs or 'c' in kwargs:
        raise ValueError('Give plot color via s0_color, s1_color and s2_color not color or c.')

    if time_range is not None:
        endtime = peaks['time'] + peaks['length'] * peaks['dt']
        peaks = peaks[(peaks['time'] >= time_range[0]) &
                      (endtime <= time_range[1])]
    else:
        peaks = peaks[peak_idx]

    plt.figure(figsize=figsize)
    plt.axhline(0, c='k', alpha=0.2)

    for p in peaks:
        at.plot_peak(p,
                    t0=t_reference,
                    color={0: s0_color, 1: s1_color, 2: s2_color}[p['type']],
                    **kwargs)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if is_log:
        plt.ylim(0.1, None)
        plt.yscale('log')
    else:
        plt.axhline(0, c='k', alpha=0.2)

    plt.tight_layout()
