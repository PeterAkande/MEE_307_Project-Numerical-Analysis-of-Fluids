import sys
from typing import List

import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# from PyQt5.QtCore import QSize, Qt
# from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, \
    QDoubleSpinBox, QGridLayout, QStackedLayout, QCheckBox

from test import get_values, GRAPH_DETAILS, FLUIDS


def get_formatted_name_for_graph(word: str) -> str:
    word = word.replace('_', ' ')

    return word.capitalize()


def get_quantity_unit(quantity: str) -> str:
    if quantity == 'heat_transfer_coefficient':
        return '(W/m2/K)'
    elif quantity == 'head_loss':
        return '(m)'
    else:
        # Frictional Factor and Reynolds number are dimensionless
        return ''
    pass


class FluidData:
    def __init__(self, name, density, shc, viscosity):
        self.name = name
        self.density = 0
        self.shc = 0
        self.viscosity = 0


matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.datas = []  # This would contain the data needed to draw the graphs
        self.current_index_for_graph = 0

        fluids_values_v_layout = QGridLayout()
        axis_h_layout = QHBoxLayout()
        self.graph_plot_layout = QStackedLayout()  # Can be a stacked layout

        # Add the contents of the fluids_values_v_layout
        # It would contain the text fields that gives room to enter the values of the fluid
        # Density, SHC and Viscosity

        number_of_rows = 5
        number_of_columns = 2

        index = 0
        for row in range(number_of_rows):
            for column in range(number_of_columns):
                fluids_values_v_layout.addWidget(self.get_entry_layout(index), row, column)

                index += 1

        btn = QPushButton('Calculate values')
        btn.clicked.connect(self.plot_graphs)
        fluids_values_v_layout.addWidget(btn)

        # Is horizontal view check #
        is_horizontal_view_check_layout = QHBoxLayout()
        self.is_horizontal_check = QCheckBox()

        self.is_horizontal_check.clicked.connect(lambda check_state: self.plot_graphs())
        is_horizontal_label = QLabel('Horizontal')

        is_horizontal_view_check_layout.addWidget(self.is_horizontal_check)
        is_horizontal_view_check_layout.addWidget(is_horizontal_label)

        is_horizontal_view_check_widget = QWidget()
        is_horizontal_view_check_widget.setLayout(is_horizontal_view_check_layout)

        fluids_values_v_layout.addWidget(is_horizontal_view_check_widget)

        # Add the contents of axis_h_layout
        # It would contain the buttons that would control the graoh that is being shown

        # Add he buttons
        f_against_reynold = QPushButton('Frictional Factor against Reynold Number')
        head_loss_against_reynold = QPushButton('Head loss against Reynold Number')
        heat_coefficient_against_reynold = QPushButton('Heat transfer Coefficient against Reynold Number')

        f_against_reynold.clicked.connect(lambda d: self.set_current_index_for_plot(2))
        head_loss_against_reynold.clicked.connect(lambda d: self.set_current_index_for_plot(0))
        heat_coefficient_against_reynold.clicked.connect(lambda d: self.set_current_index_for_plot(1))

        axis_h_layout.addWidget(head_loss_against_reynold)
        axis_h_layout.addWidget(heat_coefficient_against_reynold)
        axis_h_layout.addWidget(f_against_reynold)

        # Add the contents of the graph plot layout
        # It would contain only the graph

        self.f_against_reynolds_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.headloss_against_reynolds_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.shc_against_reynolds_plot = MplCanvas(self, width=5, height=4, dpi=100)

        self.info_label = QLabel('Please Enter values and Click on the calculate values button')
        self.graph_plot_layout.addWidget(self.info_label)

        # The
        right_side_v_layout = QVBoxLayout()  # This would occupy both the buttons to change graphs and the graph
        right_side_v_layout.addLayout(axis_h_layout)
        right_side_v_layout.addLayout(self.graph_plot_layout)

        whole_layout = QHBoxLayout()

        whole_layout.addLayout(fluids_values_v_layout)
        whole_layout.addLayout(right_side_v_layout)

        widget = QWidget()
        widget.setLayout(whole_layout)

        self.setCentralWidget(widget)

    def get_entry_layout(self, index):
        values_names = ['Density', 'SHC', 'Viscosity']
        container = QWidget()

        root_layout = QVBoxLayout()  # This is the root layout

        fluids_names_n_layout = QVBoxLayout()  # This would contain each entry layout
        fluids_names_n_layout.addWidget(QLabel(FLUIDS[index]))

        fluid_data = FluidData(name=FLUIDS[index], density=0, shc=0, viscosity=0)

        d_each_entry_layout = QHBoxLayout()
        v_each_entry_layout = QHBoxLayout()
        s_each_entry_layout = QHBoxLayout()

        d_label = QLabel('Density')
        d_edit_field = QDoubleSpinBox()
        d_edit_field.setMaximum(100000000000000000000000)
        d_edit_field.setDecimals(8)
        d_edit_field.setSuffix('  kg/m3')
        d_edit_field.valueChanged.connect(lambda d: self.edit_fluid_data(fluid_data, 'd', d))
        d_each_entry_layout.addWidget(d_label)
        d_each_entry_layout.addWidget(d_edit_field)
        fluids_names_n_layout.addLayout(d_each_entry_layout)

        ########################
        v_label = QLabel('Viscosity')
        v_edit_field = QDoubleSpinBox()
        v_edit_field.setMaximum(100000000000000000000000)
        v_edit_field.setDecimals(8)
        v_edit_field.setSuffix('  Pa.s')
        v_edit_field.valueChanged.connect(lambda d: self.edit_fluid_data(fluid_data, 'v', d))
        v_each_entry_layout.addWidget(v_label)
        v_each_entry_layout.addWidget(v_edit_field)
        fluids_names_n_layout.addLayout(v_each_entry_layout)

        ######################

        s_label = QLabel('SHC')
        s_edit_field = QDoubleSpinBox()
        s_edit_field.setMaximum(100000000000000000000000)
        s_edit_field.setDecimals(8)
        s_edit_field.setSuffix('  J/kg.K')
        s_edit_field.valueChanged.connect(lambda d: self.edit_fluid_data(fluid_data, 's', d))
        s_each_entry_layout.addWidget(s_label)
        s_each_entry_layout.addWidget(s_edit_field)
        fluids_names_n_layout.addLayout(s_each_entry_layout)

        root_layout.addLayout(fluids_names_n_layout)

        container.setLayout(root_layout)

        self.datas.append(fluid_data)

        return container

    def edit_fluid_data(self, fluid_data, quantity_type_first_letter, d):

        if quantity_type_first_letter == 'd':
            fluid_data.density = d
        elif quantity_type_first_letter == 's':
            fluid_data.shc = d
        else:
            fluid_data.viscosity = d

    def set_current_index_for_plot(self, index: int):
        self.graph_plot_layout.setCurrentIndex(index)

        self.current_index_for_graph = index

    def get_valid_fluid_data(self) -> (list, list):
        # This would return the valid data and those data would be used to plot the graph
        valid_fluid_data = []
        valid_fluid_names = []
        for data in self.datas:

            if len(data.name) == 0 or data.density <= 0 or data.shc <= 0 or data.viscosity <= 0:
                continue
            valid_fluid_data.append(data)
            valid_fluid_names.append(data.name)

        return valid_fluid_data, valid_fluid_names

    def plot_graphs(self):
        """
        This would plot the graphs for us
        """
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'pink', 'chartreuse', 'burlywood']
        fluids_data, fluids_names = self.get_valid_fluid_data()

        fluids_tables = {}

        if len(fluids_data) == 0:
            return

        self.info_label.setParent(None)

        for fluid in fluids_data:
            fluid_value = get_values(fluid.shc, fluid.viscosity,
                                     fluid.density, self.get_acceleration_due_to_gravity())
            fluids_tables[fluid.name] = fluid_value

        for row in range(len(GRAPH_DETAILS)):

            graph_detail = GRAPH_DETAILS[row]
            y_axis = graph_detail[0]
            x_axis = graph_detail[1]

            if row == 0:
                self.headloss_against_reynolds_plot.setParent(None)
                plt = self.headloss_against_reynolds_plot = MplCanvas(self, width=5, height=4, dpi=100)

            elif row == 1:
                self.shc_against_reynolds_plot.setParent(None)
                plt = self.shc_against_reynolds_plot = MplCanvas(self, width=5, height=4, dpi=100)

            else:
                self.f_against_reynolds_plot.setParent(None)
                plt = self.f_against_reynolds_plot = MplCanvas(self, width=5, height=4, dpi=100)

            # plt = MplCanvas(self, width=5, height=4, dpi=100)

            for specific_graph_number in range(len(fluids_data)):
                # Plot all the graphs on a canvas

                plt.axes.plot(fluids_tables[fluids_data[specific_graph_number].name][x_axis],
                              fluids_tables[fluids_data[specific_graph_number].name][y_axis],
                              color=colors[specific_graph_number])

            plt.axes.set_xlabel(f'{get_formatted_name_for_graph(x_axis)} {get_quantity_unit(x_axis)}')
            plt.axes.set_ylabel(f'{get_formatted_name_for_graph(y_axis)} {get_quantity_unit(y_axis)}')
            plt.axes.set_title(
                f'Graph of {get_formatted_name_for_graph(y_axis)} against {get_formatted_name_for_graph(x_axis)}')
            plt.fig.legend(fluids_names)

            self.graph_plot_layout.addWidget(plt)
        self.graph_plot_layout.setCurrentIndex(self.current_index_for_graph)

    def get_acceleration_due_to_gravity(self) -> float:
        """
        :return: This would return the acceleration due to gravity
        """

        if self.is_horizontal_check.isChecked():
            return 0.01
        return 9.81


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
