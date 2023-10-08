import random
import math

def is_web():
    return "__BRYTHON__" in globals()

def write(message, end='\n'):
    if is_web():
        from browser import document
        console = document.getElementById('console')
        p = document.createElement('p')
        p.textContent = '> ' + message
        console.appendChild(p)
        console.scrollTop = console.scrollHeight
    else:
        print(message, end=end)


async def read():
    if is_web():
        from browser import document, aio
        inp = document.getElementById('input')
        while True:
            event = await aio.event(inp, 'keydown')
            if event.key == 'Enter':
                tmp = event.target.value
                event.target.value = ''
                write(tmp)
                return tmp
    else:
        return input()
    
def run(function):
    if is_web():
        from browser import aio
        aio.run(function())
    else:
        import asyncio
        asyncio.run(function())

def create_deck(n):
    # Создаем колоду из чисел от 1 до n
    deck = list(range(1, n + 1))
    return deck

def shuffle_deck(deck):
    # Перемешиваем колоду
    # random.shuffle(deck)
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]
    return deck

def deal_hand(deck, num):
    # Раздаем руку игроку или компьютеру
    hand = []
    for _ in range(num):
        card = deck.pop()
        hand.append(card)
    return hand

async def main():
    write("GUESS-IT")
    write("CREATIVE COMPUTING")
    write("MORRISTOWN, NEW JERSEY")
    write("")

    write("DO YOU WANT INSTRUCTIONS? TYPE YES OR NO")
    instructions = await read()
    if instructions == "YES":
        write("THE OBJECT OF THIS GAME IS TO GUESS AN UNKNOWN NUMBER")
        write("CALLED THE 'DOWN NUMBER'.  THE GAME IS PLAYED WITH THE")
        write("NUMBERS 1 TO 11. YOU WILL BE GIVEN A HAND OF 5")
        write("RANDOMLY SELECTED NUMBERS BETWEEN 1 AND 11 . THE ")
        write("COMPUTER WILL HAVE A SIMILAR HAND.  THE DOWN NUMBER WILL ")
        write("ALWAYS BE THE NUMBER NOT IN EITHER PLAYER HANDS.")
        write("")
        write("YOU ALTERNATE MOVES WITH THE COMPUTER. ON ANY MOVE THERE")
        write("ARE TWO OPTIONS- GUESS THE DOWN NUMBER OR ASK ABOUT SOME ")
        write("NUMBER")
        write("")
        write("WHEN A PLAYER GUESSES THE DOWN NUMBER THE GAME STOPS.")
        write("IF THE GUESS IS CORRECT THAT PLAYER WINS.")
        write("IF THE GUESS IS NOT CORRECT THAT PLAYER LOSES.")
        write("")
        write("ALL QUESTIONS ABOUT NUMBERS IN THE OTHER PLAYERS HAND")
        write("MUST BE ANSWERED TRUTHFULLY.  A PLAYER MAY'BLUFF' BY")
        write("ASKING ABOUT A NUMBER IN HIS OWN HAND.  THE COMPUTER")
        write("WILL SOMETIMES DO THIS.")
        write("")
        write("A NUMBER MAY BE ASKED ABOUT ONLY ONCE.")
        write("")
        write("GOOD LUCK")
    elif instructions != "NO":
        write("Invalid input")

    while True:
        deck = create_deck(10)  # Создаем новую колоду в начале каждой игры
        shuffle_deck(deck)
        player_hand = deal_hand(deck.copy(), 5)  # Копируем колоду для раздачи
        computer_hand = deal_hand(deck.copy(), 5)  # Копируем колоду для раздачи
        down_number = deck.pop()
        tmp = str(player_hand)

        write("YOUR HAND IS:" + tmp)
        write("")

        player_turn = True
        guess = None

        while True:
            if player_turn:
                write("YOUR TURN")
                write("Do you want to GUESS the DOWN NUMBER? YES or NO")
                action = await read()
                if action == "YES":
                    write("What is your guess for the DOWN NUMBER?")
                    guess = int(await read())
                    if guess == down_number:
                        write("YOUR GUESS IS CORRECT - YOU WIN!")
                    else:
                        write("YOUR GUESS IS NOT CORRECT - YOU LOSE!")
                    break
                elif action != "NO":
                    write("Invalid input")
                    continue

                write("Which number do you want to ask about?")
                number = int(await read())

                if number not in player_hand:
                    write("IS NOT IN YOUR HAND")
                else:
                    write(str(number) + " IS IN YOUR HAND")
                    player_hand.remove(number)
                    computer_hand.append(number)

            else:
                write("COMPUTER'S TURN")
                if random.random() > 1 / (1 + len(computer_hand) * math.comb(len(computer_hand), len(player_hand) - 1)):
                    write("I WANT TO GUESS THE DOWN NUMBER")
                    if down_number in computer_hand:
                        write("I GUESS " + str(down_number) + " - I WAS WRONG... YOU WIN!")
                    else:
                        write("I GUESS " + str(down_number) + " - I WAS CORRECT... YOU LOSE!")
                    break
                else:
                    write("I WANT TO ASK ABOUT A NUMBER")
                    number = random.choice(computer_hand)
                    write("DO YOU HAVE" + str(number) + " ? YES or NO")
                    answer = await read()
                    if answer == "YES":
                        write("YOU HAVE" + str(number))
                        player_hand.append(number)
                        computer_hand.remove(number)
                    else:
                        write("I GUESS" + str(number) + " WAS NOT A BLUFF")
                        computer_hand.remove(number)

            player_turn = not player_turn

        write("DO YOU WANT TO PLAY AGAIN? YES or NO")
        play_again = await read()
        if play_again == "NO":
            break

run(main)