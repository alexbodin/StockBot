
####################
#
#   User interface
#   for StockBot
#   by Alexander Bodin
#
####################

import tkinter as tk
from tkinter import ttk
import time
import datetime
import web_api

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import pandas as pd
import mplfinance as mpf



def showGUI(sym):

    window = tk.Tk()
    window.title("StockBot")
    #window.wm_title("Embedding in Tk")

    notebook = ttk.Notebook(window)

    def createGraph(sym):
    
        graphframe = tk.Frame(notebook)
        
        fig = graph_data(sym)

        canvas = FigureCanvasTkAgg(fig, master=graphframe)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, graphframe)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)


        canvas.mpl_connect("key_press_event", on_key_press)

        graphframe.pack(side=tk.TOP)
        notebook.add(graphframe, text=sym)
        notebook.select(graphframe)
        



    btnframe = tk.Frame(window)

    def graphClicked():
        sym = txt.get().upper()
        try:
            end = int(time.mktime(datetime.datetime.strptime(txt3.get(), "%Y-%m-%d").timetuple()))
        except:
            end = int(time.time())
        try:
            start = int(time.mktime(datetime.datetime.strptime(txt2.get(), "%Y-%m-%d").timetuple()))
        except:
            start = end-7*24*60*60
        if (txt4.get() != 1 or
            txt4.get() != 5 or 
            txt4.get() != 15 or 
            txt4.get() != 30 or 
            txt4.get() != 60 or 
            txt4.get() != 'D' or 
            txt4.get() != 'W' or 
            txt4.get() != 'M'):
            res = txt4.get().upper()
        else:
            res = 'D'
        if (var1):
            web_api.getCandles(sym, res, start, end)
        createGraph(sym)

#regex for date
 #       text = input('Input a date (YYYY-MM-DD): ')
  #      pattern = r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])'
   #     match = re.search(pattern, text)
    #    if match:
     #       print(match.group())
      #  else:
       #     print('Wrong format')



    def _quit():
        window.quit()     # stops mainloop
        window.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate


    label = ttk.Label(btnframe, text="Stock symbol: ", width=12)
    label.grid(row=0, column=0)

    txt = tk.Entry(btnframe, width=12)
    txt.insert(0, 'TSLA')
    txt.grid(row=0, column=1)




    label2 = ttk.Label(btnframe, text="From date: ", width=12)
    label2.grid(row=1, column=0)

    txt2 = tk.Entry(btnframe, width=12)
    txt2.insert(0, '2020-01-01')
    txt2.grid(row=1, column=1)


    label3 = ttk.Label(btnframe, text="To date: ", width=12)
    label3.grid(row=2, column=0)

    txt3 = tk.Entry(btnframe, width=12)
    txt3.insert(0, '2020-01-31')
    txt3.grid(row=2, column=1)

    label4 = ttk.Label(btnframe, text="Resolution: ", width=12)
    label4.grid(row=3, column=0)

    txt4 = tk.Entry(btnframe, width=12)
    txt4.insert(0, 'D')
    txt4.grid(row=3, column=1)


    alg = 1

    radio1 = ttk.Radiobutton(btnframe, text="Algoritm 1", variable=alg, value=1)
    radio1.grid(row=4, column=0)
    radio2 = ttk.Radiobutton(btnframe, text="Algoritm 2", variable=alg, value=2)
    radio2.grid(row=5, column=0)
    radio3 = ttk.Radiobutton(btnframe, text="Algoritm 3", variable=alg, value=3)
    radio3.grid(row=6, column=0)
    radio4 = ttk.Radiobutton(btnframe, text="Algoritm 4", variable=alg, value=4)
    radio4.grid(row=7, column=0)

    var1 = True

    def dataChanged():
        pass

    check1 = ttk.Checkbutton(btnframe, text='Ladda ner data', 
	    command=dataChanged, variable=var1,
	    onvalue=True, offvalue=False)
    check1.grid(row=4, column=1)



    btn = tk.Button(btnframe, text="Graph", command=graphClicked, width=12)
    btn.grid(row=10, column=0)
    
    button = tk.Button(master=btnframe, text="Quit", command=_quit, width=12)
    button.grid(row=10, column=1)


    
    btnframe.pack(side=tk.LEFT)
    notebook.pack(side=tk.RIGHT, fill='both', expand=1)

    window.mainloop()
        

def graph_data(sym):

    #fig = mpf.figure()
    
    

    data = pd.read_csv('data/' + sym.replace(':', '_') + '.csv', index_col=0, parse_dates=True)
    #data = data.drop('Volume', axis=1) # Volume is zero anyway for this data data set
    data.index.name = 'Date'
    data.shape
    data.head(3)
    data.tail(3)

    mc = mpf.make_marketcolors(up='#44BB44', down='#BB4444',inherit=True)
    s  = mpf.make_mpf_style(
        base_mpl_style='dark_background',
        marketcolors=mc,
        facecolor='#222222',
        edgecolor='#444444',
        figcolor='#222222',
        gridcolor='#444444'
        )

    #iday = data.loc['2020-10-09 13:30':'2020-10-09 23:55',:]
    fig, ax = mpf.plot(data,
        type='candle',
        title=sym,
        mav=(7,12),
        volume=True,
        style=s,
        returnfig=True
        )
    return fig



showGUI('TSLA')

#data = pd.read_csv('data/' + 'TSLA' + '.csv', index_col=0, parse_dates=True)
#drawChart(data)

