from log import log


def avg(arr: list[int]):
    return sum(arr) / len(arr)


class Task:
    def __init__(self, id: int, arrival_time: int, duration: int, priority: int = 0):
        self.id = id
        self.arrival_time = arrival_time
        self.duration = duration
        self.priority = priority

    def __repr__(self) -> str:
        return f"Task {self.id + 1} arrived at {self.arrival_time}, durated {self.duration}, had priority {self.priority}"


class TimePart:
    def __init__(self, id: int, start: int, end: int):
        self.id = id
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"Process {self.id + 1}: {self.start} -> {self.end}"


class FirstComeFirstServeAlgorithm:
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks

    def simulate(self):
        timeline = []
        self.tasks.sort(key=lambda x: (x.arrival_time, x.priority, x.id))

        number_of_tasks = len(self.tasks)
        response_time = [0] * number_of_tasks
        turnaround_time = [0] * number_of_tasks
        waiting_time = [0] * number_of_tasks

        current_time = 0
        for task in self.tasks:
            log(task)
            if current_time < task.arrival_time:
                current_time = task.arrival_time

            response_time[task.id] = current_time - task.arrival_time
            waiting_time[task.id] = response_time[task.id]
            turnaround_time[task.id] = response_time[task.id] + task.duration

            timeline.append(
                TimePart(task.id, current_time, current_time + task.duration)
            )

            current_time += task.duration

        throughput = number_of_tasks / current_time
        log(f"throughput:       {throughput} ({number_of_tasks}/{current_time})")
        log(f"response time:    {response_time}, AVG: {avg(response_time)}")
        log(f"waiting time:     {waiting_time}, AVG: {avg(waiting_time)}")
        log(f"turn around time: {turnaround_time}, AVG: {avg(turnaround_time)}")
        log("")
        for tl in timeline:
            log(tl)


class ShortestJobFirstAlgorithm:
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks

    # in this algorithm, I assume that there's no priority
    def simulate(self):
        timeline = []
        # self.tasks.sort(key=lambda x: (x.arrival_time, x.duration, x.id))

        number_of_tasks = len(self.tasks)
        response_time = [0] * number_of_tasks
        turnaround_time = [0] * number_of_tasks
        waiting_time = [0] * number_of_tasks
        finish = [False] * number_of_tasks

        current_time = 0
        while not all(finish):
            batch = []
            for task in self.tasks:
                if not finish[task.id] and task.arrival_time <= current_time:
                    batch.append(task)

            # in case there is no task has arrived
            if len(batch) == 0:
                todo = None
                earliest_time = 10**6
                for task in self.tasks:
                    if not finish[task.id]:
                        if task.arrival_time <= earliest_time:
                            todo = task
                            earliest_time = task.arrival_time
                batch.append(todo)
                current_time = earliest_time

            # sort by duration then next criteria is id
            batch.sort(key=lambda x: (x.duration, x.id))

            chosen_task = batch[0]
            finish[chosen_task.id] = True

            timeline.append(
                TimePart(
                    chosen_task.id, current_time, current_time + chosen_task.duration
                )
            )

            response_time[chosen_task.id] = current_time - chosen_task.arrival_time
            waiting_time[chosen_task.id] = response_time[chosen_task.id]
            turnaround_time[chosen_task.id] = (
                response_time[chosen_task.id] + chosen_task.duration
            )

            current_time += chosen_task.duration

        throughput = number_of_tasks / (current_time + 1)
        log(f"throughput:       {throughput} ({number_of_tasks}/{current_time})")
        log(f"response time:    {response_time}, AVG: {avg(response_time)}")
        log(f"waiting time:     {waiting_time}, AVG: {avg(waiting_time)}")
        log(f"turn around time: {turnaround_time}, AVG: {avg(turnaround_time)}")
        log("")
        for tl in timeline:
            log(tl)


class ShortestRemainingJobFirstAlgorithm:
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks

    def simulate(self):
        timeline = []

        number_of_tasks = len(self.tasks)
        response_time = [-1] * number_of_tasks
        turnaround_time = [0] * number_of_tasks
        waiting_time = [0] * number_of_tasks
        finish = [False] * number_of_tasks

        current_time = -1

        last_task_id = -1
        start_time = -1
        last_done = -1
        chosen_task = None
        while not all(finish):
            current_time += 1
            batch = []
            for task in self.tasks:
                if current_time >= task.arrival_time and task.duration > 0:
                    batch.append(task)

            if len(batch) == 0:
                continue

            batch.sort(key=lambda x: (x.duration, x.id))

            chosen_task = batch[0]
            chosen_task.duration -= 1

            if response_time[chosen_task.id] == -1:
                response_time[chosen_task.id] = current_time - chosen_task.arrival_time

            if chosen_task.duration == 0:
                finish[chosen_task.id] = True
                turnaround_time[chosen_task.id] = (
                    current_time + 1 - chosen_task.arrival_time
                )

            if chosen_task.id != last_task_id:
                if last_task_id != -1:
                    timeline.append(TimePart(last_task_id, start_time, last_done + 1))

                last_task_id = chosen_task.id
                start_time = current_time

            for task in self.tasks:
                if task.id == chosen_task.id:
                    # task.duration -= 1
                    pass
                elif task.duration > 0 and task.arrival_time <= current_time:
                    waiting_time[task.id] += 1

            last_done = current_time

        timeline.append(TimePart(last_task_id, start_time, current_time + 1))

        throughput = number_of_tasks / (current_time + 1)

        log(f"throughput:       {throughput} ({number_of_tasks}/{current_time})")
        log(f"response time:    {response_time}, AVG: {avg(response_time)}")
        log(f"waiting time:     {waiting_time}, AVG: {avg(waiting_time)}")
        log(f"turn around time: {turnaround_time}, AVG: {avg(turnaround_time)}")
        log("")
        for tl in timeline:
            log(tl)


from collections import deque


class RoundRobinAlgorithm:
    def __init__(self, tasks: list[Task], quantum: int):
        self.tasks = tasks
        self.quantum = quantum

    def simulate(self):
        number_of_tasks = len(self.tasks)
        self.tasks.sort(key=lambda x: (x.arrival_time, x.id))
        timeline = []

        response_time = [-1] * number_of_tasks
        turnaround_time = [0] * number_of_tasks
        waiting_time = [0] * number_of_tasks
        finish = [False] * number_of_tasks

        current_time = 0
        batch = deque()

        index = 0
        session = self.quantum
        current_task_id = -1
        while not all(finish):

            while (
                index < number_of_tasks
                and self.tasks[index].arrival_time <= current_time
            ):
                batch.append(self.tasks[index])
                index += 1

            if len(batch) == 0:
                current_time += 1
                continue

            current_task_id = batch[0].id
            if response_time[current_task_id] == -1:
                response_time[current_task_id] = current_time - batch[0].arrival_time

            session -= 1
            batch[0].duration -= 1
            if batch[0].duration == 0:
                timeline.append(
                    TimePart(
                        current_task_id,
                        current_time - self.quantum + session + 1,
                        current_time + 1,
                    )
                )
                finish[current_task_id] = True
                turnaround_time[current_task_id] = (
                    current_time + 1 - batch[0].arrival_time
                )
                batch.popleft()
                session = self.quantum

            if session == 0:
                session = self.quantum
                if batch[0].duration > 0:
                    timeline.append(
                        TimePart(
                            current_task_id,
                            current_time - self.quantum + 1,
                            current_time + 1,
                        )
                    )

                    task = batch.popleft()
                    batch.append(task)

            for task in batch:
                if task.id != current_task_id:
                    waiting_time[task.id] += 1
            current_time += 1

        throughput = number_of_tasks / (current_time)

        log(f"throughput:       {throughput} ({number_of_tasks}/{current_time})")
        log(f"response time:    {response_time}, AVG: {avg(response_time)}")
        log(f"waiting time:     {waiting_time}, AVG: {avg(waiting_time)}")
        log(f"turn around time: {turnaround_time}, AVG: {avg(turnaround_time)}")
        log("")
        for tl in timeline:
            log(tl)
