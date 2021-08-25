# Counting Max-Complexity Patterns!
# Zye 2021-08-22
#
# Uses a method slightly different from video.
# At each step, it first checks number of possible positions for each slope to be in.
# Might be a bit more efficient for larger grids?
# (but it still uses recurrent code so it gets really slow)

import math

WIDTH = 3
HEIGHT = 3

############################
#### SIMPLE CALCULATION ####
############################

# calculate slope
# string 'nan' for special value (infinity)
def calc_slope(dot1, dot2) :
  if dot2[0] == dot1[0] : return 'nan'
  return (dot2[1] - dot1[1]) / (dot2[0] - dot1[0])

# convert pattern to string
# [[0,0], [0,1], [0,2]] => "123"
def pattern_to_string(pattern) :
  string = ''
  for dot in pattern :
    string += str(dot[1]*WIDTH + dot[0] + 1) + ' '
  return string

##########################
#### GET INFO OF GRID ####
##########################

# get all points in w*h grid
# points have the form [x, y]
def get_dots(width, height) :
  points = []
  for x in range(width) :
    for y in range(height) :
      points.append([x, y])
  
  return points

# get all possible slopes in w*h grid
def get_slopes(width, height) :
  slopes = []
  # add horizontal / vertical
  if width > 1 : slopes.append(0)
  if height > 1 : slopes.append('nan')

  # add positive / negative slopes
  # we can just double the positive slopes
  for x in range(1, width) :
    for y in range(1, height) :
      if y/x not in slopes :
        slopes.append(y/x)
        slopes.append(-y/x)

  return slopes

# count number of possible positions for each slope to be in
# ex) in a 3x3 grid, slope 0 can be in 9 positions
def get_slope_count(width, height) :
  # initialize
  slope_count = {}
  for s in get_slopes(width, height) :
    slope_count[s] = 0

  # iterate for line segment with width=x and height=y
  for x in range(width) :
    for y in range(height) :
      if x == 0 and y == 0 : continue # not a valid line segment

      slope = calc_slope([0, 0], [x, y])
      slope_positions = (width - x) * (height - y) # number of positions the line segment can go in

      slope_count[slope] += slope_positions
      if slope != 0 and slope != 'nan' : # not horizontal or vertical
        slope_count[-slope] += slope_positions
  
  return slope_count  


############################
#### RECURRENT FUNCTION ####
############################

# recurrent function for get_maxcomp_patterns
def rec_maxcomp_patterns(used_dots, left_dots, left_slopes, slope_count) :
  new_slope_count = slope_count.copy()
  curr_dot = used_dots[-1] # current dot

  # final case
  if len(left_dots) == 1 :
    # print answer
    ans = pattern_to_string(used_dots + left_dots)
    print(ans)
    return [ans]
  
  # list of possible dots to go, sorted by slope
  # ex: {0.0: [[0, 0], [2, 0]]}
  possible_dots = {}
  for slope in left_slopes :
    possible_dots[slope] = []
  
  necessary_dot = []
  for d in left_dots :
    slope = calc_slope(curr_dot, d)
    if slope in left_slopes :
      
      # update possible_dots
      if possible_dots[slope] == [] :
        possible_dots[slope] = [d]
      else :
        dist_new = math.dist(curr_dot, d)
        dist_orig = math.dist(curr_dot, possible_dots[slope][0])
        if dist_new < dist_orig : possible_dots[slope] = [d]
        elif dist_new == dist_orig : possible_dots[slope].append(d)
    
      # update slope count
      new_slope_count[slope] -= 1

      # check if the dot is necessary
      if new_slope_count[slope] == 0 :
        if necessary_dot == [] :
          necessary_dot = d
        else : # two or more necessary dots: impossible
          return []

  # determine dots to run
  next_dots = []
  if necessary_dot == [] :
    for key in possible_dots :
      next_dots += possible_dots[key]
  else :
    next_dots = [necessary_dot]

  # recursive
  patterns = []
  for d in next_dots :
    slope = calc_slope(curr_dot, d)

    left_dots.remove(d)
    left_slopes.remove(slope)
    patterns += rec_maxcomp_patterns(used_dots + [d], left_dots, left_slopes, new_slope_count)
    left_slopes.append(slope)
    left_dots.append(d)
    
  return patterns


# get all max complexity patterns
def get_maxcomp_patterns(width: int, height: int) :
  dots = get_dots(width, height)
  slopes = get_slopes(width, height)
  slope_count = get_slope_count(width, height) # get candidates of all slopes

  patterns = []
  for start_dot in dots.copy() :
    dots.remove(start_dot)
    patterns += rec_maxcomp_patterns([start_dot], dots, slopes, slope_count) # add list of patterns
    dots.append(start_dot)
  return patterns


if __name__ == '__main__' :
  pattern_list = get_maxcomp_patterns(WIDTH, HEIGHT)
  print('number of max complexity patterns:', len(pattern_list))