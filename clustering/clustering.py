import random
from position import Position
class cluster():
    def divideIntoCluster(self, points, k):
        centroids = random.sample(points, k)
        print("Printing centroid")
        for c in centroids:
            print(c)
        for x in range(1000):
            clusters = [[] for _ in range(k)]
            for location in points:
                cluster_no = -1
                min_distance = float('inf')
                for i in range(len(centroids)):
                    distance = location.euclid(centroids[i])
                    if distance < min_distance:
                        min_distance = distance
                        cluster_no = i
                clusters[cluster_no].append(location)
                print(f"Point {location.name} added to {cluster_no} cluster")
                updated_centroid_lat = (location.latitude + centroids[cluster_no].latitude)/2
                updated_centroid_long = (location.longitude + centroids[cluster_no].longitude)/2
                centroids[cluster_no] = Position(updated_centroid_lat, updated_centroid_long)
        return clusters

mfag = Position(42.3383847862946, -71.09596925777339, name = "mfa g")
wvh = Position(42.338828895046134, -71.09206396187207, name = "wvh")
mfa = Position(42.33935230490517, -71.09418827118103, name = "mfa only")

bch = Position(42.33809276105862, -71.10554772340559, name = "children hospital")
bhfw = Position(42.33623178846243, -71.10764569697659, name = "another hospital")

nubian = Position(42.3302537463558, -71.08405501615835, name = "nubian")
suya = Position(42.328725074917315, -71.08230536373581, name = "suya")
points = [mfag, wvh, mfa, bch, bhfw, nubian, suya]
k = 3
a = cluster()

cluster = a.divideIntoCluster(points, k)
for i in range(len(cluster)):
    print(f"Printing {i} cluster")
    for j in range(len(cluster[i])):
        print(cluster[i][j])
    print()






