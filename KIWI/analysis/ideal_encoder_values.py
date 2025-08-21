t = 0
t_inc = 0.1
input_range = 90.0
deg = 0
data = []
time = []

sample_num = input_range / t_inc
deg_inc = input_range / sample_num

while deg <= input_range:
    data.append(round(deg,4))
    time.append(round(t,4))
    
    deg += deg_inc
    print(deg)
    #t += t_inc






