import random
import math
import time


game_map = []
active_tokens = []
colors = {"Red" , "Green", "Blue", "Yellow"}
BASESPEED = 300
states = {"Blocked", "Active"}
TIME_PER_FRAME = 300 ## miliseconds per frame

X = 0 #Eliminar



def check_state(state):
    if state not in states:
        print("Wrong state value for token")
        exit()
    

def init_game_map(l = 10,c = 7):
    global game_map 
  
    for x in range(c):     
        game_map.append([])
        for y in range(l):
            game_map[x].append(0)


def print_game_map():
    for y in range(len(game_map[0])):
        linha = ""     
        for x in range(len(game_map)):

            # Se for um dicionario, então nesta posição do mapa temos um token
            if type(game_map[x][y]) is dict:
                color = game_map[x][y]["Color"][0]  # Dar a primeira letra da color do token
                linha += color + " "
            else:
                linha += str(game_map[x][y]) + " "
        print(linha)

def spawn_token():
    ## Cria um token na linha 0 e numa coluna aleatória
    y = 0
    #x = math.floor(random.random() * 7)
    global X
    

    if ( game_map[1][8] != 0):
        X = 2
        
    ## Cria uma cor aleatória 
    #color = random.choice(list(colors))

    color = "Red"
    speed = BASESPEED
    state = "Active"
    remaining_time = speed
    check_state(state)

    token = { "Position": (X,y),
               "Color": color,
               "Speed": speed,
               "State": state,
               "Remaining_Time": remaining_time}

    
  
    X = X + 1
    X = X % 2


    return token

#Função que remove um token do map
def remove_token_from_map(token):
    pos_x = token["Position"][0]
    pos_y = token["Position"][1]

    game_map[pos_x][pos_y] = 0



def activate_floating_tokens():
    global game_map
    for y in range(len(game_map[0])):    
        for x in range(len(game_map)):
            if game_map[x][y] != 0:
                if y != len(game_map[0]) -1:
                    if game_map[x][y+1]==0:
                        game_map[x][y]["State"] = "Active"
                        active_tokens.append(game_map[x][y])  ## Coloca no active tokens para atualizar a posição do token no ciclo do update


def check_colisions(position, token):
    _state = token["State"]
    if position[1] == len(game_map[0]):
        _state = "Blocked"
    else:
        #Teste se há uma colisão com um token abaixo
        #Só testa se a new position ainda está dentro do numero de linhas do mapa
        if game_map[position[0]][(position[1])] != 0: 
            _state = "Blocked"  

    if _state == "Blocked":
        # Testar 3 ou mais em linha


        tokens_in_line_vertical = [token]
        #Ver quais os tokens em baixo
        x = token["Position"][0]
        y = token["Position"][1]

        found_token = True
        while ( found_token ):
            #Token na posição abaixo
            found_token = False
            y = y+1
            if y >= len(game_map[0]):  # testar se já passou os limites do game_map
                break

            if (game_map[x][y] != 0):
                tokens_in_line_vertical.append(game_map[x][y])  ## Se em baixo não for vazio, então há um token e guardamos ele numa lista
                found_token = True
        
    
        tokens_in_line_horizontal = [token]
        #Ver quais os tokens em baixo
        x = token["Position"][0]
        y = token["Position"][1]

        found_token = True
        while ( found_token ):
            #Token na posição abaixo
            found_token = False
            x = x+1
            if x >= len(game_map):  # testar se já passou os limites do game_map
                break

            if (game_map[x][y] != 0):
                tokens_in_line_horizontal.append(game_map[x][y])  ## Se em baixo não for vazio, então há um token e guardamos ele numa lista
                found_token = True
        
        x = token["Position"][0]
        y = token["Position"][1]

        found_token = True
        while ( found_token ):
            #Token na posição abaixo
            found_token = False
            x = x-1
            if x < 0:  # testar se já passou os limites do game_map
                break

            if (game_map[x][y] != 0):
                tokens_in_line_horizontal.append(game_map[x][y])  ## Se em baixo não for vazio, então há um token e guardamos ele numa lista
                found_token = True




        if (len(tokens_in_line_vertical)>=3):
            for tk in tokens_in_line_vertical:
                remove_token_from_map(tk)
                
        if (len(tokens_in_line_horizontal)>=3):

            for tk in tokens_in_line_horizontal:
                remove_token_from_map(tk)
            activate_floating_tokens()
                


    return _state

def update_token_position(token):
    ## Subtrair ao remaining time o tempo por frame
    new_position = token["Position"]
    new_remaining_time = math.floor(token["Remaining_Time"] - TIME_PER_FRAME) 
    new_state = token["State"]
    
    if new_remaining_time <= 0:
        new_position = (new_position[0], new_position[1] +1)
        new_remaining_time = math.floor(token["Speed"] - abs(new_remaining_time))  #retirar o excesso de tempo na contagem do tempo que permanece no proxima posição

        new_state = check_colisions(new_position, token)
        ## TODO check de colisoes


    new_token = { "Position": new_position,
                  "Color": token["Color"],
                  "Speed": token["Speed"],
                  "State": new_state,
                  "Remaining_Time": new_remaining_time}


    return new_token

def update():

    while(True):
        time.sleep(TIME_PER_FRAME/1000)

        ## Retirar token ativos
        global game_map
        if (active_tokens == []): ## Só é chamado para criar um novo token, quando não há tokens ativos
            new_token = spawn_token()
            active_tokens.append(new_token)
            position = new_token["Position"]
            x = position[0]
            y = position[1] 

            game_map[x][y]=new_token

        size = len(active_tokens)
        for i in range(size):

            if i >=  len(active_tokens):
                continue


            token = active_tokens[i]
            new_token = update_token_position(token)
            if new_token["State"]=="Blocked":
                active_tokens.pop(i)
               
                ## Esta condição é feita para evitar a situação em que completa 3 ou mais em linha e os tokens são eliminados do game map
                ## Neste caso não podemos fazer a substituição do estado para blocked porque o token já não existe
                if game_map[token["Position"][0]][token["Position"][1]] != 0:  
                    game_map[token["Position"][0]][token["Position"][1]]["State"]="Blocked"
            else:    
                active_tokens[i] = new_token
                
                #Remove token do mapa
                token_pos_x = token["Position"][0]
                token_pos_y = token["Position"][1]
                game_map[token_pos_x][token_pos_y] = 0
                
                #adiciona o token atualizado na nova posição do mapa
                new_token_pos_x = new_token["Position"][0]
                new_token_pos_y = new_token["Position"][1]
                game_map[new_token_pos_x][new_token_pos_y] = new_token
            

        print_game_map()
        print("#####################################################################")
        

        

    


init_game_map()
update()


