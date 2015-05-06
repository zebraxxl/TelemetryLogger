import matplotlib
matplotlib.use('gtk3agg')

from gi.repository import Gtk
from matplotlib import pyplot
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from numpy import arange, sin, pi
from telemetry_logger.localization import get_string, TELEMETRY_STRING, PROCESSES_STRING


__author__ = 'zebraxxl'


class ViewerWindow:
    def on_tree_selection_changed(self, selection):
        model, tree_iterator = selection.get_selected()
        if tree_iterator is not None:
            telemetry_name = model[tree_iterator][1]
            telemetry_data = model[tree_iterator][2]
            if telemetry_name and telemetry_data:
                # Temp code for testing
                figure, plot = pyplot.subplots()
                t = arange(0.0, 3.0, 0.01)
                s = sin(2*pi*t)
                plot.plot(t, s)

                canvas = FigureCanvas(figure)
                canvas.set_visible(True)

                last_child = self.plot_holder.get_child()
                if last_child:
                    self.plot_holder.remove(last_child)
                self.plot_holder.add(canvas)

    def __init__(self, settings, telemetries, processes, markers):
        self.viewer_signals = {
            'onDeleteWindow': Gtk.main_quit,
            'onMainTreeSelectionChanged': self.on_tree_selection_changed,
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

    def show(self):
        self.main_window.show_all()
        Gtk.main()