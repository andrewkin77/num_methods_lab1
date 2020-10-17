import lab1_num as ln
import PySimpleGUI as sg 
def main():
	sg.theme('DarkBlue14')   # Add a touch of color
	# All the stuff inside your window.
	layout = [  
	            [
	             sg.Text('x0:'), sg.InputText('0', size = (7,1), key = 'input_x0'),
	             sg.Text('Right boundary:'), sg.InputText('', size = (7,1), key = 'input_rb'),
	            ],

	            [
	             sg.Text('y0:'), sg.InputText('', size = (7,1), key = 'input_y0'),
	             sg.Text('Step:'), sg.InputText('', size = (7,1), key = 'input_h')
	            ],

	            [
	             sg.Text('Choose function:'),
	             sg.Combo(['Test', 'Function 1'], font = 'Avenir 15', default_value='Test', size=(20, 1), key = 'input_func')
	            ],

	            [sg.Checkbox('Use error control', default=False, enable_events = True, key='cbox_bool')],

	            [
	             sg.Text('Max error:'), sg.InputText('', size = (7,1), disabled = True,
	             disabled_readonly_background_color= sg.theme_background_color(), key = 'input_e'),
	             sg.Text('Number of iterations:'), sg.InputText('', size = (7,1), disabled = True,
	              disabled_readonly_background_color= sg.theme_background_color(), key = 'input_N')
	            ],

	            [
	            sg.Button('Exit', size = (6,1), font=('Avenir 15')), 
	             #sg.Button('Clear', size = (6,1), font=('Avenir 15')),
	             sg.Button('Plot', size = (6,1), font=('Avenir 15'), bind_return_key = True)
	            ] 
	        ]

	# Create the Window
	window = sg.Window('Lab1', layout, font=('Avenir 20'))
	# Event Loop to process "events" and get the "values" of the inputs
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
		    break

		# if event == 'Clear':
		#     plt.clf()

		if event == 'cbox_bool':
		    if values['cbox_bool']:
		        window.FindElement('input_e').Update(disabled = False)
		        window.FindElement('input_N').Update(disabled = False)
		    else:
		        window.FindElement('input_e').Update(disabled = True)
		        window.FindElement('input_N').Update(disabled = True)

		if event == 'Plot':

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

			if values['input_func'] == 'Test' :
				data = ln.func_num_sln(x0, u0, x_max, h, Nmax, e, ln.func_test, values['cbox_bool'])
				data += ln.test_precise_sln(x0, u0, h, x_max)

			elif values['input_func'] == 'Function 1':
				data = ln.func_num_sln(x0, u0, x_max, h, Nmax, e, ln.func_1, values['cbox_bool'])

			ln.draw(data, values['cbox_bool'], values['input_func'])
			

	window.close()

if __name__ == '__main__':
	main()