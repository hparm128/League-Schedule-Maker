import random
import copy

# copied 11/15

league_size = int(input('How many teams are in your league? '))
season_length = int(input('How many games do you want your season to be? '))

length_minus_size = season_length-league_size+1

names = []

for num in range(league_size):
    team_name = input(f"Please enter team {num+1}'s team name: ")
    names.append(team_name)


def set_repeats():
    while True:
        try:
            repeats = []
            for num in range(league_size):
                repeats.append([])
            for team in repeats:
                nums = [n + 1 for n in range(league_size) if n != repeats.index(team)]
                for x in repeats:
                    if len(x) == length_minus_size and repeats.index(x)+1 in nums:
                        nums.remove(repeats.index(x) + 1)
                for um in range(length_minus_size):
                    if len(team) < length_minus_size:
                        r = random.choice(nums)
                        team.append(r)
                        repeats[r - 1].append(repeats.index(team) + 1)
                        if r in nums:
                            nums.remove(r)
            break
        except IndexError:
            pass

    return repeats


def set_schedule_with_repeats():
    teams = set_repeats()
    repeats = copy.deepcopy(teams)
    schedule = []
    non_repeat_games = []

    for num in range(1,league_size+1):
        non_repeat_games.append([n for n in range(1,league_size+1) if n != num])

    for num in range(league_size):
        schedule.append([])

        for n in range(season_length):
            schedule[num].append(0)

    for num in range(season_length):
        numbers = [n for n in range(1, league_size+1)]
        for ls in schedule:
            if ls[num] == 0:
                current = schedule.index(ls)+1

                # Create list of possible opponents for current team
                intersection = set(non_repeat_games[current-1]).intersection(set(numbers))
                repeat_intersection = set(repeats[current-1]).intersection(set(numbers))
                full_intersection = list(intersection) + list(repeat_intersection)
                full_intersection_set = set(full_intersection)
                full_intersection_list = list(full_intersection_set)

                # Remove set game from lists of games that need to be set for the current team and opponent
                numbers.remove(current)
                if len(full_intersection_list) > 0:
                    ls[num] = random.choice(full_intersection_list)
                    opponent = ls[num]
                    if opponent in non_repeat_games[current-1]:
                        non_repeat_games[current - 1].remove(opponent)
                    else:
                        repeats[current-1].remove(opponent)
                    if current in non_repeat_games[opponent-1]:
                        non_repeat_games[opponent-1].remove(current)
                    elif current in non_repeat_games[opponent-1]:
                        repeats[opponent-1].remove(current)
                    numbers.remove(opponent)

                    # Set opponents match-up to the current team
                    schedule[opponent-1][num] = current

    # Count errors
    fail_counter = 0
    for team_schedule in schedule:
        for game in team_schedule:
            if game == 0:
                fail_counter += 1

    return schedule, fail_counter


# Run schedule making code for the first time and find number of errors
run = set_schedule_with_repeats()
schedule = run[::league_size]
fail_counter = run[-1]

# Run schedule making code until there are zero errors
while fail_counter:
    run = set_schedule_with_repeats()
    schedule = run[::league_size]
    fail_counter = run[-1]

name_schedule = []

# Print results
for sch in schedule:
    for team_schedule in sch:
        name_schedule.append([names[opp-1] for opp in team_schedule])
        #print(f'Team {names[sch.index(team_schedule)]}: {team_schedule}')

for schedule in name_schedule:
    counter = 1
    print(f"{names[name_schedule.index(schedule)].upper()}'S SCHEDULE:")
    for g in schedule:
        print(f'Week {counter}: {names[name_schedule.index(schedule)]} vs. {g}')
        counter += 1