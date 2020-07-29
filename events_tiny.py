import numpy as np
import matplotlib.pyplot as plt
import analysis_tools as at
import tiny_analysis as ta

@ta.tiny_analysis(requires=('events', 'event_basics',
                         'peaks'))
def event_waveform(events,
                   peaks,
                   event_nr=0,
                   xlabel='t since first peak [us]',
                   ylabel='area / ns [PE]',
                   title='',
                   peak_color='gray',
                   s1_color='b',
                   s2_color='g',
                   max_time=None,
                   is_log=False,
                   figsize=(10, 4),
                   **kwargs):
    """Plots peak waveforms of given event.

    Arguments for decorator:
    context -- straxbra context
    run_id  -- 5-digit zero padded run-id (str)


    Arguments:
    events  -- Provided by decorator (DataFrame)
    peaks   -- Provided by decorator (ndarray)

    Keyword arguments:
    event_nr   -- Index of event to plot (default 0, int)
    xlabel     -- Label of x-axis (str)
    ylabel     -- Label of y-axis (str)
    title      -- Title of Plot   (str)
    peak_color -- Plot color of peaks (default 'gray')
    s1_color   -- Plot color of main S1 (default 'b')
    s2_color   -- Plot color of main S2 (default 'g')
    max_time   -- Time in ns relative to first peaks start time
                  after which peaks are not plotted (int)
    is_log     -- Wheather or not to plot y-axis logarithmicly (default False)
    figsize    -- mpl figsize (tuple)
    kwargs     -- Any kwargs plt.plot accepts, except color.
    """

    if 'color' in kwargs or 'c' in kwargs:
        raise ValueError('Give plot color via peak_color, s1_color and s2_color not color or c.')

    event = events.iloc[event_nr]
    peaks = peaks[(peaks['time'] >= event['time']) & (peaks['time'] < event['endtime'])]

    if max_time is not None:
        peaks = peaks[peaks['time'] <= peaks[0]['time'] + max_time]

    colors = {event['s1_index']: s1_color,
              event['s2_index']: s2_color}

    plt.figure(figsize=figsize)
    for idx, peak in enumerate(peaks):
        color = peak_color if idx not in colors else colors[idx]
        at.plot_peak(peak, t0=peaks[0]['time'], color=color, **kwargs)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if is_log:
        plt.ylim(0.1, None)
        plt.yscale('log')
    else:
        plt.axhline(0, c='k', alpha=0.2)

    plt.tight_layout()
