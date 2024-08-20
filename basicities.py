print("Daily routine")

day = int(input("Day :"))

if day == 1:
    print("Day1")
    workout = int(input("workout = "))
    waterintake = int(input("water intake = "))
    studied = int(input("studied = "))
    junk = int(input("junk = "))

    if(workout > 1):
        print("Workout is complete.")
    else:
        print("Workout isn't completed.")
    if(waterintake > 3):
        print("Water intake is complete.")
    else:
         print("Need to drink water.")
    if(studied > 1):
        print("Studied well!!")
    else:
         print("Need to study.")
    if(junk == 0):
        print("Avoided junk food")
    else:
         print("Avoid junk food")