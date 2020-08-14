from functools import total_ordering
from itertools import count
from typing import List

@total_ordering
class Task:
    _ids = count(0) #shared id variable, unique for each task
    
    def __init__(self, release: int, duration: int, deadline: int):
        self._id = next(self._ids)
        self.release = release
        self.duration = duration
        self.deadline = deadline
        self.start_min = release
        self.start_max = deadline - duration
        
    def __eq__(self, other):
        return self.deadline == other.deadline
    
    def __ne__(self, other):
        return not (self.deadline == other.deadline)
    
    def __lt__(self, other):
        return self.deadline < other.deadline
    
    def __repr__(self):
        return f"Task ID: {self._id}, release: {self.release}, duration: {self.duration}, deadline: {self.deadline}"

class cEDF:
    def __init__(self, task_index: List, time):
        self._index = task_index
        self._time = time
        self._crit_q = self._critical_queue()
        self._red_q = self._ready_queue()
        
    def _critical_queue(self):
        crit_q = sorted(self._index, key=lambda x: x.start_max, reverse=False)
        return crit_q
    
    def _ready_queue(self):
        temp_q = []
        for item in self._index:
            if item.release <= self._time:
                temp_q.append(item)
        red_q = sorted(temp_q, key=lambda x: x.deadline, reverse=False)
        return red_q
    
    def _remove_task_id_queue(self, task_id: int, queue: List):
        for i in range(0, len(queue)):
            if queue[i]._id == task_id:
                del queue[i]
                break;
    
    def _remove_task_id_all(self, task_id: int):
        self._remove_task_id_queue(task_id, self._index)
        self._remove_task_id_queue(task_id, self._crit_q)
        self._remove_task_id_queue(task_id, self._red_q)
    
    def update_time(self, time: int):
        self._time = time
        self._red_q = self._ready_queue()
        
    def schedule(self):
        return NotImplementedError()