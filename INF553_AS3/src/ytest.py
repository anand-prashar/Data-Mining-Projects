import sys
import math

try:
    fd = open('ratings-dataset.tsv')
except:
    print "File cannot be opened"
    exit()
user_dic = {}
user_movie_list = []
user_list = []
user_name = '8ccfa5d6-6f0b-407f-a463-0e1f745f9dad'#sys.argv[2]
item_name = 'The Fugitive'#sys.argv[3]
k_value = 200#int(sys.argv[4])
# user_name = "Kluver"
# item_name = "The Fugitive"
# k_value = 10

for line in fd:
    line = line.strip()
    line = line.split("\t")
    user_movie_list.append(line)
    if line[0] not in user_list:
        user_list.append(line[0])
user_list.sort()


for i in user_movie_list:
    if i[0] not in user_dic:
        user_dic[i[0]] = [[i[2],i[1]]]
    else:
        user_dic[i[0]].append([i[2],i[1]])
# for i in user_dic.items():
#     print i
# print user_dic

def pearson_correlation(user1, user2):
    if user1 in user_dic.keys() and user2 in user_dic.keys():
        sum_user1_total = 0
        sum_user2_total = 0
        diff_total = 0
        user1_total = 0
        user2_total = 0
        num = 0
        user1_value = user_dic[user1]
        user2_value = user_dic[user2]
        for i in user1_value:
            for j in user2_value:
                if j[0] == i[0]:
                    num = num+1
                    sum_user1_total = sum_user1_total + float(i[1])
                    sum_user2_total = sum_user2_total + float(j[1])
        user1_ave = float(sum_user1_total / num)
        user2_ave = float(sum_user2_total / num)

        for i in user1_value:
            for j in user2_value:
                if j[0] == i[0]:
                    diff= (float(i[1]) - user1_ave)*(float(j[1]) - user2_ave)
                    diff_total = diff_total+diff
                    user1 = (float(i[1]) - user1_ave)**2
                    user1_total = user1_total + user1
                    user2 = (float(j[1]) - user2_ave)**2
                    user2_total = user2_total + user2

        sqr_user1 = math.sqrt(user1_total)
        sqr_user2 = math.sqrt(user2_total)
        weight = diff_total / (sqr_user1*sqr_user2)
        return weight
    else:
        return "could not find corresponding user"

a = pearson_correlation("Kluver","hi mom")

similarity1_list = []
similarity2_list = []
def K_nearest_neighbors(user1,k,item):
    if user1 in user_list:
        for i in user_list:
            if i != user1:
                user2_value = user_dic[i]
                for j in user2_value:
                    if j[0] == item:
                        similarity = pearson_correlation(user1, i)
                        similarity1_list.append([-similarity,i])

        similarity1_list.sort()
        for i in similarity1_list:
            similarity2_list.append([i[1],-i[0]])
        similarity_user = similarity2_list[:k]
        return similarity_user
    else:
        return "could not find corresponding user"

b = K_nearest_neighbors(user_name,k_value,item_name)
for i in b:
    print i[0],i[1]

def calculate_corated_mean(user1,user2):
    num = 0
    sum_user1_total = 0
    sum_user2_total = 0
    user1_value = user_dic[user1]
    user2_value = user_dic[user2]
    for i in user1_value:
        for j in user2_value:
            if j[0] == i[0]:
                num = num + 1
                sum_user1_total = sum_user1_total + float(i[1])
                sum_user2_total = sum_user2_total + float(j[1])
    user1_ave = float(sum_user1_total / num)
    user2_ave = float(sum_user2_total / num)

    return user1_ave, user2_ave

def Predict(user1, item, k_nearest_neighbors):
    user_total_weight = 0
    weight_total = 0
    sum = 0
    k_nearest = k_nearest_neighbors

    user1_value = user_dic[user1]
    for i in user1_value:
        sum = sum + float(i[1])
    ave_user1 = sum / len(user1_value)

    for i in k_nearest:
        user1_ave, user2_ave = calculate_corated_mean(user1, i[0])
        value = user_dic[i[0]]
        for j in value:
            if item == j[0]:
                value_rank = float(j[1])
                user_weight = (value_rank - user2_ave) *float(i[1])
                user_total_weight = user_total_weight+user_weight
                weight_total = weight_total + abs(float(i[1]))
    predict_value = ave_user1 + user_total_weight / weight_total

    return predict_value

c = Predict(user_name,item_name,b)
print c

