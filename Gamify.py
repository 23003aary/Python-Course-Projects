def initialize():
    '''Initializes the global variables needed for the simulation.'''
#store current hedons and health points
    global cur_hedons, cur_health
#  measure time elapsed, store previous activities
    global cur_time, previous_activities
#store last activity conducted
    global last_finished
#store whether user is bored with star
    global bored_with_stars
#set initial values of cur_health and cur_hedons to 0
    cur_hedons = 0
    cur_health = 0
#store current star, current star activity, star offer times
    global cur_star, cur_star_activity, star_offer_times
#set initial values of cur_star, cur_star_activity and star_offer_times
    cur_star = None
    cur_star_activity = None
    star_offer_times = []
# set bored_with_stars to False to initialize
    bored_with_stars = False
# set previous_activities to an empty list to initialize
    previous_activities = []
#store the last tiring activity
    global last_tiring_activity
# store the time at which last tiring activity was finished
    global last_tiring_activity_finished
#set initial value of last_tiring_activity
    last_tiring_activity = None
#set time of last_tiring_activity_finished to a very low number to initialize
    last_tiring_activity_finished = -1000
# set initial time in cur_time as 0
    cur_time = 0
# set initial value of time of last_finished
    last_finished = -1000

def is_tired():
  ''' returns true if user has done activity 'running' or 'textbooks' for the last 120 minutes or more
  returns false otherwise'''
  global last_tiring_activity_finished, cur_time
  if cur_time - last_tiring_activity_finished <= 120:
    return True
  return False


def estimate_hedons_delta(activity, duration):
    ''' compute the number of hedons according to rules on activity 'running', 'textbooks', 'resting'
    save calculated number of hedons in variable hedons '''
    global cur_time, cur_star_activity, cur_star

    hedons = 0
    if activity == 'running' and not is_tired():
        hedons += 2*min(10, duration)
        hedons += -2*max(0, duration - 10)
    elif activity == 'textbooks' and not is_tired():
        hedons += 1*min(20, duration)
        hedons += -1*max(0, duration - 20)

    if star_can_be_taken(activity):
        hedon_minutes = min(10, duration)
        hedons += hedon_minutes * 3

    if is_tired() and activity != 'resting':
        hedons += -2*duration

    return hedons


def cumulative_activity_time(activity):
  '''track all activties until present under an array '''
  '''Provide value of accumulated activites as a function of time '''
  global previous_activities

  i = len(previous_activities) - 1
  acc = 0
  while 0 <= i and previous_activities[i][0] == activity:
      acc += previous_activities[i][1]
      i -= 1
  return acc



def estimate_health_delta(activity, duration):
    '''
    computes change in health points according to activity and net duration
    '''
    global cur_health, previous_activities
    health_delta = 0
    if activity == 'running':
        additional = cumulative_activity_time('running')
        if additional + duration < 180:
            health_delta += 3 * duration
        elif additional >= 180:
            health_delta += duration
        else:
            health_delta += 3 * (180 - additional)
            health_delta += additional + duration - 180

    elif activity == 'textbooks':
        health_delta += 2 * duration

    return health_delta


def perform_activity(activity, duration):
  '''Calculate total change in health and hedon points based on conditions of           each activity'''
  global cur_hedons, cur_health, cur_time, last_finished, previous_activities, last_tiring_activity_finished

  cur_health += estimate_health_delta(activity, duration)
  cur_hedons += estimate_hedons_delta(activity, duration)

  if cur_star_activity:
      use_star()

  cur_time += duration
  last_finished = cur_time
  previous_activities.append((activity, duration))
  if activity != 'resting':
      last_tiring_activity_finished = cur_time



def get_cur_hedons():
    ''' return current hedons cur_hedons '''
    global cur_hedons
    return cur_hedons


def get_cur_health():
  '''Return value of total health points 'cur_health' '''
  global cur_health
  return cur_health


def star_can_be_taken(activity):
    '''returns True iff a star can be used to get more hedons for activity 'activity' iff no time passed between the star’s being offered and the activity, and the user is not bored with stars, and the star was offered for activity 'activity'.
    '''
    global cur_time, star_offer_times, bored_with_stars, cur_star_activity
    if not cur_star_activity:
        return False
    return not bored_with_stars and star_offer_times[-1] == cur_time and cur_star_activity == activity


def use_star():
    '''resets values of cur_star and cur_star_activity when star has been used '''
    global cur_star, cur_star_activity
    cur_star = None
    cur_star_activity = None


def offer_star(activity):
    '''Calculate if star will be offered based off of duration and activity'''
    global cur_time, star_offer_times, cur_star, cur_star_activity, bored_with_stars

    global cur_time, star_offer_times, cur_star, cur_star_activity, bored_with_stars

    if bored_with_stars:
        use_star()
        return

    if len(star_offer_times) >= 3 and cur_time - star_offer_times[-3] >= 120:
        bored_with_stars = True
        use_star()
        return

    cur_star = True
    cur_star_activity = activity
    star_offer_times.append(cur_time)


def most_fun_activity_minute():
    ''' store activity and number of hedons 'estimate_hedons_delta' in a     dictionary in fun
    sort fun in descending order
    return the activity that yields most hedons
    '''
    activities = ['running', 'resting', 'textbooks']
    fun = {activity: estimate_hedons_delta(activity, 1) for activity in activities}
    return sorted(activities, key=lambda x: fun[x], reverse=True)[0]

################################################################################


if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons()) # -20 = 10 * 2 + 20 * (-2)
    print(get_cur_health()) # 90 = 30 * 3
    print(most_fun_activity_minute()) #resting
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute()) # running
    perform_activity("textbooks", 30)
    print(get_cur_health()) # 150 = 90 + 30*2
    print(get_cur_hedons()) # -80 = -20 + 30 * (-2)
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health()) # 210 = 150 + 20 * 3
    print(get_cur_hedons()) # -90 = -80 + 10 * (3-2) + 10 * (-2)
    perform_activity("running", 170)
    print(get_cur_health()) # 700 = 210 + 160 * 3 + 10 * 1
    print(get_cur_hedons()) # -430 = -90 + 170 * (-2)
    perform_activity("running", 160)
    perform_activity("running", 30)
    perform_activity("running", 30)
    perform_activity("running", 30)
    print(get_cur_health())
    print(get_cur_hedons())

