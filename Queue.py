class Queue:
    def __init__(self):
        self.new_queue = []

    def enqueue(self, points):
        self.new_queue.append(points)

    def dequeue(self, x=5):
        if len(self.new_queue) < 5:
            x = len(self.new_queue)
        points = []
        for i in range(x):
            points.append(self.new_queue.pop())
        return points

num_of_queue = 5
num_of_lists = 4
queues = []
for i in range(num_of_queue):
    queue = Queue()
    for j in range(num_of_lists):
        for k in range(num_of_lists):
            queue.enqueue([0,0,0,0,0])
    queues.append(queue)
for queue in queues:
    print(queue.dequeue())
