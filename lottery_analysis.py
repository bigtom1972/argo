import csv
from typing import List, Union

def getHistoryDataFromCsv(csvfile: str) -> List[List[Union[str, List[str], str]]]:
    """
    Read lottery history data from a CSV file and return it as a list of dictionaries.
    Each dictionary represents a row in the CSV file with column headers as keys.
    """
    history_data = []
    try:
        with open(csvfile, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                history_data.append(row['Issue'], row['Red Balls'].split(":"), row['Blue Ball']])                    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        print(e)
    history_data.reverse()
    return history_data


def guessByPolicy1(data: List[List[Union[str, List[str], str]]] , hist_cnt: int) -> List[str]:
    """
    Guess the next lottery numbers based on a simple policy.
    This is a placeholder function and should be replaced with actual logic.
    """
    oldestIssue = data[0][0]
    latestIssue = data[hist_cnt-1][0]
    
    
    red_balls_num = 6
    red_coutners = []
    red_distances = []

    blue_counter = []
    blue_distances = []


    for idx in range(hist_cnt):
        red_balls = data[idx][1]
        blue_ball = data[idx][2]
        for i in range(red_balls_num):
            red_distances[red_balls[i]] = hist_cnt - idx
            if red_balls[i] in red_coutners:
                red_coutners[red_balls[i]] += 1            
            else:
                red_coutners[red_balls[i]] = 1
        blue_distances[blue_ball] = hist_cnt - idx
        if blue_ball in blue_counter:
            blue_counter[blue_ball] += 1
        else:
            blue_counter[blue_ball] = 1
    
    sorted_red = sorted(red_coutners.items(), key=lambda kv: kv[1], reverse=True)
    sorted_blue = sorted(blue_counter.items(), key=lambda kv: kv[1], reverse=True)
    




def main():
    import argparse
    parser = argparse.ArgumentParser(description='Analyze lottery history data')
    parser.add_argument('csvfile', help='CSV file containing lottery history data')
    args = parser.parse_args()
    history_data = getHistoryDataFromCsv(args.csvfile)
    print(f"Read {len(history_data)} rows of lottery history data from {args.csvfile}")
    for row in history_data:
        print(row)



if __name__ == '__main__':
    main()
