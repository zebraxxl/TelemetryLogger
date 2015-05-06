from matplotlib.dates import DateFormatter
from consts import TELEMETRY_CPU_PERCENT

__author__ = 'zebraxxl'

TIME_FORMATTER = DateFormatter('%H:%M:%S.%f')


def draw_single_plot(data, axes):
    times = [x[0] for x in data]
    values = [x[1] for x in data]

    axes.plot_date(times, values, '-')
    axes.xaxis.set_major_formatter(TIME_FORMATTER)


PLOT_DRAWERS = {
    TELEMETRY_CPU_PERCENT: draw_single_plot,
}
