
class TestMain(object):
    def test_file_reading(self, memories, jobs):
        test_mem_1 = memories[0]
        test_mem_2 = memories[len(memories) - 1]
        test_mem_3 = memories[4]

        test_job_1 = jobs[0]
        test_job_2 = jobs[len(jobs) - 1]
        test_job_3 = jobs[10]

        mem_success_count = 0
        if test_mem_1.id == 1 and test_mem_1.name == "1" and test_mem_1.size == 9500:
            mem_success_count += 1
        if test_mem_2.id == 10 and test_mem_2.name == "10" and test_mem_2.size == 500:
			mem_success_count += 1
        if test_mem_3.id == 5 and test_mem_3.name == "5" and test_mem_3.size == 3000:
            mem_success_count += 1

        if mem_success_count == 3:
            print("Memory File Reading: SUCCESS")
        else:
            print("Memory File Reading: FAILED - Success Count=" + str(mem_success_count))

        job_success_count = 0
        if test_job_1.id == 1 and test_job_1.name == "1" and test_job_1.size == 5760 and test_job_1.time == 5:
            job_success_count += 1
        if test_job_2.id == 25 and test_job_2.name == "25" and test_job_2.size == 760 and test_job_2.time == 10:
            job_success_count += 1
        if test_job_3.id == 11 and test_job_3.name == "11" and test_job_3.size == 6580 and test_job_3.time == 5:
            job_success_count += 1

        if job_success_count == 3:
            print("Job File Reading: SUCCESS")
        else:
            print("Job File Reading: FAILED - Success Count=" + str(job_success_count))
