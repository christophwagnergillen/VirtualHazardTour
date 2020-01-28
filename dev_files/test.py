#%%
import os
tour_file_directory="hazard_tours"
topic="Travel Impressions"
file_list=[]
file_index={}
num_pics=0
current_pic =6
next_pic=0
previous_pic=0
dir_names= next(os.walk("static/" + tour_file_directory))[1]
for name in dir_names:
    i=0
    files=next(os.walk("static/" + tour_file_directory + "/" + name))[2]
    file_list.append([name, files])
    file_index[name]=len(file_list[i][1])

# to be included in tour element
for key in file_index:
    if key == topic:
        num_pics = int(file_index[key])
if current_pic+1 > num_pics:
    previous_pic =current_pic
    current_pic=1
    next_pic= current_pic+1
elif current_pic+1 == num_pics:
    previous_pic=current_pic
    current_pic= num_pics
    next_pic= 1   
else:
    previous_pic=current_pic
    current_pic=current_pic+1
    next_pic=current_pic+1    

print(previous_pic,current_pic,next_pic)
#print (len(dir_names))    
#print(dir_names)
#print (file_list)   
#print (file_index)


# %%
