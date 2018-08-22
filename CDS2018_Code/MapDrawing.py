from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import statistics as stats

# List of result files from Sensor_Data_Compiler.py
# Replace with your own files
results = ['results/result_seg_13-21_6sec_M.csv',
            'results/result_seg_13-48_6sec_M.csv',
            'results/result_seg_15-13_6sec_M.csv',
            'results/result_seg_16-05_6sec_M.csv',
            'results/result_seg_18-24_6sec_M.csv',
            'results/result_seg_18-44_6sec_M.csv',
            'results/result_seg_20-18_6sec_M.csv',
            'results/result_seg_20-33_6sec_M.csv']

# Calculates colors for absolute values of PM
# As defined by the US EPA
def color(pm25):
    if pm25 <= 12:
        return 'lime'
    if pm25 <= 35.4:
        return 'yellow'
    if pm25 <= 55.4:
        return 'orange' 
    return 'red'

# Calculates colors for measuring difference between individual sensors 
# Magnitudes of colors were determined arbitrarily by our team, can be changed if necessary
def colorDiff(diff):
    if abs(diff) <= 5:
        return 'lime'
    if abs(diff) <= 10:
        return 'yellow'
    if abs(diff) <= 15:
        return 'orange'
    return 'red'


def drawMap(resultFile):
    with open(resultFile, newline='') as rf:
        # Centers a satellite image over the run
        # Change values of lat/long bounds for a different run
        new_map = Basemap(llcrnrlon=-84.404627,llcrnrlat=33.770042,urcrnrlon=-84.383710,urcrnrlat=33.781740, epsg=2240)
        new_map.arcgisimage(service='World_Imagery', xpixels = 1500, verbose= True)

        lines_rf = rf.readlines()[1:]
        lines_rf = [i.strip().split(',') for i in lines_rf]

        # Each iteration draws one colored line on the map, for each segment
        for i, row in enumerate(lines_rf):
            if i+1 == len(lines_rf):
                break
            if row[1] == '""' or lines_rf[i+1][1] == '""' or row[1] == '' or lines_rf[i+1][1] == '':
                continue
            coords = row[1:3] + lines_rf[i+1][1:3]
            coords = [i for i in coords]

            # Error checking
            # Cells in the results files may or may not be enclosed with double quotes
            if coords[0][0] == '"':
                lats = [float(coords[0][1:-1]), float(coords[2][1:-1])]
                longs = [float(coords[1][1:-1]), float(coords[3][1:-1])]
            else:
                lats = [float(coords[0]), float(coords[2])]
                longs = [float(coords[1]), float(coords[3])]
            x,y = new_map(longs, lats)

            # Error checking
            # Cells in the results files may or may not be enclosed with double quotes
            if row[17][0] == '"':
                pm_mean = stats.mean([float(row[9][1:-1]),float(row[13][1:-1])])
                pm_mean = float(row[5][1:-1])
                pm_mean = float(row[17][1:-1])
            else:
                pm_mean = stats.mean([float(row[9]),float(row[13])])
                pm_mean = float(row[5])
                pm_mean = float(row[17])
            if pm_mean == 0:
                continue
            
            new_map.plot(x, y, marker='o', color=colorDiff(pm_mean), linewidth=7.0)


def main():
    fig = plt.figure()
    plt.subplots_adjust(left=0.05,right=0.95,bottom=0.1,top=0.9,wspace=0.05, hspace=0.1)
    for i, f in enumerate(results):
        plt.subplot(3,3,i+1) #increase if plotting more than 9 runs on one day
        drawMap(f)
    plt.show()

main()