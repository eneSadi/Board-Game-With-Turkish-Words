class tree:
    def __init__(self, root_word, score = 0, children = None):
        self.root_word = root_word
        self.score = score
        self.children = children
        

def scoring(word):
    scores = {'a': 1,'b':3,'c':4,'ç':4,'d':3,
          'e':1,'f':7,'g':5,'ğ':8,'h':5,
          'ı':2,'i':1,'j':10,'k':1,'l':1,
          'm':2,'n':1,'o':2,'ö':7,'p':5,
          'r':1,'s':2,'ş':4,'t':1,'u':2,
          'ü':3,'v':7,'y':3,'z':4}
    
    score = 0
    for i in word:
        score += scores[i]
    return score

import pickle

def read_dict():
    a_file = open("turkish_dict.pkl", "rb")
    words_dict = pickle.load(a_file)
    return words_dict

import numpy as np

def mask_vocab(list_of_words, difficulty):
    
    len_list = len(list_of_words)
    
    if difficulty == 'very easy':
        return np.random.choice(list_of_words, int(len_list * 0.1))
    elif difficulty == 'easy':
        return np.random.choice(list_of_words, int(len_list * 0.2))
    elif difficulty == 'medium':
        return np.random.choice(list_of_words, int(len_list * 0.3))
    elif difficulty == 'hard':
        return np.random.choice(list_of_words, int(len_list * 0.6))
    elif difficulty == 'very hard':
        return np.random.choice(list_of_words, int(len_list * 0.99))

def create_tree(root_word, difficulty):
    
    if difficulty == 1:
        difficulty = 'very easy'
    elif difficulty == 2:
        difficulty = 'easy'    
    elif difficulty == 3:
        difficulty = 'medium'    
    elif difficulty == 4:
        difficulty = 'hard'
    elif difficulty == 5:
        difficulty = 'very hard'
    
    root = tree(root_word)
    children = []
    
    letter_for_dict = 'x'
    
    if root_word[-1] == 'ğ':
        letter_for_dict = 'g'
    else:
        letter_for_dict = root_word[-1]   
    
    masked_words = mask_vocab(words_dict[letter_for_dict], difficulty)
    
    for word in masked_words:
        tmp_node = tree(word)
        
        letter_for_dict_2 = 'x'
        if word[-1] == 'ğ':
            letter_for_dict_2 = 'g'
        else:
            letter_for_dict_2 = word[-1]
            
        maximum = 0
        for w in words_dict[letter_for_dict_2]:
            score_w = scoring(w)
            if score_w > maximum:
                maximum = score_w
        tmp_node.score = maximum 
    
        children.append(tmp_node)
        
    root.children = children
    return root

def choose_best_word(root, forbidden_words, max_len):
    min_score = root.children[0].score
    min_index = 0
    max_word = 'a'

    for i, child_node in enumerate(root.children):
        if child_node.score <= min_score:
            min_score = child_node.score
            min_index = i
            
            if (scoring(child_node.root_word) > scoring(max_word)) and (child_node.root_word not in forbidden_words) and len(child_node.root_word) <= max_len:
                max_word = child_node.root_word
    return max_word
    
def make_board(size):
    return [[" " for i in range(size)] for j in range(size)]

def print_board(board,user_score, agent_score):
    print("-"*50)
    print("Sizin Skorunuz : ", user_score)
    print("Ajanın Skoru   : ", agent_score)
    print("-"*50)
    for j,row in enumerate(board):
        print(j,end="\t")
        for i,square in enumerate(row):
            if square == "☐":
                print(square, end = " ")
                row[i] = " "
            elif square != " ":
                print(square, end= " "),
            else:
                print('.', end= " "),
        print("")
    print("-"*50)
    
def put_board(board, board_size, word, start_x, start_y, direction):
    
    if start_x > board_size-1 or start_y > board_size-1:
        print("Tahtanın dışına kelime yazamazsınız!")
        return False,0,0
    
    
    len_word = len(word)
    if direction == 'right':
        if (start_y + len_word) > board_size:
            print("Kelime tahtaya sığmadı!")
            return False,0,0
        
        for i in range(len_word):
            if board[start_x][start_y + i] != ' ':
                print("Kelime diğer kelimelerden biriyle çakıştı!")
                return False,0,0
        for i in range(len_word):
            board[start_x][start_y + i] = word[i]
            
        return True, start_x, start_y+len_word-1
    
    if direction == 'left':
        if (start_y - len_word) < -1:
            print("Kelime tahtaya sığmadı!")
            return False,0,0
        
        for i in range(len_word):
            if board[start_x][start_y - i] != ' ':
                print("Kelime diğer kelimelerden biriyle çakıştı!")
                return False,0,0 
        for i in range(len_word):
            board[start_x][start_y - i] = word[i]
        
        return True, start_x, start_y-len_word+1
    
    if direction == 'up':
        if (start_x - len_word) < -1:
            print("Kelime tahtaya sığmadı!")
            return False,0,0
        
        for i in range(len_word):
            if board[start_x - i][start_y] != ' ':
                print("Kelime diğer kelimelerden biriyle çakıştı!")
                return False,0,0 
        for i in range(len_word):
            board[start_x - i][start_y] = word[i]
        
        return True, start_x-len_word+1, start_y 
    
    if direction == 'down':
        if (start_x + len_word) > board_size:
            print("Kelime tahtaya sığmadı!")
            return False,0,0
        
        for i in range(len_word):
            if board[start_x + i][start_y] != ' ':
                print("Kelime diğer kelimelerden biriyle çakıştı!")
                return False,0,0 
        for i in range(len_word):
            board[start_x + i][start_y] = word[i]
        
        return True, start_x+len_word-1, start_y    
    
def max_space(board, board_size, x,y):
    max_space = 0
    direction = 'x'
    
    each = []
    
    count = 1
    for i in range(x+1,board_size):
        if board[i][y] == ' ':
            count += 1
        else:
            break
    #print("down : ", count)
    each.append(count)
    if count > max_space:
        max_space = count
        direction = 'down'
    
    count = 1
    ctrl = 0
    for i in range(x-1,0,-1):
        
        if board[i][y] == ' ':
            count += 1
        else:
            ctrl = 1
            break
    if ctrl == 0:
        count += 1
            
    #print("up : ", count)       
    each.append(count)
    if count > max_space:
        max_space = count
        direction = 'up'
    
    count = 1
    for i in range(y+1,board_size):
        if board[x][i] == ' ':
            count += 1
        else:
            break
    #print("right : ", count)        
    each.append(count)
    if count > max_space:
        max_space = count
        direction = 'right'
    
    count = 1
    ctrl = 0
    for i in range(y-1,0,-1):
        if board[x][i] == ' ':
            count += 1
        else:
            ctrl = 1
            break
    if ctrl == 0:
        count += 1
        
    #print("left : ", count)
    each.append(count)
    if count > max_space:
        max_space = count
        direction = 'left'
        
    return direction, max_space, each


import random

def game_with_board(board_size):
    print("-"*50)
    print("Tahta Üzerinde Kelimelik Oyununa Hoş Geldiniz!")
    print("- Kelimeleriniz Türkçe olmalıdır.")
    print("- İlk tur hariç karşı tarafın yazdığı kelimenin bittiği yerden itibaren, tahtanın boş olan kısmına\n'aşağı', 'yukarı', 'sağ', 'sol' yönlerinde kelimeler yazabilirsiniz.")
    print("- Başarısız deneme hakkınız 5'tir, bunun üzerinde deneme yaparsanız oyun sonlanır.")
    print("- Oyundan çıkmak için sıra sizdeyken '.' karakterini girmeniz gerekmektedir.")
    print("-"*50)
    print("\nBaşlamak için herhangi bir tuşa basınız...")
    input()
    
    #clear_output(wait=True)
    
    print("Bir zorluk seviyesi seçiniz : ")
    print("1 -> Çok Kolay\n2 -> Kolay\n3 -> Orta\n4 -> Zor\n5 -> TDK'de Çalışıyorum")
    difficulty = int(input())
    while difficulty not in [1,2,3,4,5]:
        print("Geçersiz zorluk düzeyi seçimi! Tekrar seçiniz...")
        difficulty = int(input())
    
    #clear_output(wait=True)
    
    board = make_board(board_size)
    initial_x = random.randint(0,board_size-1)
    initial_y = random.randint(0,board_size-1)
    board[initial_x][initial_y] = '☐'
    
    user_score = 0
    agent_score = 0
    print_board(board, user_score, agent_score)
    
    toggle = 1 # 0 - user | 1 - agent
    
    forbidden_words = []
    user_trying = 1
    user_word = input('İlk kelimeyi giriniz: ')
    if user_word == '.':
        print("Çıkış yapılıyor...")
        return
        
    while (user_word[0] not in words_dict.keys()) or (user_word not in words_dict[user_word[0]]):
        if (user_word[0] not in words_dict.keys()):
            print("Türkçe karakterler kullanınız!")
            user_word = input('İlk kelimeyi giriniz: ')
        elif (user_word not in words_dict[user_word[0]]):
            print("Sözlükte bulunan bir kelime giriniz...")
            user_word = input('İlk kelimeyi giriniz: ')
        if user_word == '.':
            print("Çıkış yapılıyor...")
            return
        user_trying += 1
        if user_trying >= 5:
            print('Deneme Hakkınız ve Oyun Bitti!')
            if agent_score>=user_score:
                print("Ajan Kazandı!")
            else:
                print("Siz Kazandınız!")
            return

    ctrl_dir = False
    while ctrl_dir == False:
        direction  = input("Yön seçiniz : ")
        if direction == "sağ":
            ctrl_dir,last_x,last_y = put_board(board,board_size,user_word, initial_x, initial_y, 'right')
        elif direction == "sol":
            ctrl_dir,last_x,last_y = put_board(board,board_size,user_word, initial_x, initial_y, 'left')
        elif direction == "yukarı":
            ctrl_dir,last_x,last_y = put_board(board,board_size,user_word, initial_x, initial_y, 'up')
        elif direction == "aşağı":
            ctrl_dir,last_x,last_y = put_board(board,board_size,user_word, initial_x, initial_y, 'down')
        else:
            print("Yön olarak aşağı, yukarı, sağ veya sol giriniz!")
    
    user_score = scoring(user_word)
    forbidden_words.append(user_word)
    agent_score = 0
    #clear_output(wait=True)
    print_board(board, user_score, agent_score)
    
    while(True):
        if toggle == 1:
            print("Ajan düşünüyor...")
            root = create_tree(user_word, difficulty)
            #print(last_x,last_y)
            direction, max_len, each = max_space(board,board_size, last_x, last_y)
            agent_word = choose_best_word(root, forbidden_words, max_len)
            
            if agent_word == 'a':
                print('Ajanı Köşeye Sıkıştırdın!')
                if agent_score>=user_score:
                    print("Ajan Kazandı!")
                else:
                    print("Siz Kazandınız!")                
                return
            
            print("Ajanın Kelimesi : ", agent_word)
            
            if direction == 'right':
                _,last_x,last_y = put_board(board,board_size,agent_word[1:], start_x=last_x, start_y=last_y+1,direction=direction)
            elif direction == 'left':
                _,last_x,last_y = put_board(board,board_size,agent_word[1:], start_x=last_x, start_y=last_y-1,direction=direction)
            elif direction == 'up':
                _,last_x,last_y = put_board(board,board_size,agent_word[1:], start_x=last_x-1, start_y=last_y,direction=direction)
            elif direction == 'down':
                _,last_x,last_y = put_board(board,board_size,agent_word[1:], start_x=last_x+1, start_y=last_y,direction=direction)
            
            agent_score += scoring(agent_word)
            toggle = 0
            #clear_output(wait=True)
            print_board(board,user_score,agent_score)
            
            forbidden_words.append(agent_word)
            
            if len([i for i in each if i < 2]) == 4:
                print('Oyun Bitti!')
                if agent_score>=user_score:
                    print("Ajan Kazandı!")
                else:
                    print("Siz Kazandınız!")
                return
        
        _, max_len, _= max_space(board,board_size, last_x, last_y)
        user_trying = 1
        if toggle == 0:            
            user_word = input('Kelimeniz: ')
            if user_word == '.':
                print("Çıkış yapılıyor...")
                return
            #print(user_word not in words_dict[user_word[0]])
            while (user_word[0] not in words_dict.keys()) or (user_word not in words_dict[user_word[0]]) or (user_word[0] != agent_word[-1]) or (user_word in forbidden_words) or (len(user_word) > max_len):
                if (user_word[0] not in words_dict.keys()):
                    print("Türkçe karakterler kullanınız!")
                elif (user_word[0] != agent_word[-1]):
                    print("Son kelimenin son harfiyle başlayan bir kelime giriniz!")
                elif (user_word not in words_dict[user_word[0]]):
                    print("Sözlükte bulunan bir kelime giriniz!")
                elif (user_word in forbidden_words):
                    print("Daha önce kullanılmayan bir kelime giriniz!")
                elif (len(user_word) > max_len):
                    print("Bu kelime hiçbir yönde yazılamaz!")
                user_trying += 1
                if user_trying >= 5:
                    print('Deneme Hakkınız ve Oyun Bitti!')
                    if agent_score>=user_score:
                        print("Ajan Kazandı!")
                    else:
                        print("Siz Kazandınız!")
                    return
                user_word = input('Kelimeniz: ')
                if user_word == '.':
                    print("Çıkış yapılıyor...")
                    return
            #print("Last X = ",last_x, "Last Y = ", last_y)
            ctrl_dir = False
            while ctrl_dir == False:
                direction  = input("Yön seçiniz : ")
                if direction == "sağ":
                    ctrl_dir,last_x_tmp,last_y_tmp = put_board(board,board_size,user_word[1:], last_x, last_y+1, 'right')
                elif direction == "sol":
                    ctrl_dir,last_x_tmp,last_y_tmp = put_board(board,board_size,user_word[1:], last_x, last_y-1, 'left')
                elif direction == "yukarı":
                    ctrl_dir,last_x_tmp,last_y_tmp = put_board(board,board_size,user_word[1:], last_x-1, last_y, 'up')
                elif direction == "aşağı":
                    ctrl_dir,last_x_tmp,last_y_tmp = put_board(board,board_size,user_word[1:], last_x+1, last_y, 'down')
                else:
                    print("Yön olarak aşağı, yukarı, sağ veya sol giriniz!")

            forbidden_words.append(user_word)
            user_score += scoring(user_word)
            toggle = 1
            
            #clear_output(wait=True)
            print_board(board, user_score, agent_score)
            last_x, last_y = last_x_tmp, last_y_tmp
            if len([i for i in each if i < 2]) == 4:
                print('Oyun Bitti!')
                if agent_score>user_score:
                    print("Ajan Kazandı!")
                else:
                    print("Siz Kazandınız!")
                return



if __name__ == "__main__":

    words_dict = read_dict()
    game_with_board(20) 
    print("\n\nÇıkmak için herhangi bir tuşa basınız...")
    print("\n\ndeveloped by sadi\n\n")
    input()