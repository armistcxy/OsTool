from schedule import *
from log import refresh

if __name__ == "__main__":
    while True:

        number_of_task = int(input())
        if number_of_task < 1:
            print("End program")
            break

        refresh("log.txt")
        tasks = []
        for i in range(number_of_task):
            # input format: arrival time - duration - priority
            params = list(map(int, input().split()))
            tasks.append(Task(i, *params))

        # Please input algorithm type
        algo_type = ""
        not_found = True
        algo_set = set(["FCFS", "SJF", "SRJF", "RR"])
        while not_found:
            algo_type = input().strip()

            if algo_type in algo_set:
                not_found = False
            else:
                print(
                    "we do not support this algorithm, please choose one of these below:"
                )
                print("FCFS, STF, SRTF, RR")

        algo = None

        if algo_type == "FCFS":
            algo = FirstComeFirstServeAlgorithm(tasks)
        elif algo_type == "SJF":
            algo = ShortestJobFirstAlgorithm(tasks)
        elif algo_type == "SRJF":
            algo = ShortestRemainingJobFirstAlgorithm(tasks)
        elif algo_type == "RR":
            quantum = int(input())
            algo = RoundRobinAlgorithm(tasks, quantum)

        algo.simulate()
