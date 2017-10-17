import time
import Tkinter as tk
import os
import re
import copy

from sub.job import Job
from sub.memory import Memory
from sub.test import TestMain

class Main(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.table = Table(self, rows=11, columns=6)
		self.table.pack(side="top", fill="x")
		self.memories  = []
		self.jobs = []
		self.tester = TestMain()

		self.table.set(0, 0, "Memory Block")
		self.table.set(0, 1, "Size")
		self.table.set(0, 2, "Current Process")
		self.table.set(0, 3, "Time")
		self.table.set(0, 4, "Size")
		self.table.set(0, 5, "Queue")
		self.read_file()

	def read_file(self):
		m_file = open('data/memory-block.txt')
		j_file = open('data/job-stream.txt')

		m_lines = m_file.readlines()[1:]
		j_lines = j_file.readlines()[1:]

		for idx, line in enumerate(m_lines):
			line = re.findall(r"[^\W\d_]+|\d+", line)
			memory = Memory(id=(idx + 1), name=str(line[0]), size=int(line[1]))
			self.memories.append(memory)

		for idx, line in enumerate(j_lines):
			line = re.findall(r"[^\W\d_]+|\d+", line)
			job = Job(id=(idx + 1), name=str(line[0]), time=int(line[1]), size=int(line[2]))
			self.jobs.append(job)

		self.tester.test_file_reading(memories=self.memories, jobs=self.jobs)






class Table(tk.Frame):
	def __init__(self, parent, rows=10, columns=2, num_button=1):
		tk.Frame.__init__(self, parent, background="#34495e")
		self._widgets = []
		self.parent = parent
		self.rows = rows
		self.columns = columns

		for row in xrange(0, rows):
			current_row = []
			for column in range(columns):
				label = tk.Label(self, text="",
								borderwidth=1, width=15, foreground="black", background="white")
				label.grid(row=row, column=column, sticky="nsew", padx=0.5, pady=0.5)
				current_row.append(label)
			self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Throughput: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Storage Utilization: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 1, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Waiting Queue Length: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 2, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Waiting Time in Queue: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 3, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Internal Fragmentation: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 4, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Internal Fragmentation: ",
						borderwidth=1, width=15, foreground="#34495e", background="#34495e", anchor="w")
		label.grid(row=rows + 5, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		button = tk.Button(self, text ="First Fit", command= lambda: self.display_results("FCFS"))
		button.grid(row=rows + 6, columnspan=2, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		button = tk.Button(self, text ="Best Fit", command= lambda: self.display_results("SJF"))
		button.grid(row=rows + 6, column=2, columnspan=2, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		button = tk.Button(self, text ="Worst Fit", command=lambda: self.display_results("SRPT"))
		button.grid(row=rows + 6, column=4, columnspan=2, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		current_row = []
		button = tk.Button(self, text ="Simulate", command= lambda: self.display_results("FCFS"))
		button.grid(row=rows + 7, columnspan=3, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		button = tk.Button(self, text ="Pause", command= lambda: self.display_results("SJF"))
		button.grid(row=rows + 7, column=3, columnspan=3, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		for column in range(columns):
			self.grid_columnconfigure(column, weight=1)

	def set(self, row, column, value, foreground="black", background="white", append=False):
		widget = self._widgets[row][column]
		if append:
			value = widget.cget("text") + "\n" + value
		widget.configure(text=value, foreground=foreground, background=background)


main = Main()
main.mainloop()
