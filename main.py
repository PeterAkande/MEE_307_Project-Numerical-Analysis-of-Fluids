import math
import matplotlib.pyplot as plt

ACCELERATION_DUE_GRAVITY = 9.81
VELOCITY = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
DIAMETERS = [0.00159, 0.00318, 0.00477, 0.00636, 0.00795, 0.00954, 0.01113, 0.01272, 0.01431, 0.0159]
LENGTHS = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
PIPE_ROUGHNESS = 0.03
THERMAL_CONDUCTIVITY = 401


def calculate_reynolds_number(density: float, diameter: float, velocity: float, dynamic_viscosity: float) -> float:
    # This function calculates the reynolds number

    reynolds_number = (density * diameter * velocity) / dynamic_viscosity

    return reynolds_number


def calculate_frictional_factor_for_laminar_flow(reynold_number: float) -> float:
    return 64 / reynold_number


def calculate_frictional_factor_for_turbulent(reynold_number: float, pipe_roughness: float, diameter: float) -> float:
    return 2 * ((8 / reynold_number) ** 12 + (
            (2.457 * math.log((0.27 * pipe_roughness / diameter) + (7 / reynold_number) ** 0.9)) ** 16 + (
            37530 / reynold_number) ** 16) ** (-3 / 2)) ** (
                   1 / 12)


def get_frictional_factor(reynold_number: float, pipe_roughness: float, is_laminar: bool, diameter: float) -> float:
    if is_laminar:
        frictional_factor = calculate_frictional_factor_for_laminar_flow(reynold_number)
    else:
        frictional_factor = calculate_frictional_factor_for_turbulent(reynold_number=reynold_number,
                                                                      pipe_roughness=pipe_roughness, diameter=diameter)

    return frictional_factor


def calculate_head_loss(friction_factor: float, pipe_length: float, diameter: float, velocity: float):
    head_loss = (friction_factor * pipe_length * velocity ** 2) / (diameter * 2 * ACCELERATION_DUE_GRAVITY)
    return head_loss


def calculate_prandtl_number(dynamic_viscosity: float, specific_heat_capacity: float, conductivity: float) -> float:
    prandtl_number = (dynamic_viscosity * specific_heat_capacity) / conductivity

    return prandtl_number


def calculate_pressure(density: float, head_loss: float) -> float:
    return -density * ACCELERATION_DUE_GRAVITY * head_loss


def calculate_coefficient_of_heat_transfer(reynold_number: float, diameter: float, prandtl_number: float,
                                           conductivity: float) -> float:
    return 0.023 * (reynold_number ** 0.8) * (prandtl_number ** 0.4) * conductivity / diameter


def get_values() -> dict:
    # This function gets the various values and does the operation for each fluid

    reynolds_number_values = []  # This list would store the reynold number for the fluid in what ever case
    head_loss_values = []  # This list would store the head loss for the fluid in varuous cases
    coefficient_of_heat_transfer_values = []
    pressure_values = []

    # Get the values that would be used for all fluids
    specific_heat_capacity = float(input('Enter specific heat capacity: '))
    dynamic_viscosity = float(input('Enter the dynamic viscosity: '))
    density = float(input('Enter the density of the fluid: '))

    for length, diameter, velocity in zip(LENGTHS, DIAMETERS, VELOCITY):
        # Calculate the reynold's number.
        reynold_number = calculate_reynolds_number(diameter=diameter, density=density, velocity=velocity,
                                                   dynamic_viscosity=dynamic_viscosity)

        # Get if the fluid is laminar or not
        is_laminar = reynold_number < 2000

        # Get the prandtl number
        prandtl_number = calculate_prandtl_number(specific_heat_capacity=specific_heat_capacity,
                                                  conductivity=THERMAL_CONDUCTIVITY,
                                                  dynamic_viscosity=dynamic_viscosity)

        # Get the frictional factor
        frictional_factor = get_frictional_factor(reynold_number=reynold_number, pipe_roughness=PIPE_ROUGHNESS,
                                                  is_laminar=is_laminar, diameter=diameter)

        # Get the head loss
        head_loss = calculate_head_loss(friction_factor=frictional_factor, pipe_length=length, diameter=diameter,
                                        velocity=velocity)

        # Get the pressure
        pressure = calculate_pressure(density=density, head_loss=head_loss)

        # Get the coefficient of heat transfer.
        coefficient_of_heat_transfer = calculate_coefficient_of_heat_transfer(reynold_number=reynold_number,
                                                                              diameter=diameter,
                                                                              prandtl_number=prandtl_number,
                                                                              conductivity=THERMAL_CONDUCTIVITY)

        pressure_values.append(pressure)
        coefficient_of_heat_transfer_values.append(coefficient_of_heat_transfer)
        head_loss_values.append(head_loss)
        reynolds_number_values.append(reynold_number)

    return {
        'head_loss': head_loss_values,
        'pressure_loss': pressure_values,
        'heat_transfer_coefficient': coefficient_of_heat_transfer_values,
        'reynolds_number': reynolds_number_values,
        'velocity': VELOCITY,
        'diameter': DIAMETERS,
    }


def plot_graph(x: list, y: list, x_axis_label, y_axis_label, plot_title):
    plt.plot(x, y, color='r')
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    # setting the title of the plot
    plt.title(plot_title)
    plt.show()


# sub plots
def add_subplot_graph(axis, row: int, col: int, x: list, y: list, x_axis_label: str, y_axis_label: str,
                      plot_title: str, color: str):
    axis[row, col].plot(x, y, color=color)
    axis.set_title(plot_title)

    axis.xlabel(x_axis_label)
    axis.ylabel(y_axis_label)


if __name__ == '__main__':
    # Run some code

    # fluids = ['castor_oil', 'linseed oil', 'aqua ammonia']
    fluids = ['Propane', 'R134a', 'R600a', 'R407c']
    fluids_values = {

    }

    for fluid in fluids:
        print(f'<------------Calculating for {fluid}-------------->')
        fluid_value = get_values()
        fluids_values[fluid] = fluid_value

    print('Plotting graphs >>>>>>>>>>>> Loading >>>>>>>>>>>>>>>>>>>')
    # plot_graph(y=castor_oil_reynolds_number, x=DIAMETERS, x_axis_label='Diameter', y_axis_label='Reynolds Number',
    #            plot_title='Plot of The Reynolds Number against the Diameter')

    graphs_details = [['head_loss', 'reynolds_number'], ['heat_transfer_coefficient', 'reynolds_number'],
                      ['pressure_loss', 'reynolds_number'], ['reynolds_number', 'diameter'],
                      ['reynolds_number', 'velocity']]

    colors = ['r', 'g', 'b', 'c']

    for row in range(len(graphs_details)):

        graph_detail = graphs_details[row]
        y_axis = graph_detail[0]
        x_axis = graph_detail[1]

        fluid_one_y_values = fluids_values[fluids[0]][y_axis]
        fluid_one_x_values = fluids_values[fluids[0]][x_axis]

        fluid_two_y_values = fluids_values[fluids[1]][y_axis]
        fluid_two_x_values = fluids_values[fluids[1]][x_axis]

        fluid_three_y_values = fluids_values[fluids[2]][y_axis]
        fluid_three_x_values = fluids_values[fluids[2]][x_axis]

        fluid_four_y_values = fluids_values[fluids[3]][y_axis]
        fluid_four_x_value = fluids_values[fluids[3]][x_axis]

        x_values = [fluid_one_x_values, fluid_two_x_values, fluid_three_x_values, fluid_four_x_value]
        y_values = [fluid_one_y_values, fluid_two_y_values, fluid_three_y_values, fluid_four_y_values]

        # x_values = [castor_oil_x_values, linseed_oil_x_values, aqua_ammonia_x_value]
        # y_values = [castor_oil_y_values, linseed_oil_y_values, aqua_ammonia_y_value]

        for specific_graph_number in range(len(fluids)):
            plt.plot(x_values[specific_graph_number], y_values[specific_graph_number],
                     color=colors[specific_graph_number])

        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(f'graph of {y_axis} against {x_axis}')
        plt.legend(fluids)
        # plt.legend(['Castor Oil', 'Linseed Oil','Aqua Ammonia'])
        plt.show()
