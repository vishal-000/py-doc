def create_student_marks_dictionary():
    student_data = {}
    num_students = int(input("Enter the number of students :"))
    for i in range(num_students):
        name = input(f"Enter name for studen{i+1}:")
        try:
            marks = float(input(f"Enter marks for {name}:"))
            student_data[name] = marks
        except ValueError:
            print("Invalid marks entered.Please enter a numeric value.")
            continue
    return student_data
def display_student_marks(student_data):
    while True:
         search_name = input("\nEnter the name of the student to search for")
         if search_name.lower() == 'quit':
             break
         if search_name in student_data:
             print(f"Marks for {search_name}:{student_data[search_name]}")
        else:
            print(f"Student'{student_name}")

if __name__ == "__main__":
     print("\nComplete student marks dictionary :")
     print (student_dict)
        