
main_path = "/home/dsml01/Ultron"

continuous_variables = ['b10','b11',
                        'b12number_1','b12number_2','b12number_3_5',
                        'b12number_4','b12number_6','b12number_7_8',
                        'c1c','c4c_1',
                        'b12b_1','b12b_2']


spend_categories = ['Expenditure on Accommodation (c4.tot.new)',
                    'Expenditure on F&B (c6.tot.new)',
                    'Expenditure on Transport (c7.tot.new)',
                    'Expenditure on Sightseeing & Entertainment (c10.tot.new)',
                    'Expenditure on Shopping (t7.m.any)']
    

spend_label = ['Accommodation', 'F&B', 'Transport', 'S&E', 'Shopping']


minimum_spend = {
                 'Expenditure on Accommodation (c4.tot.new)': 10,
                 'Expenditure on F&B (c6.tot.new)': 8,
                 'Expenditure on Transport (c7.tot.new)': 5.8,
                 'Expenditure on Sightseeing & Entertainment (c10.tot.new)': 12,
                 'Expenditure on Shopping (t7.m.any)': 0.01
}