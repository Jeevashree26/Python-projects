import random
import math

start_number = int(input("Enter start_number:- "))

end_number = int(input("Enter end_number:- "))

x = random.randint(start_number, end_number)
print("\n\tYou've ", 
	round(math.log(end_number - start_number + 1, 2)),
	" chances to guess the number!\n")

count = 0

while count < math.log(end_number - start_number + 1, 2):
	count += 1

	guess = int(input("Guess a number:- "))

	if x == guess:
		print("Congratulations you found the number within ",
			count, " try")
		break
	elif x > guess:
		print("You guessed too small!")
	elif x < guess:
		print("You Guessed too high!")

if count >= math.log(end_number - start_number + 1, 2):
	print("\nThe number is %d" % x)
	print("\tBetter Luck Next time!")
