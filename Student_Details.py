def get_student_details():
    students = []
    n = int(input("Enter number of students: "))

    for i in range(n):
        print(f"\nEnter details for student {i + 1}:")
        roll_no = input("Roll Number: ")
        name = input("Name: ")
        age = input("Age: ")
        course = input("Course: ")

        students.append([roll_no, name, age, course])

    return students

def display_table(students):
    print("\nStudent Details")
    print("-" * 55)
    print(f"{'Roll No':<10}{'Name':<15}{'Age':<10}{'Course':<20}")
    print("-" * 55)

    for student in students:
        print(f"{student[0]:<10}{student[1]:<15}{student[2]:<10}{student[3]:<20}")

    print("-" * 55)


# Main program
students = get_student_details()
display_table(students)
