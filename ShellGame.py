import random

player_count=int(input("Enter number of players [3-12]:"))
players=[]
player_data={}
gold=1000
starting_money=100

light_weight=random.randint(4,6)
heavy_weight=random.randint(9,12)

def register_players():
    global players,player_count
    if player_count<3 or player_count>12:
        print("Invalid number. Try again.")
        player_count=int(input("Enter number of players [3-12]:"))
        register_players()
    else:
        for n in range(1,player_count+1):
            name=input(f"Enter name of player {n}:")
            players.append(name)

register_players()

def get_choices():
    global player_data,bridge_limit,sabotage_count
    sabotage_count=0
    bridge_limit=random.randint(4*player_count-3,12*player_count+3)
    for player in players:
        while True:
            choice=input(f"{player}, choose heavy/light (h/l):").lower()
            if choice in ('light','l'):
                while True:
                    sabotage=input("Sabotage? (y/n):").lower()
                    if sabotage in ('y','yes','n','no'):
                        sabotage='y' if sabotage in ('y','yes') else 'n'
                        if sabotage=='y':
                            sabotage_count+=1
                        player_data[player]=[choice,sabotage,starting_money]
                        if player not in player_data:
                            player_data[player]=[choice,sabotage,starting_money]
                        else:
                            player_data[player][0]=choice
                            player_data[player][1]=sabotage
                        break
                    else:
                        print("Invalid. Try again.")
                break

            elif choice in ('heavy','h'):
                if player not in player_data:
                    player_data[player]=[choice,'n',starting_money]
                else:
                    player_data[player][0]=choice
                    player_data[player][1]='n'
                break
            else:
                print("Invalid. Try again.")

def evaluate_round():
    global player_count,players,player_data,total_weight
    total_weight=0
    for player,values in player_data.items():
        choice,sabotage,money=values
        if choice in ('light','l'):
            total_weight+=light_weight
        else:
            total_weight+=heavy_weight

    if total_weight<=bridge_limit:
        for player,values in player_data.items():
            choice,sabotage,money=values
            if sabotage=='y':
                money = 10
            if choice in ('light','l'):
                money+=20
            else:
                money+=80
            player_data[player]=[choice,sabotage,money]
        print("Total:",total_weight,"\nBridge:",bridge_limit,"\n",player_data,"\nEveryone survives!")
    else:
        for player,values in list(player_data.items()):
            choice,sabotage,money=values
            if choice in ('heavy','h'):
                del player_data[player]
                players.remove(player)
        for player,values in list(player_data.items()):
            choice,sabotage,money=values
            if sabotage=='y':
                money*=2
            if choice in ('light','l'):
                money+=20
            player_data[player]=[choice,sabotage,money]
        print("Total:",total_weight,"\nBridge:",bridge_limit,"\n",player_data,"survive!")
        player_count=len(players)

def determine_winner():
    if len(player_data)==0:
        print("All players died. No winner.")
        return
    money_values=[player_data[p][2] for p in player_data]
    max_money=max(money_values)
    winners=[p for p in player_data if player_data[p][2]==max_money]
    if len(winners)==1:
        print("Winner:",winners[0],"with",max_money,"money!")
    else:
        print("Tie between:",winners,"with",max_money,"money each!")

def deadlock():
    final_results={}
    for player in players:
        while True:
            decision=input(f"{player}, Share or Steal?").lower()
            if decision in ('share','steal'):
                final_results[player]=[decision,player_data[player][2]]
                break
            else:
                print("Invalid. Try again.")
    p1=players[0]
    p2=players[1]
    d1=final_results[p1][0]
    d2=final_results[p2][0]
    if d1=='share' and d2=='share':
        final_results[p1][1]+=gold/2
        final_results[p2][1]+=gold/2
    elif d1=='share' and d2=='steal':
        final_results[p2][1]+=gold
    elif d1=='steal' and d2=='share':
        final_results[p1][1]+=gold
    else:
        final_results[p1][1]/=2
        final_results[p2][1]/=2
    print(final_results)
    player_data[p1][2]=final_results[p1][1]
    player_data[p2][2]=final_results[p2][1]
    determine_winner()

get_choices()
evaluate_round()
while player_count>2:
    if len(players)==0:
        print("All players died. No winner.")
        exit()
    get_choices()
    evaluate_round()
if player_count==2:
    deadlock()
else:
    determine_winner()
