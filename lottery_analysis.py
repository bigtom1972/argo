import csv
from typing import List, Union
import csv
from typing import List, Union
import random

class LotteryAnalyzer:
    def __init__(self, csvfile: str, hist_cnt: int) -> None:
        self.csvfile = csvfile
        self.data = self.get_history_data_from_csv()
        self.red_balls_num = 6
        self.hist_cnt = hist_cnt
        self.red_counters = {}
        self.blue_counters = {}
        self.red_distances = {}
        self.blue_distances = {}
        self.initWithHistoryData()



    def get_history_data_from_csv(self) -> List[List[Union[str, List[str], str]]]:
        """
        Read lottery history data from a CSV file and return it as a list of lists.
        Each list represents a row in the CSV file with specific columns as elements.
        """
        history_data = []
        try:
            with open(self.csvfile, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    history_data.append([row['Issue'], row['Red Balls'].split(":")])
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        history_data.reverse()
        return history_data

    def initWithHistoryData(self) -> None:
        """
        Initialize the LotteryAnalyzer with history data.
        This function is a placeholder and should be replaced with actual logic.
        """
        # Logic for initializing with history data would be implemented here
        for idx in range(self.hist_cnt):
            red_balls = self.data[idx][1][0:self.red_balls_num]
            blue_ball = self.data[idx][1][-1]
            for i in range(self.red_balls_num):
                self.red_distances[red_balls[i]] = self.hist_cnt - idx
                if red_balls[i] in self.red_counters:
                    self.red_counters[red_balls[i]] += 1            
                else:
                    self.red_counters[red_balls[i]] = 1
            self.blue_distances[blue_ball] = self.hist_cnt - idx
            if blue_ball in self.blue_counters:
                self.blue_counters[blue_ball] += 1
            else:
                self.blue_counters[blue_ball] = 1

    def updateHistStatistics(self, act_red_balls: List[str], act_blue_ball: str) -> None:
        """
        Update the history statistics with the actual drawn numbers.
        This function is a placeholder and should be replaced with actual logic.
        """
        # Logic for updating history statistics would be implemented here
        for i in range(self.red_balls_num):
            self.red_distances[act_red_balls[i]] = 1
            if act_red_balls[i] in self.red_counters:
                self.red_counters[act_red_balls[i]] += 1            
            else:
                self.red_counters[act_red_balls[i]] = 1
        self.blue_distances[act_blue_ball] = 1
        if act_blue_ball in self.blue_counters:
            self.blue_counters[act_blue_ball] += 1
        else:
            self.blue_counters[act_blue_ball] = 1
    
    def _red_ball_by_distance(self) -> List[str]:
        """
        Get red balls by distance.
        This function is a placeholder and should be replaced with actual logic.
        """
        # Logic for getting red balls by distance would be implemented here
        red_balls_by_distance = []
        red_distances_invert = invert_dict(self.red_distances)

        sorted_red = list(red_distances_invert.keys())
        sorted_red = sorted(sorted_red, key=lambda i: int(i), reverse=True)
        for i in range(self.red_balls_num):             
            red_balls_by_distance.extend(red_distances_invert[sorted_red[i]])
            # print(f"selected red balls: {red_balls} with distance: {sorted_red[i]}")
            if len(red_balls_by_distance) >= self.red_balls_num:
                break
        red_balls_by_distance = red_balls_by_distance[:self.red_balls_num]
        return red_balls_by_distance

    def _blue_ball_by_distance(self) -> str:
        """
        Get blue ball by distance.
        This function is a placeholder and should be replaced with actual logic.
        """
        # Logic for getting blue ball by distance would be implemented here
        blue_ball_by_distance = ""
        blue_distances_invert = invert_dict(self.blue_distances)

        sorted_blue = list(blue_distances_invert.keys())
        sorted_blue = sorted(sorted_blue, key=lambda i: int(i), reverse=True)
        blue_ball = blue_distances_invert[sorted_blue[0]][0]
        return blue_ball
    
    def _blue_ball_by_counter(self) -> str:
        """
        Get blue ball by counter.
        This function is a placeholder and should be replaced with actual logic.
        """
        # Logic for getting blue ball by counter would be implemented here
        blue_ball_by_counter = ""
        blue_counters_invert = invert_dict(self.blue_counters)

        sorted_blue_by_counter = list(blue_counters_invert.keys())
        sorted_blue_by_counter = sorted(sorted_blue_by_counter, key=lambda i: int(i), reverse=True)
        blue_ball = blue_counters_invert[sorted_blue_by_counter[0]][0]
        return blue_ball
    
    def _red_ball_mix_distance_counter(self ) -> List[str]:
        """
        Get red balls by mixing distance and counter.
        This function is a placeholder and should be replaced with actual logic.
        """
        # Logic for getting red balls by mixing distance and counter would be implemented here
        red_balls_by_distance = []
        red_balls_by_counter = []
        red_distances_invert = invert_dict(self.red_distances)
        red_counters_invert = invert_dict(self.red_counters)            

        sorted_red = list(red_distances_invert.keys())
        sorted_red = sorted(sorted_red, key=lambda i: int(i), reverse=True)

        sorted_red_by_counter = list(red_counters_invert.keys())
        sorted_red_by_counter = sorted(sorted_red_by_counter, key=lambda i: int(i), reverse=True)
        for i in range(self.red_balls_num):             
            red_balls_by_distance.extend(red_distances_invert[sorted_red[i]])
            # print(f"selected red balls: {red_balls} with distance: {sorted_red[i]}")
            if len(red_balls_by_distance) >= self.red_balls_num:
                break
        red_balls_by_distance = red_balls_by_distance[:self.red_balls_num]

        for i in range(self.red_balls_num):
            red_balls_by_counter.extend(red_counters_invert[sorted_red_by_counter[i]])
            # print(f"selected red balls by counter: {red_balls_by_counter} with distance: {sorted_red_by_counter[i]}")
            if len(red_balls_by_counter) >= self.red_balls_num:
                break       
        red_balls_by_counter = red_balls_by_counter[:self.red_balls_num]

        red_balls = list(set(red_balls_by_distance + red_balls_by_counter))
        red_balls = random.sample(red_balls, self.red_balls_num)
        red_balls = sorted(red_balls, key=lambda i: int(i), reverse=False)
        return red_balls


    def _red_ball_rand(self) -> List[str]:    
        """
        Get red balls randomly.
        This function is a placeholder and should be replaced with actual logic.
        """
        # Logic for getting red balls randomly would be implemented here
        red_balls = []
        while True:
            tmp = str(random.randint(1, 33))
            if tmp not in red_balls:
                red_balls.append(tmp)    
            if len(red_balls) >= self.red_balls_num:
                break
            red_balls = sorted(red_balls, key=lambda i: int(i), reverse=False)
        return red_balls

    def _blue_ball_rand(self) -> str:
        """
        Get blue ball randomly.
        This function is a placeholder and should be replaced with actual logic.
        """
        # Logic for getting blue ball randomly would be implemented here
        blue_ball = str(random.randint(1, 16))
        return blue_ball


    def play_guess_game(self, base_money: int, num_guess: int, single_cost: int, bet_times: int) -> None:
        """
        Guess the next lottery numbers based on a simple policy.
        This is a placeholder function and should be replaced with actual logic.
        """
        # Logic for guessing numbers would be implemented here        
        for guess_time in range(num_guess):
            
            # red_balls = self._red_ball_mix_distance_counter()
            # red_balls = self._red_ball_by_distance()
            red_balls = self._red_ball_rand()


            blue_ball = self._blue_ball_by_distance()
            # blue_ball = self._blue_ball_by_counter()
            # blue_ball = self._blue_ball_rand()
            act_red_balls = self.data[self.hist_cnt][1][0:self.red_balls_num]
            act_blue_ball = self.data[self.hist_cnt][1][-1]
            issue = self.data[self.hist_cnt][0]
            
            result = checkLottery(act_red_balls, act_blue_ball, red_balls, blue_ball, single_cost, bet_times)
            
            red_correct = len([x for x in act_red_balls if x in red_balls])

            base_money = base_money + result
            if result > 0:
                print(f"Guess time: {guess_time}, Issue： {issue} baseM: {base_money}, result: {result}, red_balls: {red_balls}, blue_ball: {blue_ball}, act_red_balls: {act_red_balls}, act_blue_ball: {act_blue_ball}, ret: {result}, red_correct: {red_correct}")

            if base_money <= 0:
                print(f"base_money is negative, stop, totally round: {guess_time}")
                exit()
            self.hist_cnt += 1
            self.updateHistStatistics(act_red_balls, act_blue_ball)
        print(f"Completed guesses, based money is {base_money}, total round: {guess_time}")

            
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Analyze lottery history data')
    parser.add_argument('--csvfile', type=str, help='CSV file containing lottery history data')
    parser.add_argument('--hist_cnt', type=int, default=1000, help='Number of history records to analyze')
    parser.add_argument('--num_guess', type=int, default=100, help='Number of guesses to make')
    parser.add_argument('--baseMoney', type=int, default=1000, help='Base Money for Lottery')
    parser.add_argument('--single_bet_cost', type = int, default=2, help='The cost of single bet')
    parser.add_argument('--bet_times', type= int, default=5, help='The times of bet')

    args = parser.parse_args()

    analyzer = LotteryAnalyzer(args.csvfile, args.hist_cnt)
    # print(f"Read {len(analyzer.data)} rows of lottery history data from {args.csvfile}")
    analyzer.play_guess_game(args.baseMoney, args.num_guess,args.single_bet_cost, args.bet_times)




def checkLottery( act_red_balls: List[str], act_blue_ball: str, guess_red_balls: List[str], guess_blue_ball: str, single_cost: int = 2, times: int = 5) -> int:
    """
    Check the result of a lottery guess.
    Returns the number of correct guesses.
    """
    rewardLevel = 0
    cost = single_cost * times
    red_correct = len([x for x in act_red_balls if x in guess_red_balls])
    blue_correct = 1 if act_blue_ball == guess_blue_ball else 0
    if blue_correct == 0 :
        if red_correct <4 :
            rewardLevel = 0;
        else:
            if red_correct == 4:
                rewardLevel =5
            elif red_correct == 5:
                rewardLevel = 4
            elif red_correct == 6:
                rewardLevel = 2
    else:
        if red_correct == 3:
            rewardLevel = 5
        elif red_correct == 4:
            rewardLevel = 4
        elif red_correct == 5:
            rewardLevel = 3
        elif red_correct == 6:
            rewardLevel = 1
        else:
            rewardLevel = 6
    

    if rewardLevel == 0:
            ret= 0 - cost
    elif rewardLevel == 6:
        ret = 5 * times - cost
    elif rewardLevel == 5:
        ret = 10 * times - cost
    elif rewardLevel == 4:
        ret = 200 * times - cost
    elif rewardLevel == 3:
        ret = 3000 * times - cost
    elif rewardLevel == 2:
        ret = 5000000 * times - cost
    elif rewardLevel == 1:
        ret = 10000000 * times - cost
    else:
        ret = 0 - cost
    
    return ret
            



    
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



  
    




if __name__ == '__main__':
    main()
