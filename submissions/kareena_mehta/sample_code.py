#!/usr/bin/env python3
"""
This file is just for trying out the Emotion-Driven Code Review Assistant.
It shows different ways developers feel when coding.
"""

import math
import random

# This is such a mess, I don't even know where to begin
def calculate_area(r):
    # TODO: need to handle negative radius values (why are there always weird cases?)
    # Why didn't I just use a library for this?
    return math.pi * r * r  # at least this part works, I guess...

# I'm actually proud of this function! It's so clean and easy to understand
def generate_random_numbers(count=10):
    """Makes a list of random numbers - something that actually worked on the first try!"""
    return [random.randint(1, 100) for _ in range(count)]

# This is a really bad hack but I got a deadline tomorrow and I'm so tired
def parse_data(raw_data):
    # FIXME: this will probably break with bad input but whatever, not my problem now
    # I hate regex but here we are again, what can you do
    import re
    
    # Another super clever piece of code (just kidding, it's bad)
    pattern = r'(\d+),(\w+)'  # I hope this catches everything, fingers crossed
    matches = re.findall(pattern, raw_data)
    
    # TODO: add proper error handling instead of just hoping it works
    return [(int(num), name) for num, name in matches]

# I'm actually feeling good about this one - clean recursion!
def fibonacci(n):
    """Calculates fibonacci number - using recursion because I enjoy elegant solutions"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # perfect, just like in the textbook!

# This function gives me bad dreams but it kinda works, somehow
def mysterious_algorithm(data):
    # I found this answer on Stack Overflow and I still don't understand it
    # But all the tests pass so I'm just keeping it (please don't judge me)
    
    result = []
    temp = data.copy()  # I'm copying it just in case, because I've messed this up before
    
    # Something magical is happening here (seriously, I really don't get this part)
    for i in range(len(temp)):
        # This loop is probably inefficient but I'm too scared to try to make it faster
        for j in range(i+1, len(temp)):
            if temp[i] > temp[j]:
                temp[i], temp[j] = temp[j], temp[i]  # is this bubble sort? in 2024? I know, right...
    
    # TODO: need to look up better ways to sort stuff when I have more mental capacity
    return temp

# Finally! A function I'm actually excited about
def create_user_profile(name, age, interests):
    """
    Make a user profile dictionary - I love how clean this came out!
    This function makes me happy inside
    """
    profile = {
        'name': name,
        'age': age,
        'interests': interests,
        'created_at': 'today',  # this is good enough, for now anyway
        'active': True
    }
    
    # Some checking that makes actual sense
    if age < 0:
        raise ValueError("Age cannot be negative - basic logic wins!")
    
    return profile

# I give up on this function, it's totally cursed or something
def broken_calculator(a, b, operation):
    # Every single time I touch this function, something new breaks
    # It's like that game whack-a-mole but with bugs instead of moles
    
    ops = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,  # this used to work, but now it doesn't for some reason
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else float('inf')  # lazy error handling, don't judge
    }
    
    # TODO: I really need to rewrite this whole function from scratch
    # FIXME: when you divide by zero it acts weird
    # NOTE: to whoever is reading this code, I am very sorry
    
    if operation in ops:
        return ops[operation](a, b)
    else:
        return "Invalid operation"  # giving up on making proper error types, it's too hard

if __name__ == "__main__":
    # A quick test because I don't even trust anything anymore, honestly
    print("Testing all this chaos...")
    
    # This should work (famous last words, right?)
    print(f"Area of circle: {calculate_area(5)}")
    
    # I'm feeling pretty good about this one actually
    print(f"Random numbers: {generate_random_numbers(5)}")
    
    # I'm holding my breath for this test, I really hope it passes
    test_data = "123,Alice 456,Bob 789,Charlie"
    parsed = parse_data(test_data)
    print(f"Parsed data: {parsed}")
    
    # This is like, the only good part in this whole file
    profile = create_user_profile("Test User", 25, ["coding", "coffee", "debugging"])
    print(f"User profile: {profile}")
    
    print("If you see this message, then actual miracles happened!")