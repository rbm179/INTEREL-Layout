"""
This function allows you to check / count a given process and kill it if required.
"""
import psutil
import time


class ProcessManager:
    def __init__(self,
                 process_limit=None,
                 process_name=None,
                 max_duration_for_process_in_mins=None):
        self.process_limit = process_limit
        self.process_name = process_name
        self.max_duration_for_process_in_mins = max_duration_for_process_in_mins

    """
    This method counts number of process and returns True, if process count exceeds allowed threshold and
    returns False, if process count is less than equal to allowed threshold.
    """
    def count_excel_processes(self):
        excel_count = sum(1 for p in psutil.process_iter(['name'])
                          if p.info['name'] == self.process_name)
        return excel_count > self.process_limit, excel_count

    """
    This method counts number of process and if total number of spawned processes, exceeds given threshold, then it 
    checks if spawned process is older than xx minutes. IF yes, terminates all old processes
    """
    def kill_old_processes(self):
        original_excel_processes = [p for p in psutil.process_iter(['pid', 'name', 'create_time'])
                                    if p.info['name'] == self.process_name]
        original_excel_count = len(original_excel_processes)

        current_time = time.time()
        for p in original_excel_processes:
            if current_time - p.info['create_time'] > (self.max_duration_for_process_in_mins * 60):
                try:
                    process = psutil.Process(p.info['pid'])
                    process.terminate()
                except psutil.NoSuchProcess:
                    pass

        # Count the number of EXCEL.exe processes after termination
        excel_processes_after_termination = [p for p in psutil.process_iter(['name'])
                                             if p.info['name'] == self.process_name]
        excel_count_after_termination = len(excel_processes_after_termination)

        return original_excel_count, excel_count_after_termination


