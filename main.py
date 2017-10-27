import time
import Tkinter as tk
import os
import re
import copy

from sub.job import Job
from sub.memory import Memory
from sub.test import TestMain

class Main(tk.Tk):
	def __init__(self, algo_type="F", header_idx=1):
		tk.Tk.__init__(self)
		headers = ["First-Fit Algorithm", "Best-Fit Algorithm", "Worst-Fit Algorithm"]
		self.title(headers[header_idx - 1])
		self.table = Table(self, rows=26, columns=6)
		self.table.pack(side="top", fill="x")
		self.memories  = []
		self.jobs = []
		self.free_list = []
		self.qualified_jobs = []
		self.occupied = []
		self.allocated = []
		self.max_time = 0
		self.counter = 0
		self.algo_type = algo_type
		self.by_second = True
		self.max_memory = 0
		self.min_memory = 0
		self.runner = None
		self.finished = 0
		self.throughput = 0
		self.count_throughput = 0
		self.storage = 0
		self.count_storage = 0
		self.total_storage = 0
		self.free_list_size = 0
		self.queue_length = 0
		self.qualified_jobs_count = 0
		self.count_queue_length = 0
		self.total_queue_length = 0
		self.tester = TestMain()
		self.total_frag = 0
		self.table.set(0, 0, "Memory Block")
		self.table.set(0, 1, "Current Process")
		self.table.set(0, 2, "Time")
		self.table.set(0, 3, "Fragmentation")
		self.table.set(0, 4, "Job Stream")
		self.table.set(0, 5, "Waiting Time")
		self.read_file()
		self.display_memory_blocks()
		self.display_job_streams()
		self.display_job_waiting_time()
		self.display_memory_fragmentation()
		self.display_memory_processes()

	def read_file(self):
		m_file = open('data/memory-block.txt')
		j_file = open('data/job-stream.txt')

		m_lines = m_file.readlines()[1:]
		j_lines = j_file.readlines()[1:]

		for idx, line in enumerate(m_lines):
			line = re.findall(r"[^\W\d_]+|\d+", line)
			memory = Memory(id=(idx + 1), name=str(line[0]), size=int(line[1]))
			if idx == 0:
				self.max_memory = memory.size
				self.min_memory = memory.size
			else:
				if memory.size > self.max_memory:
					self.max_memory = memory.size
				if memory.size < self.min_memory:
					self.min_memory = memory.size

			self.memories.append(memory)
			self.free_list.append(memory)

		for idx, line in enumerate(j_lines):
			line = re.findall(r"[^\W\d_]+|\d+", line)
			job = Job(id=(idx + 1), name=str(line[0]), time=int(line[1]), size=int(line[2]))
			self.max_time += job.time
			self.jobs.append(job)
			if job.size <= self.max_memory:
				self.qualified_jobs.append(job)
				self.qualified_jobs_count += 1

	def display_memory_blocks(self):
		row = 1
		for memory in self.memories:
			self.table.set(row, 0, memory.to_string())
			row += 1

	def display_job_streams(self):
		row = 1
		for job in self.jobs:
			self.table.set(row, 4, job.to_string())
			row += 1

	def display_job_waiting_time(self):
		row = 1
		for job in self.jobs:
			self.table.set(row, 5, job.get_waiting_time())
			row += 1

	def display_memory_fragmentation(self):
		row = 1
		for memory in self.memories:
			self.table.set(row, 3, memory.display_fragmentation())
			row += 1

	def display_memory_processes(self):
		row = 1
		for memory in self.memories:
			self.table.set(row, 1, memory.current_process())
			self.table.set(row, 2, memory.current_process_time())
			row += 1

	def perform_evaluations(self):
		self.calculate_throughput()
		self.calculate_storage()
		self.calculate_queue_length()

	def calculate_throughput(self):
		if len(self.qualified_jobs) and self.finished:
			self.throughput += (len(self.allocated) / float(self.counter))
			self.count_throughput += 1

	def calculate_storage(self):
		if len(self.qualified_jobs):
			self.storage = len(self.free_list) / float(len(self.memories))
			self.total_storage += self.storage
			self.count_storage += 1

	def calculate_queue_length(self):
		if len(self.qualified_jobs):
			self.queue_length = self.qualified_jobs_count - len(self.allocated) + 1
			self.total_queue_length += self.queue_length
			self.count_queue_length += 1

	def display_throughput(self):
		if self.finished:
			throughput = self.throughput / float(self.count_throughput)

			self.table.set(26, 0, "Throughput: " + str(throughput) + " finished job/s per ms")

	def display_storage(self):
		used = 1 - self.storage
		unused = self.storage
		ave = self.total_storage / float(self.count_storage)
		ave_used = 1 - ave
		ave_unused = ave
		self.table.set(27, 0, "Actual Storage Util (used/unused): " + str(used) + " / " + str(unused))
		self.table.set(28, 0, "Ave Storage Util (used/unused): " + str(ave_used) + " / " + str(ave_unused))

	def display_queue_length(self):
		ave = self.total_queue_length / float(self.count_queue_length)
		self.table.set(29, 0, "Actual Waiting Queue Length: " + str(self.queue_length) + " jobs")
		self.table.set(30, 0, "Ave Waiting Queue Length: " + str(ave) + " jobs")

	def display_ave_waiting(self):
		total = 0
		count = 0
		for job in self.jobs:
			if job.waiting_time_value() >= 0:
				count += 1
				total += job.waiting_time_value()

		self.table.set(31, 0, "Ave Waiting Time: " + str(total / float(count)) + " ms")

	def display_ave_frag(self):
		self.table.set(32, 0, "Ave Internal Fragmentation: " + str(self.total_frag / float(self.qualified_jobs_count)) + "K")

	def is_all_done(self):
		for job in self.jobs:
			if job.waiting_time_value() != -1:
				if job.counter > 0:
					return False
		return True

	def reset(self):
		self.free_list = []
		for job in self.jobs:
			if job.size <= self.max_memory:
				self.qualified_jobs.append(job)
			job.reset()

		for memory in self.memories:
			memory.process = None
			self.free_list.append(memory)

	def run(self):
		if len(self.qualified_jobs):
			self.free_list_size = len(self.free_list)
			self.check_jobs()
			self.check_memory()
			self.sort_memory()
			self.allocate_memory()
			if not self.is_all_done():
				self.perform_evaluations()
			self.update_display()
			# for job in self.jobs:
			# 	print(" -> JOB #: " + str(job.id))
			# 	if job.memory:
			# 		print(" AT MEMORY: " + str(job.memory.id))
			# 	else:
			# 		print(" NOT ALLOCATED")
			# 	print(" TIME: " + str(job.counter))
			# print("\n\n\n")
			if not self.is_all_done():
				print("Incrementing..")
				self.counter += 1
				print(self.counter)

			self.runner = self.after(1000, self.run)

	def sort_memory(self):
		if self.algo_type == "F":
			self.free_list = sorted(self.free_list, key=lambda x: x.id, reverse=False)
		elif self.algo_type == "B":
			self.free_list = sorted(self.free_list, key=lambda x: x.size, reverse=False)
		elif self.algo_type == "W":
			self.free_list = sorted(self.free_list, key=lambda x: x.size, reverse=True)

	def check_jobs(self):
		for job in self.qualified_jobs:
			if job.memory:
				if job.counter == 0:
					self.qualified_jobs.remove(job)
					job.memory = None
					self.finished += 1
					continue
				if job.counter > 0:
					job.decrease_time()
			else:
				if job.counter > 0:
					job.wait()

	def check_memory(self):
		for memory in self.memories:
			if memory.process:
				if memory.process.counter == 0:
					if memory not in self.free_list:
						self.free_list.append(memory)

	def allocate_memory(self):
		for job in self.qualified_jobs:
			if job not in self.allocated:
				for memory in self.free_list:
					if job.size <= memory.size:
						memory.process = job
						job.memory = memory
						self.total_frag += memory.get_frag()
						if job not in self.allocated:
							self.allocated.append(job)
						self.free_list.remove(memory)
						break

	def update_display(self):
		self.display_job_waiting_time()
		self.display_memory_fragmentation()
		self.display_memory_processes()
		self.display_throughput()
		self.display_storage()
		self.display_queue_length()
		self.display_ave_waiting()
		self.display_ave_frag()

	def stop(self):
		self.after_cancel(self.runner)

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
		label = tk.Label(self, text="Actual Storage Util: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 1, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Ave Storage Util: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 2, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Actual Waiting Queue Length: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 3, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Ave Waiting Queue Length: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 4, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Ave Waiting Time: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 5, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Ave Internal Fragmentation: ",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 6, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)

		self._widgets.append(current_row)
		current_row = []
		label = tk.Label(self, text="",
						borderwidth=1, width=15, foreground="#34495e", background="#34495e", anchor="w")
		label.grid(row=rows + 7, columnspan=6, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		button = tk.Button(self, text ="Start", command= self.start_simulation)
		button.grid(row=rows + 8, columnspan=6, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		current_row = []
		button = tk.Button(self, text ="Stop", command= self.stop_simulation)
		button.grid(row=rows + 9, column=0, columnspan=6, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		for column in range(columns):
			self.grid_columnconfigure(column, weight=1)

	def set(self, row, column, value, foreground="black", background="white", append=False):
		widget = self._widgets[row][column]
		if append:
			value = widget.cget("text") + "\n" + value
		widget.configure(text=value, foreground=foreground, background=background)

	def set_algo_type(self, algo_type="F"):
		self.parent.algo_type = algo_type

	def stop_simulation(self):
		self.parent.destroy()

	def start_simulation(self):
		self.parent.run()

raw = raw_input("Type of Algorithm: \n 1. First-Fit \n 2. Best-Fit \n 3. Worst-Fit\n")
algo_type = "F"
if raw == "1":
	algo_type = "F"
elif raw == "2":
	algo_type = "B"
elif raw == "3":
	algo_type = "W"

main = Main(algo_type=algo_type, header_idx=int(raw))
main.mainloop()
