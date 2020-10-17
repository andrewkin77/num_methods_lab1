import lab1_num as ln
import PySimpleGUI as sg 

sg.theme('DarkBlue14')   # Add a touch of color
# All the stuff inside your window.
def make_table(is_test_table):
	if is_test_table:
			headers = ['x', 'v']
			table_data = [[data[j][i] for j in range(2)] for i in range(len(data[0]))]
			layout = [
						[
						 sg.Table(values=table_data, headings=headers, display_row_numbers=True, num_rows=15)
						],
						[
						 sg.Button('Exit', size = (6,1), font=('Avenir 15'))
						]
					]
	return layout				

layout_main = [  
            [
             sg.Text('x0:'), sg.InputText('0', size = (7,1), key = 'input_x0'),
             sg.Text('Right boundary:'), sg.InputText('', size = (7,1),
             	key = 'input_rb'),
            ],

            [
             sg.Text('u0:'), sg.InputText('', size = (7,1), key = 'input_y0'),
             sg.Text('Step:'), sg.InputText('', size = (7,1), key = 'input_h')
            ],

            [
             sg.Text('Function:'),
             sg.Radio('Test', "RADIO1", default=True, key='RTest'),
         	 sg.Radio('Function 1', "RADIO1", key='RFunc1'),
         	 sg.Radio('Function 2', "RADIO1", key='RFunc2')
            ],

            [sg.Checkbox('Use error control', default=False,
            	enable_events = True, key='cbox_bool')],

            [
             sg.Text('Max error:'), sg.InputText('', size = (7,1), disabled = True,
             	disabled_readonly_background_color= sg.theme_background_color(), key = 'input_e'),
             sg.Text('Number of iterations:'), sg.InputText('', size = (7,1), disabled = True,
             	disabled_readonly_background_color= sg.theme_background_color(), key = 'input_N')
            ],

            [
             sg.Button('Exit', size = (6,1), font=('Avenir 15')), 
             sg.Button('Table', size = (6,1), font=('Avenir 15'), disabled = True),
             # sg.Button('Clear', size = (6,1), font=('Avenir 15'), disabled = True),
             sg.Button('Calculate', size = (7,1), font=('Avenir 15'), bind_return_key = True)
            ] 
        ]

# Create main window
window_main = sg.Window('Lab1', layout_main, font=('Avenir 17'))
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window_main.read()
	if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
	    break

	# if event == 'Clear':
	#     ln.clear()

	if event == 'cbox_bool':
	    if values['cbox_bool']:
	        window_main.FindElement('input_e').Update(disabled = False)
	        window_main.FindElement('input_N').Update(disabled = False)
	    else:
	        window_main.FindElement('input_e').Update(disabled = True)
	        window_main.FindElement('input_N').Update(disabled = True)

	if event == 'Table':
		window_table = sg.Window('Table', make_table(is_test_table), font=('Avenir 17'))
		while True:
			event_t, values_t = window_table.read()
			if event_t == sg.WIN_CLOSED or event_t == 'Close':
				break
		window_table.close()

	if event == 'Calculate':
		window_main.FindElement('Table').Update(disabled = False)
		# window_main.FindElement('Clear').Update(disabled = False)

		#user input
		x0 = float(values['input_x0'])
		u0 = float(values['input_y0'])
		x_max = float(values['input_rb'])
		h = float(values['input_h'])
		Nmax = None
		e = None
		if values['cbox_bool']:
		    Nmax = int(values['input_N']) #максимальное кол-во итераций
		    e = float(values['input_e'])

		if values['RTest']:
			data = ln.func_num_sln(x0, u0, x_max, h, Nmax, e,
				ln.func_test, values['cbox_bool'])
			data += ln.test_precise_sln(x0, u0, h, x_max)
			is_test_table = True

		elif values['RFunc1']:
			data = ln.func_num_sln(x0, u0, x_max, h, Nmax, e,
				ln.func_1, values['cbox_bool'])
		ln.draw(data, values['cbox_bool'], values['RTest'])
		

window_main.close()