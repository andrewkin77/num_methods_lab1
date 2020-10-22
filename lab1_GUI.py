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
			if is_test_table:
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
	 sg.Text('x0:'), sg.InputText('0', size = (7,1), key = 'input_x0'),
     sg.Text('Right boundary:'), sg.InputText('5', size = (7,1),
     	key = 'input_rb'),
    ],

    [
     sg.Text('u0:'), sg.InputText('3', size = (7,1), key = 'input_y0'),
     sg.Text('Step:'), sg.InputText('0.1', size = (7,1), key = 'input_h')
    ],

    [
     sg.Text('Function:'),
     sg.Radio('Test', "RADIO1", default=True, key='RTest'),
 	 sg.Radio('Function 1', "RADIO1", key='RFunc1'),
 	 sg.Radio('Function 2', "RADIO1", key='RFunc2')
 	]
]

bottom_frame_layout = [ 
	[
	 sg.Checkbox('Use error control', default=False,
	 	enable_events = True, key='cbox_bool')
	],

	[
	 sg.Text('Max error:'), sg.InputText('', size = (7,1), disabled = True,
		 disabled_readonly_background_color= sg.theme_background_color(), key = 'input_e'),
	 sg.Text('Number of iterations:'), sg.InputText('', size = (7,1), disabled = True,
		 disabled_readonly_background_color= sg.theme_background_color(), key = 'input_N')
	] 
]

input_frame_layout = [ 
	[
     sg.Frame(layout=top_frame_layout, title = '', border_width=0)
    ],

    [
     sg.Frame(layout=bottom_frame_layout, title='Error control')
    ]
]

layout_main = [  
			[
				sg.Frame(layout=input_frame_layout, title='', border_width=0)
			],

            [
             sg.Text('', size=(1,1), font = ('Avenir 10'))
            ],

            [
             sg.Button('Exit', size = (6,1), font=('Avenir 15')),
             sg.Text('', size  = (17,1), font = ('Avenir 15')),
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

	if event == 'Table':
		window_table = sg.Window('Table', make_table(is_test_table, data), font=('Avenir 17'))
		while True:
			event_t, values_t = window_table.read()
			if event_t == sg.WIN_CLOSED or event_t == 'Close':
				break
		window_table.close()

	if event == 'Calculate':
		is_test_table = False
		window_main.FindElement('Table').Update(disabled = False)
		window_main.FindElement('Plot').Update(disabled = False)
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

		elif values['RFunc2']:
			data = ln.RK_4(1, 2, 1000, 0, 0, 5, 2, h)

	if event == 'Plot':
		ln.draw(data, values['cbox_bool'], values['RTest'])
		

window_main.close()