#coding:utf-8

def read_station(filename):
    file = open(filename)
    stations_with_line = []
    stations = []
    for l in file.readlines():
        stations_line = l.split()
        line = stations_line[0]
        for i in range(1, len(stations_line)):
            station = stations_line[i]
            station_with_line = (line, station)
            stations_with_line.append(station_with_line)
            if station not in stations:
                stations.append(station)
    return stations, stations_with_line


# def make_relaionslist(stations, stations_with_line):
    # relationslist = []
    # for i in range(len(lines)):
        # line = lines[i]
        # for j in range(len(line)):
            # stations_list = line["stations"]
            # station = stations_list[j]


# def search_transfer(start, end):



if __name__ == '__main__':
    stations, stations_with_line = read_station("net.txt")
    # search_transfer(sys.argv[1], sys.argv[2])
    print str(stations_with_line).decode("string-escape")
