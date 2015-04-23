from geopy.distance import great_circle
from imposm.parser import OSMParser
import time

__author__ = 'pavel'

 # pointA = (41.49008, -71.312796)
 # pointB = (41.499498, -81.695391)
def getDistance(pointA, pointB):
    return great_circle(pointA,pointB).kilometers

def printElapsedTime(start):
    end = time.clock()
    print 'time elapsed', (end - start)/60, 'minutes'


class DistanceCounter(object):
    distance = 0
    filteredWays = []
    nodesCoordinates = {}
    key = ''
    value = ''

    def __init__(self, key='highway', value='cycleway'):
        self.key = key
        self.value = value

    def ways(self, ways):
        # callback method for ways
        for osmid, tags, refs in ways:
            if self.key in tags:
                #print (self.key, tags[self.key], self.value, tags[self.key]== self.value )
                if tags[self.key] == self.value:
                    #in refs are all nodes
                    self.filteredWays.append(refs)
                    for id in refs:
                        self.nodesCoordinates[id]=0

    def coords(self, coords):
        for osmid, longitude,latitude in coords:
            if osmid in self.nodesCoordinates:
                #print latitude, longitude
                self.nodesCoordinates[osmid] = (latitude, longitude)


    def computeTotalDistance(self):
        for way in self.filteredWays:
            previousNode = way[0]
            for currentNode in way:
                self.distance += getDistance(self.nodesCoordinates[previousNode], self.nodesCoordinates[currentNode])
                previousNode = currentNode

# instantiate counter and parser and start parsing
KEY='waterway'
VALUE='river'

start =time.clock()
counter = DistanceCounter(KEY,VALUE)
print 'initializing for', KEY, '=', VALUE
printElapsedTime(start)

print 'parsing ways'
p = OSMParser(concurrency=4, ways_callback=counter.ways)
p.parse('/home/pavel/osp/osm/czech-republic-snapshot.osm.pbf')
printElapsedTime(start)

print 'parsing coords'
p = OSMParser(concurrency=4, coords_callback=counter.coords)
p.parse('/home/pavel/osp/osm/czech-republic-snapshot.osm.pbf')
printElapsedTime(start)

print('computing total distance')
counter.computeTotalDistance()

# done
printElapsedTime(start)
print 'total distance for', KEY, '=', VALUE, 'is:', counter.distance, 'km'