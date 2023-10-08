from math import pi, sqrt, log
from time import sleep
from sys import stdout
import matplotlib.pyplot as plt
import numpy as np

#Permits flushing of text and makes program easier to follow
def type_out(message, new_line=True, type_time=0.025):
    for char in message:
        stdout.write(char)
        stdout.flush()
        sleep(type_time)

    if new_line == True:
        print()

def calc_min_stem_dia(body_weight, canal_diameter, femoral_head_offset, ult_ten_strength):
    min_stem_dia = 0
    app_ten_stress = ult_ten_strength + 1
    stem_dia_increment = 0.1

    while ult_ten_strength < app_ten_stress:
        min_stem_dia += stem_dia_increment
        app_ten_stress = 104*body_weight*femoral_head_offset/(pi*min_stem_dia**3)+(13*body_weight/(pi*min_stem_dia**2))

    type_out(f'\nBody Weight:{body_weight: .1f} N')
    type_out(f'Canal Diameter:{canal_diameter: .1f} mm')
    type_out(f'Ultimate Tensile Strength:{ult_ten_strength: .1f} MPa')
    type_out(f'Minimum Stem Diameter:{min_stem_dia: .1f} mm')
    type_out(f'Applied Tensile Stress:{app_ten_stress: .1f} MPa')

    sleep(1)

    response_vailidity = False
    while response_vailidity == False:
        type_out('Would you like to view the relationship between applied tensile stress and stem diameter graphically? (Y/N): ', False)
        graph_resp = input()
        if graph_resp.lower() in ['y', 'yes', 'yes.', 'ye', 'ya', 'yep', 'true', '1']:
            response_vailidity = True

            ult_ten_strength_wrt_dia, app_ten_stress_wrt_dia, diameters_calculated = [], [], []

            for diameter in range(1, int(min_stem_dia*2)):
                diameters_calculated.append(diameter)
                app_ten_stress_wrt_dia.append(104*body_weight*femoral_head_offset/(pi*diameter**3)+(13*body_weight/(pi*diameter**2)))
                ult_ten_strength_wrt_dia.append(ult_ten_strength)

            plt.title('Applied Tensile Stress of Implant with Respect to its Diameter', fontsize=14)
            plt.xlabel('Stem Diameter (mm)', fontsize=10)
            plt.ylabel('Pressure (log(MPa))', fontsize=10)
            plt.plot(diameters_calculated, app_ten_stress_wrt_dia, label='Applied Tensile Stress')
            plt.plot(diameters_calculated, ult_ten_strength_wrt_dia, label='Ultimate Tensile Strength', linestyle='dotted')
            plt.plot(min_stem_dia, app_ten_stress, 'go', label='PROJECTED FAILURE')
            plt.yscale('log')
            plt.grid(True)
            plt.legend()
            print('\tPress ENTER to continue once you close the window of the graph.', end=' ')
            plt.show()
            input()

        elif graph_resp.lower() in ['n', 'no', 'nah', 'na', 'false', '0']:
            response_vailidity = True
        else:
            type_out(f'Sorry, I could not understand "{graph_resp}". Please enter "Y" or "N".')

def calc_fatigue_life(team_number, body_weight, stem_dia, txt_file_str):
    unadj_stress_amp = 40*body_weight/(pi*stem_dia**2)
    txt_file = open(txt_file_str, 'r')
    sn_rows = txt_file.readlines()

    stress_col = float(sn_rows[0].split('\t')[0])
    cycles_fail = float(sn_rows[0].strip('\n').split('\t')[1])
    stress_fail = float((9.25+log(cycles_fail,10)**(0.65*team_number/40))*unadj_stress_amp)

    row_index = 0
    while stress_col > stress_fail:
        row_index += 1
        try:
            stress_col = float(sn_rows[row_index].strip('\n').split('\t')[0])
            cycles_fail = float(sn_rows[row_index].strip('\n').split('\t')[1])
            stress_fail = float((9.25+log(cycles_fail,10)**(0.65*team_number/40))*unadj_stress_amp)
        except IndexError:
            type_out(f'The implant does not fail, even at the maximum cyclical load! The maximum given number of cycles was {int(cycles_fail)}.')
            return

    if row_index == 0:
        type_out(f'The implant fails on all cyclical loads given. The minimum given number of cycles was {int(cycles_fail)}.')
    else:
        type_out(f'Stress at Failure:{stress_fail: .2f} MPa')
        type_out(f'Cycles at Failure:{cycles_fail: .0f} cycles')

    txt_file.close()

def calc_implant_longevity(body_weight, outer_dia, canal_diameter, modulus_bone, modulus_implant):
    stress_reduc = ((112*body_weight)/(pi*(outer_dia**2-canal_diameter**2)))*((4*modulus_bone)/(modulus_bone+modulus_implant))**(1/3)
    E_ratio = sqrt(modulus_implant / modulus_bone)

    yrs_fail = -1
    comp_strength = stress_reduc + 1
    while comp_strength > stress_reduc:
        yrs_fail += 1
        comp_strength = 0.0012*yrs_fail**2 - 3.725*E_ratio*yrs_fail + 186.42
        type_out(f'Year {yrs_fail}:{comp_strength: .1f} MPa', True, 0.001)

    stress_fail = comp_strength
    sleep(1.75)
    type_out(f'\nYears Until Failure: {yrs_fail} years')
    type_out(f'Stress at Failure:{stress_fail: .1f} MPa')
    sleep(1)

    response_vailidity = False
    while response_vailidity == False:
        type_out('Would you like to view the relationship between implant strength and time graphically? (Y/N): ', False)
        graph_resp = input()
        if graph_resp.lower() in ['y', 'yes', 'yes.', 'ye', 'ya', 'yep', 'true', '1']:
            response_vailidity = True

            comp_strength_time, stress_reduc_time, years_elapsed = [], [], []

            for year in range(1, yrs_fail*2):
                years_elapsed.append(year)
                comp_strength_time.append(0.0012*year**2 - 3.725*E_ratio*year + 186.42)
                stress_reduc_time.append(stress_reduc)

            plt.title('Compressive Strength of Implant with Respect to Time', fontsize=14)
            plt.xlabel('Years Post-Implant', fontsize=10)
            plt.ylabel('Pressure (MPa)', fontsize=10)
            plt.plot(years_elapsed, comp_strength_time, label='Compressive Strength of Implant')
            plt.plot(years_elapsed, stress_reduc_time, label='Initial Reduced Stress', linestyle='dotted')
            plt.plot(yrs_fail, stress_fail, 'go', label='PROJECTED FAILURE')
            plt.axis(xmin=0, ymin=0)
            plt.grid(True)
            plt.legend()
            print('\tPress ENTER to continue once you close the window of the graph.', end=' ')
            plt.show()
            input()

        elif graph_resp.lower() in ['n', 'no', 'nah', 'na', 'false', '0']:
            response_vailidity = True
        else:
            type_out(f'Sorry, I could not understand "{graph_resp}". Please enter "Y" or "N".')

def main():
    #Change all
    team_number = 17
    body_weight = 51.5*9.8
    outer_dia = 22
    canal_diameter = 11.5
    femoral_head_offset = 32
    modulus_bone = 10 #Google, change, reference
    ult_ten_strength = 150 #Change this and add reference
    modulus_implant = 10 #Google, change, reference
    stem_dia = 8 #Change
    txt_file_str = 'SN Data - Sample Fiber-Reinforced Composite.txt' #Change directory when submitting

    while True:
        type_out('\n--PROGRAM MENU--\n1. Subprogram 1\n2. Subprogram 2\n3. Subprogram 3\n4. Exit Program\n')
        sleep(1)
        type_out('Enter the number beside which program would you like to choose: ', False)
        subprogram_choice = input()
        try:
            if subprogram_choice.isdigit() == True and int(subprogram_choice) >= 1 and int(subprogram_choice) <= 4:
                if int(subprogram_choice) == 1:
                    calc_min_stem_dia(body_weight, canal_diameter, femoral_head_offset, ult_ten_strength)
                    sleep(2)
                elif int(subprogram_choice) == 2:
                    calc_fatigue_life(team_number, body_weight, stem_dia, txt_file_str)
                    sleep(2)
                elif int(subprogram_choice) == 3:
                    calc_implant_longevity(body_weight, outer_dia, canal_diameter, modulus_bone, modulus_implant)
                    sleep(2)
                elif int(subprogram_choice) == 4:
                    break
            else:
                raise ValueError
        except ValueError:
            type_out('Sorry, the value you entered is invalid. Please enter an integer between 1 and 4.')

main()