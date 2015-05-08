import matplotlib
matplotlib.use('gtk3agg')

from gi.repository import Gtk
from matplotlib import pyplot
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from telemetry_logger.localization import get_string, TELEMETRY_STRING, PROCESSES_STRING
from telemetry_logger.viewer.plot_drawers import PLOT_DRAWERS


__author__ = 'zebraxxl'


class ViewerWindow:
    def __draw_plot(self, telemetry_name, telemetry_data):
        figure = pyplot.figure()
        axes, lines, labels = PLOT_DRAWERS[telemetry_name](telemetry_data, figure)

        y_lim = 0.0
        for a in axes:
            a.grid(True, color='0.35')
            y_lim = max(y_lim, a.get_ylim()[1])

        for m in self.markers:
            pyplot.axvline(m[0], color='0.75')
            pyplot.text(m[0], y_lim, m[1], rotation=-90, va='top')

        figure.tight_layout(pad=0)
        if labels is not None:
            figure.legend(lines, labels, 'upper right')

        canvas = FigureCanvas(figure)
        canvas.show()

        last_child = self.plot_holder.get_child()
        if last_child:
            self.plot_holder.remove(last_child)

        toolbar = NavigationToolbar(canvas, self.main_window)

        vbox = Gtk.VBox()
        vbox.pack_start(canvas, True, True, 0)
        vbox.pack_start(toolbar, False, False, 0)
        vbox.set_visible(True)

        self.plot_holder.add(vbox)

    def __on_tree_selection_changed(self, selection):
        model, tree_iterator = selection.get_selected()
        if tree_iterator is not None:
            telemetry_name = model[tree_iterator][1]
            telemetry_data = model[tree_iterator][2]
            if telemetry_name and telemetry_data:
                if telemetry_name in PLOT_DRAWERS:
                    self.__draw_plot(telemetry_name, telemetry_data)

    def __on_main_window_close(self, *args, **kwargs):
        pyplot.close()
        Gtk.main_quit(*args, **kwargs)

    def __init__(self, settings, telemetries, processes, markers):
        self.viewer_signals = {
            'onDeleteWindow': self.__on_main_window_close,
            'onMainTreeSelectionChanged': self.__on_tree_selection_changed,
        }
        self.markers = markers

        builder = Gtk.Builder()
        builder.add_from_file('telemetry_logger/viewer/ui.glade')
        builder.connect_signals(self.viewer_signals)

        self.main_window = builder.get_object('MainWindow')
        self.main_tree = builder.get_object('MainTree')
        self.tree_store = builder.get_object('MainTreeStore')
        self.plot_holder = builder.get_object('GraphViewport')

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("text", renderer, text=0)
        self.main_tree.append_column(column)

        telemetry_iter = self.tree_store.append(None, [get_string(TELEMETRY_STRING), None, None])
        for k in telemetries:
            self.tree_store.append(telemetry_iter, [get_string(k), k, telemetries[k]])
        processes_iter = self.tree_store.append(None, [get_string(PROCESSES_STRING), None, None])
        for process_group in processes:
            process_group_iter = self.tree_store.append(processes_iter, [process_group, None, None])
            for pid in processes[process_group]:
                pid_iter = self.tree_store.append(process_group_iter, [str(pid), None, None])    # TODO: ProcessInfo
                for k in processes[process_group][pid][1]:
                    self.tree_store.append(pid_iter, [get_string(k), k, processes[process_group][pid][1][k]])

        matplotlib.rc('font', family='Droid Sans')

    def show(self):
        self.main_window.show_all()
        Gtk.main()
