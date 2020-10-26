import lab1_num as ln
import PySimpleGUI as sg 

sg.theme('DarkBlue14')   # Add a touch of color
# All the stuff inside your window.
def make_table(is_test_table, data):
	col_widths = [5,5,5,5,5,5,5,5]
	headers = [' № ', 'x', 'v', 'v2', 'v-v2','LE', ' h ', ' C1 ', ' C2 ', 'u', '|u-v|']
	if is_test_table:
		col_map = [1 for i in range(len(headers))]
	else:
		col_map = [1 for i in range(len(headers)-2)]
	table_data = [ [0 for col in range(len(headers))] for row in range(len(data[0]))]
	for row in range(len(data[0])):
			table_data[row][0] = '{:d}'.format(row+1) # step number
			table_data[row][1] = '{:.5f}'.format(data[0][row]) # x
			table_data[row][2] = '{:.5f}'.format(data[1][row]) # v
			table_data[row][3] = '{:.5f}'.format(data[2][row]) # v2
			table_data[row][4] = '{:.2E}'.format(data[1][row] - data[2][row]) # v-v2
			table_data[row][5] = '{:.2E}'.format(data[3][row]) #LE
			table_data[row][6] = '{:.2E}'.format(data[4][row]) # h
			table_data[row][7] = '{:d}'.format(data[5][row]) # C1
			table_data[row][8] = '{:d}'.format(data[6][row]) # C2
			if is_test_table and sum(data[5]) == 0 and sum(data[6]) == 0:
				table_data[row][9] = '{:.5f}'.format(data[len(data)-1][row]) # u if is_test
				table_data[row][10] = '{:.2E}'.format(abs(data[len(data)-1][row] - data[1][row])) # |u - v| if is_test

	layout = [
				[
				 sg.Table(values=table_data, headings=headers, auto_size_columns=True,
				 	col_widths=None, num_rows=15, vertical_scroll_only=True,
				 	visible_column_map=col_map)
				],
				[
				 sg.Button('Close', size = (6,1), font=('Avenir 15'))
				]
			]
	return layout				

top_frame_layout = [ 
	[ 
     sg.Text(' u0:'), sg.InputText('3', size = (7,1), key = 'input_y0'),
     sg.Text('Boundary:'), sg.InputText('5', size = (7,1),
     	key = 'input_rb'),
	 sg.Text("a:"), sg.InputText('', size = (7,1), key = 'input_a', disabled=True,
	 	disabled_readonly_background_color= sg.theme_background_color()),
    ],

    [sg.Text('', size=(1,1), font='Avenir 3')],

    [
     sg.Text("u'0:"), sg.InputText('', size = (7,1), key = 'input_u20', disabled=True,
		disabled_readonly_background_color= sg.theme_background_color()),
     sg.Text('', size=(2,1)),
     sg.Text(' Step:'), sg.InputText('0.1', size = (7,1), key = 'input_h'),
	 sg.Text('b:'), sg.InputText('', size = (7,1), key = 'input_b', disabled=True,
	 	disabled_readonly_background_color= sg.theme_background_color()),
    ],
  #   [
	 # sg.Text('x0:'), sg.InputText('0', size = (7,1), key = 'input_x0'),
  #   ],
    [sg.Text('', size=(1,1), font='Avenir 5')],

    [
     sg.Text('Function:'),
     sg.Radio('Test', "RADIO1", default=True, key='RTest', enable_events=True),
 	 sg.Radio('Function 1', "RADIO1", key='RFunc1', enable_events=True),
 	 sg.Radio('Function 2', "RADIO1", key='RFunc2', enable_events=True)
 	]
]

bottom_frame_layout = [ 
	[
	 sg.Checkbox('Use error control', default=False,
	 	enable_events = True, key='cbox_bool')
	],

	[
	 sg.Text('Epsilon:'), sg.InputText('', size = (7,1), disabled = True,
		 disabled_readonly_background_color= sg.theme_background_color(), key = 'input_e'),
	 sg.Text('Number of iterations:'), sg.InputText('', size = (7,1), disabled = True,
		 disabled_readonly_background_color= sg.theme_background_color(), key = 'input_N')
	] 
]

input_frame_layout = [ 
	[
     sg.Frame(layout=top_frame_layout, title = '', border_width=0),
    ],

    [
     sg.Frame(layout=bottom_frame_layout, title='Error control')
    ]
]

output_frame_layout = [[sg.Text(text="", size = (38,3),font='Avenir 17 bold', key='main_out')]]

layout_main = [  
			[
				sg.Frame(layout=input_frame_layout, title='', border_width=0)
			],

            [
             sg.Frame(layout=output_frame_layout, title='Output')
            ],

            [
             sg.Button('Exit', size = (6,1), font=('Avenir 15')),
             sg.Text('', size  = (16,1), font = ('Avenir 15')),
             sg.Button('Table', size = (6,1), font=('Avenir 15'), disabled = True),
             # sg.Button('Clear', size = (6,1), font=('Avenir 15'), disabled = True),
             sg.Button('Plot', size = (4,1), font=('Avenir 15'), disabled = True),
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

	if event == 'RFunc2':
		window_main.FindElement('input_u20').Update(disabled = False)
		window_main.FindElement('input_a').Update(disabled = False)
		window_main.FindElement('input_b').Update(disabled = False)

	if event == "RTest" or event == 'RFunc1':
		window_main.FindElement('input_u20').Update(disabled = True)
		window_main.FindElement('input_a').Update(disabled = True)
		window_main.FindElement('input_b').Update(disabled = True)


	if event == 'Table':
		window_table = sg.Window('Table', make_table(is_test_table, data), font=('Avenir 17'))
		while True:
			event_t, values_t = window_table.read()
			if event_t == sg.WIN_CLOSED or event_t == 'Close':
				break
		window_table.close()

	if event == 'Calculate':
		is_test_table = False
		# window_main.FindElement('Clear').Update(disabled = False)
		window_main.FindElement('Table').Update(disabled = True)
		window_main.FindElement('Plot').Update(disabled = True)
		window_main.FindElement('Exit').Update(disabled = True)
		#user input
		# x0 = float(values['input_x0'])
		x0 = 0;
		u0 = float(values['input_y0'])
		x_max = float(values['input_rb'])
		h = float(values['input_h'])
		Nmax = None
		e = None
		if values['cbox_bool']:
		    Nmax = float(values['input_N']) #максимальное кол-во итераций
		    e = float(values['input_e'])

		if values['RTest']:
			data = ln.func_num_sln(x0, u0, x_max, h, Nmax, e,
				ln.func_test, values['cbox_bool'])
			data += ln.test_precise_sln(x0, u0, h, x_max)
			if not values['cbox_bool']:
				Err = [(abs(data[len(data)-1][i] - data[1][i])) for i in range(len(data[1]))]
				maxErr = max(Err)
				ind_maxErr = Err.index(maxErr)
				maxErr = '{:.2E}'.format(maxErr)
				x_maxErr = '{:.2f}'.format(data[0][ind_maxErr])
				is_test_table = True

		elif values['RFunc1']:
			data = ln.func_num_sln(x0, u0, x_max, h, Nmax, e,
				ln.func_1, values['cbox_bool'])

		elif values['RFunc2']:
			u20 = float(values['input_u20'])
			a = float(values['input_a'])
			b = float(values['input_b'])
			data = ln.num_sol_3_task(a, b, Nmax, ln.f_1, ln.f_2, x0, u0, u20, x_max, h, e, values['cbox_bool'])

		n = len(data[0])
		rem = '{:.1f}'.format(x_max - data[0][len(data[0])-1])
		maxLE = '{:.2E}'.format(max(data[3]))
		main_out ="n = {};  b - x_n = {};  max|LE| = {}".format(n, rem, maxLE)

		# Adding error control output
		if values['cbox_bool']:
			maxH = max(data[4])
			minH = min(data[4])
			ind_maxH = data[4].index(maxH)
			x_maxH = '{:.2f}'.format(data[0][ind_maxH])
			ind_minH = data[4].index(minH)
			x_minH = '{:.2f}'.format(data[0][ind_minH])
			maxH = '{:.2E}'.format(maxH)
			minH = '{:.2E}'.format(minH)
			main_out+="\nmax h = {}, x = {}\nmin h = {}, x = {}".format(maxH, x_maxH, minH, x_minH)
		# Adding test finc output
		if values['RTest'] and not values['cbox_bool']:
			main_out+= "\nmax|V-U| = {}, x = {}".format(maxErr, x_maxErr)
		window_main.FindElement('main_out').Update(value = main_out)

		window_main.FindElement('Table').Update(disabled = False)
		window_main.FindElement('Plot').Update(disabled = False)
		window_main.FindElement('Exit').Update(disabled = False)

	if event == 'Plot':
		ln.draw(data, values['cbox_bool'], values['RTest'], values['RFunc2'])
		

window_main.close()