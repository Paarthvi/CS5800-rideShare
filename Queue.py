# class Queue:
#     def __init__(self):
#         self.new_queue = []
#
#     def enqueue(self, points):
#         self.new_queue.append(points)
#
#     def dequeue(self, x=5):
#         if len(self.new_queue) < 5:
#             x = len(self.new_queue)
#         points = []
#         for i in range(x):
#             points.append(self.new_queue.pop())
#         return points
#
# num_of_queue = 5
# num_of_lists = 4
# queues = []
# for i in range(num_of_queue):
#     queue = Queue()
#     for j in range(num_of_lists):
#         for k in range(num_of_lists):
#             queue.enqueue([0,0,0,0,0])
#     queues.append(queue)
# for queue in queues:
#     print(queue.dequeue())
#
#

# Goal
# // [[1,2,3], [4,5,6,7]]
# //enqueu -- [[1,2,3] [4,5,6,7]]
# // deque [1,2] [4,5] -> remaining queue [3] , [6,7]
# // deque 5 people

class Queue():
    def __init__(self):
        self.new_queue = []
    def enqueue(self, points):
        for point in points:
            self.new_queue.append(point)
        return self.new_queue

    def dequeue(self, k):
        return_queue = []
        for i in range(len(self.new_queue)):
            queue = self.new_queue[i]
            if queue:
                return_queue.append(queue[:k])
                self.new_queue[i] = queue[k:]

        return return_queue

points = [[1,2,3], [4,5,6,7]]
e = Queue()
e.enqueue(points)
print(e.dequeue(2))
print(e.new_queue)


points = [[1,2,3,4,5,6], [4,5,6,7,8,9,10]]
e = Queue()
e.enqueue(points)
print(e.dequeue(5))
print(e.new_queue)
