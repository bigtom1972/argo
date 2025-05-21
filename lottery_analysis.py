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
                history_data.append([row['Issue'], row['Red Balls'].split(":")])                    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        print(e)
    history_data.reverse()
    return history_data


def guessByPolicy1(data: List[List[Union[str, List[str], str]]] , hist_cnt: int, baseM: int, num_guess: int) ->None :
    """
    Guess the next lottery numbers based on a simple policy.
    This is a placeholder function and should be replaced with actual logic.
    """
    # oldestIssue = data[0][0]
    # latestIssue = data[hist_cnt-1][0]
    
    
    red_balls_num = 6
    red_coutners = {}
    red_distances = {}

    blue_counter = {}
    blue_distances = {}
    
    for idx in range(hist_cnt):
        red_balls = data[idx][1][0:red_balls_num]
        blue_ball = data[idx][1][-1]
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
    
    # print(f"blue distances: {blue_distances}")

    for guess_time in range(num_guess):
        red_distances_invert = invert_dict(red_distances)
        blue_distances_invert = invert_dict(blue_distances)
        
        red_balls = []
        blue_ball = ""
        sorted_red = list(red_distances_invert.keys())
        sorted_blue = list(blue_distances_invert.keys())        
        
        sorted_red = sorted(sorted_red, key=lambda i: int(i), reverse=True)
        sorted_blue = sorted(sorted_blue, key=lambda i: int(i), reverse=True)
        # print(f"sorted red balls: {sorted_red}")        
        for i in range(red_balls_num):             
            red_balls.extend(red_distances_invert[sorted_red[i]])
            # print(f"selected red balls: {red_balls} with distance: {sorted_red[i]}")
            if len(red_balls) >= red_balls_num:
                break
        red_balls = red_balls[:red_balls_num]
        # print(f"Finally selected red balls: {red_balls} ")
        blue_ball = blue_distances_invert[sorted_blue[0]][0]
        # print(f"Finally selected blue ball: {blue_ball} with distance: {sorted_blue[0]}")

        act_red_balls = data[hist_cnt][1][0:red_balls_num]
        act_blue_ball = data[hist_cnt][1][-1]
        issue = data[hist_cnt][0]
        single_cost = 2
        times = 5
        baseM = baseM - single_cost * times
        result = checkLottery(act_red_balls, act_blue_ball, red_balls, blue_ball)
        ret = 0
        if result == 0:
            ret= 0
        elif result == 6:
            ret = 5 * times
        elif result == 5:
            ret = 10 * times
        elif result == 4:
            ret = 200 * times
        elif result == 3:
            ret = 3000 * times
        elif result == 2:
            ret = 5000000 * times
        elif result == 1:
            ret = 10000000 * times
        else:
            ret = 0
        baseM = baseM + ret
        print(f"Guess time: {guess_time}, Issue： {issue} baseM: {baseM}, result: {result}, red_balls: {red_balls}, blue_ball: {blue_ball}, act_red_balls: {act_red_balls}, act_blue_ball: {act_blue_ball}, ret: {ret}")

        hist_cnt += 1
        for i in range(red_balls_num):
            red_distances[act_red_balls[i]] = 1
            if act_red_balls[i] in red_coutners:
                red_coutners[act_red_balls[i]] += 1            
            else:
                red_coutners[act_red_balls[i]] = 1
        blue_distances[act_blue_ball] = 1
        if act_blue_ball in blue_counter:
            blue_counter[act_blue_ball] += 1
        else:
            blue_counter[act_blue_ball] = 1





    




def checkLottery( act_red_balls: List[str], act_blue_ball: str, guess_red_balls: List[str], guess_blue_ball: str) -> int:
    """
    Check the result of a lottery guess.
    Returns the number of correct guesses.
    """
    red_correct = len([x for x in act_red_balls if x in guess_red_balls])
    blue_correct = 1 if act_blue_ball == guess_blue_ball else 0
    if blue_correct == 0 :
        if red_correct <4 :
            return 0;
        else:
            if red_correct == 4:
                return 5
            elif red_correct == 5:
                return 4
            elif red_correct == 6:
                return 2
    else:
        if red_correct == 3:
            return 5
        elif red_correct == 4:
            return 4
        elif red_correct == 5:
            return 3
        elif red_correct == 6:
            return 1
        else:
            return 6
    

    
    
            



    
def invert_dict(input_dict):
    inverted_dict = {}
    for key, value in input_dict.items():
        if value in inverted_dict:
            if isinstance(inverted_dict[value], list):
                inverted_dict[value].append(key)
            else:
                inverted_dict[value] = [inverted_dict[value], key]
        else:
            inverted_dict[value] = [key]
    return inverted_dict



    # sorted_red = sorted(red_coutners.items(), key=lambda kv: kv[1], reverse=True)
    # sorted_blue = sorted(blue_counter.items(), key=lambda kv: kv[1], reverse=True)
    




def main():
    import argparse
    parser = argparse.ArgumentParser(description='Analyze lottery history data')
    parser.add_argument('--csvfile', type = str, help='CSV file containing lottery history data')
    parser.add_argument('--hist_cnt', type=int, default=1000, help='Number of history records to analyze')
    parser.add_argument('--num_guess', type=int, default=100, help='Number of guesses to make')
    parser.add_argument('--baseMoney', default=1000, help='Base Money for Lottery')
    args = parser.parse_args()
    history_data = getHistoryDataFromCsv(args.csvfile)
    print(f"Read {len(history_data)} rows of lottery history data from {args.csvfile}")
    guessByPolicy1(history_data , args.hist_cnt, args.baseMoney, args.num_guess)




if __name__ == '__main__':
    main()
