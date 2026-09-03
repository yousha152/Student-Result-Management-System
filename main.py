"""
Student Result Management System
A comprehensive portal for managing student records, grade calculations, 
and performance analytics.
"""

COURSE_SUBJECTS = ["English", "Mathematics", "Computer", "Physics", "Pak Studies"]
STUDENT_DATABASE = {}

FACULTY_ACCOUNTS = {
    "admin": "teacher123",
    "Ali": "ali1234"
}


def authenticate_user():
    """Handles teacher authentication prior to opening the dashboard."""
    print("==========================================")
    print("      ACADEMIC MANAGEMENT SYSTEM          ")
    print("          FACULTY LOGIN PORTAL            ")
    print("==========================================")

    remaining_attempts = 3
    while remaining_attempts > 0:
        usr = input("\nUsername: ").strip()
        pwd = input("Password: ").strip()

        if usr in FACULTY_ACCOUNTS and FACULTY_ACCOUNTS[usr] == pwd:
            print(f"\nAuthentication successful. Welcome, Professor {usr}!")
            return True
        
        remaining_attempts -= 1
        if remaining_attempts > 0:
            print(f"Incorrect credentials. {remaining_attempts} attempt(s) remaining.")
        else:
            print("\nAccess denied: Maximum login attempts exceeded.")
            return False


def determine_letter_grade(percentage_val):
    """Maps a percentage score to its corresponding academic letter grade."""
    if percentage_val >= 90:
        return "A+"
    if percentage_val >= 80:
        return "A"
    if percentage_val >= 70:
        return "B"
    if percentage_val >= 60:
        return "C"
    if percentage_val >= 50:
        return "D"
    return "F"


def compute_academic_metrics(subject_scores):
    """Calculates total marks, overall percentage, letter grade, and passing status."""
    total_obtained = sum(subject_scores.values())
    max_possible = len(COURSE_SUBJECTS) * 100
    percentage = (total_obtained / max_possible) * 100
    grade = determine_letter_grade(percentage)

    # Student fails if overall grade is 'F' or if any subject score is under 40
    has_sub_failure = any(score < 40 for score in subject_scores.values())
    outcome = "Fail" if (grade == "F" or has_sub_failure) else "Pass"

    return total_obtained, round(percentage, 2), grade, outcome


def register_new_student():
    """Handles new student entry with strict input validations."""
    print("\n--- [ ENROLL NEW STUDENT ] ---")

    # 1. Roll Number Validation
    while True:
        roll_id = input("Enter Roll Number (digits only): ").strip()
        if not roll_id:
            print("  [Error] Roll number field cannot be left blank.")
        elif not roll_id.isdigit():
            print("  [Error] Roll number must consist strictly of numeric digits.")
        elif roll_id in STUDENT_DATABASE:
            print(f"  [Error] Record with Roll Number '{roll_id}' already exists.")
        else:
            break

    # 2. Student Name Validation
    while True:
        full_name = input("Enter Full Name: ").strip()
        if not full_name:
            print("  [Error] Name field cannot be left blank.")
        elif not all(char.isalpha() or char.isspace() for char in full_name):
            print("  [Error] Student name must contain alphabetic characters only.")
        else:
            full_name = full_name.title()
            break

    # 3. Marks Input (0 - 100)
    score_card = {}
    print("\nEnter obtained marks per subject (0 - 100):")
    for subj in COURSE_SUBJECTS:
        while True:
            try:
                mark = float(input(f"  • {subj}: "))
                if 0 <= mark <= 100:
                    score_card[subj] = mark
                    break
                print("  [Error] Score must range from 0 to 100.")
            except ValueError:
                print("  [Error] Invalid numerical input. Please re-enter.")

    # 4. Computing Metrics & Storage
    tot, pct, grd, st = compute_academic_metrics(score_card)

    STUDENT_DATABASE[roll_id] = {
        "name": full_name,
        "marks": score_card,
        "total": tot,
        "percentage": pct,
        "grade": grd,
        "status": st
    }

    print(f"\nStudent '{full_name}' (ID: {roll_id}) successfully enrolled!")
    print(f"Summary: Total = {tot}/500 | Percentage = {pct}% | Grade = {grd} | Status = {st}")


def display_roster():
    """Displays a tabular view of all registered students."""
    print("\n======================= REGISTERED STUDENTS ROSTER =======================")
    if not STUDENT_DATABASE:
        print("No student records exist within the repository.")
        return

    print(f"{'Roll No.':<12} {'Student Name':<22} {'Percentage':<14} {'Grade':<8} {'Status'}")
    print("-" * 68)

    for r_id, info in STUDENT_DATABASE.items():
        formatted_pct = f"{info['percentage']}%"
        print(f"{r_id:<12} {info['name']:<22} {formatted_pct:<14} {info['grade']:<8} {info['status']}")
    print("=" * 68)


def print_detailed_mark_sheet(roll_id):
    """Outputs a formatted result card for a specific student."""
    if roll_id not in STUDENT_DATABASE:
        print(f"\n[Error] No record matching Roll Number '{roll_id}' was located.")
        return

    record = STUDENT_DATABASE[roll_id]
    print("\n=================== ACADEMIC TRANSCRIPT ===================")
    print(f"Student Name : {record['name']}")
    print(f"Roll Number  : {roll_id}")
    print("-----------------------------------------------------------")
    print("Subject Breakdown:")
    for course, val in record["marks"].items():
        print(f"  - {course:<15} : {val:>5.1f} / 100")
    print("-----------------------------------------------------------")
    print(f"Total Score  : {record['total']:>5.1f} / 500")
    print(f"Percentage   : {record['percentage']:>5.1f}%")
    print(f"Final Grade  : {record['grade']:>5}")
    print(f"Final Status : {record['status']:>5}")
    print("===========================================================")


def locate_student_entry():
    """Prompts for a roll number and searches for the student."""
    print("\n--- [ SEARCH RECORD ] ---")
    query_id = input("Enter Roll Number to retrieve: ").strip()
    print_detailed_mark_sheet(query_id)


def fetch_report_card():
    """Generates a complete result card view."""
    print("\n--- [ INDIVIDUAL REPORT CARD ] ---")
    query_id = input("Enter Roll Number to generate transcript: ").strip()
    print_detailed_mark_sheet(query_id)


def modify_student_marks():
    """Allows selective updating of subject marks for an existing student."""
    print("\n--- [ UPDATE STUDENT MARKS ] ---")
    target_id = input("Enter Roll Number to update: ").strip()

    if target_id not in STUDENT_DATABASE:
        print(f"[Error] No record matching Roll Number '{target_id}' was located.")
        return

    profile = STUDENT_DATABASE[target_id]
    print(f"\nEditing scores for: {profile['name']} (ID: {target_id})")
    print("Available Courses:")
    for pos, sub_name in enumerate(COURSE_SUBJECTS, start=1):
        print(f"  {pos}. {sub_name} (Current Score: {profile['marks'][sub_name]})")

    selected_input = input("\nEnter Course Name or Number (1-5): ").strip()
    chosen_sub = None

    if selected_input.isdigit() and 1 <= int(selected_input) <= len(COURSE_SUBJECTS):
        chosen_sub = COURSE_SUBJECTS[int(selected_input) - 1]
    else:
        for sub_name in COURSE_SUBJECTS:
            if sub_name.lower() == selected_input.lower():
                chosen_sub = sub_name
                break

    if not chosen_sub:
        print("[Error] Invalid course selection.")
        return

    while True:
        try:
            new_val = float(input(f"Enter revised marks for {chosen_sub} (0 - 100): "))
            if 0 <= new_val <= 100:
                profile["marks"][chosen_sub] = new_val
                break
            print("[Error] Marks must be between 0 and 100.")
        except ValueError:
            print("[Error] Input must be numerical.")

    tot, pct, grd, st = compute_academic_metrics(profile["marks"])
    profile["total"] = tot
    profile["percentage"] = pct
    profile["grade"] = grd
    profile["status"] = st

    print(f"\nSuccessfully updated marks for {chosen_sub}!")
    print(f"Updated Profile: Total = {tot}/500 | Percentage = {pct}% | Grade = {grd} | Status = {st}")


def remove_student_record():
    """Deletes a student record following explicitly verified confirmation."""
    print("\n--- [ REMOVE RECORD ] ---")
    target_id = input("Enter Roll Number for deletion: ").strip()

    if target_id not in STUDENT_DATABASE:
        print(f"[Error] No record matching Roll Number '{target_id}' was located.")
        return

    st_name = STUDENT_DATABASE[target_id]["name"]
    approval = input(f"Are you sure you want to delete {st_name} (ID: {target_id})? (y/n): ").strip().lower()

    if approval == "y":
        del STUDENT_DATABASE[target_id]
        print(f"\nRecord for '{st_name}' (ID: {target_id}) permanently removed.")
        return

    print("\nAction canceled. Record remains intact.")


def print_subject_analytics():
    """Prints maximum, minimum, and average scores per subject."""
    print("\n---------------- COURSE PERFORMANCE ANALYTICS ----------------")
    print(f"{'Course Name':<18} {'High Score':<12} {'Low Score':<12} {'Average':<12}")
    print("-" * 54)

    for course in COURSE_SUBJECTS:
        all_scores = [data["marks"][course] for data in STUDENT_DATABASE.values()]
        top_mark = max(all_scores)
        low_mark = min(all_scores)
        avg_mark = sum(all_scores) / len(all_scores)
        print(f"{course:<18} {top_mark:<12.1f} {low_mark:<12.1f} {avg_mark:<12.2f}")


def print_merit_and_remedial_analysis():
    """Prints top 3 ranked students and lists failed courses per struggling student."""
    print("\n---------------- MERIT & REMEDIAL EVALUATION ----------------")

    # 1. Top 3 Performers
    ranked_list = sorted(STUDENT_DATABASE.items(), key=lambda item: item[1]["percentage"], reverse=True)
    print(" Top 3 Academic Achievers:")
    for place, (r_id, profile) in enumerate(ranked_list[:3], start=1):
        print(f"  Rank {place}: {profile['name']} (ID: {r_id}) - {profile['percentage']}% [Grade: {profile['grade']}]")

    # 2. Failing Subjects Diagnostic
    print("\n Academic Support Recommendations:")
    remedial_needed = False
    for r_id, profile in STUDENT_DATABASE.items():
        failed_courses = [course for course, val in profile["marks"].items() if val < 40]
        if failed_courses:
            remedial_needed = True
            failed_str = ", ".join(failed_courses)
            print(f"  • {profile['name']} (ID: {r_id}) -> Failed subject(s): {failed_str}")

    if not remedial_needed:
        print("  All enrolled students passed every registered subject (>=40).")


def generate_class_statistics():
    """Calculates overall class performance metrics."""
    print("\n===================== CLASSROOM ANALYTICS =====================")
    if not STUDENT_DATABASE:
        print("Insufficient data to compute class statistics.")
        return

    total_count = len(STUDENT_DATABASE)
    percentages = [st["percentage"] for st in STUDENT_DATABASE.values()]
    avg_percentage = sum(percentages) / total_count
    max_percentage = max(percentages)
    min_percentage = min(percentages)

    class_top = max(STUDENT_DATABASE.items(), key=lambda item: item[1]["percentage"])
    passes = sum(1 for st in STUDENT_DATABASE.values() if st["status"] == "Pass")
    fails = total_count - passes

    print(f"Total Enrolled Students : {total_count}")
    print(f"Class Average Percentage : {avg_percentage:.2f}%")
    print(f"Highest Class Percentage : {max_percentage:.2f}%")
    print(f"Lowest Class Percentage  : {min_percentage:.2f}%")
    print(f"Top Performing Student   : {class_top[1]['name']} (ID: {class_top[0]}) @ {class_top[1]['percentage']}%")
    print(f"Passed Count             : {passes}")
    print(f"Failed Count             : {fails}")

    # Render Subject-Wise & Merit/Remedial Breakdown
    print_subject_analytics()
    print_merit_and_remedial_analysis()
    print("===============================================================")


def start_system_dashboard():
    """Main event loop driving the application menu system."""
    while True:
        print("\n========== STUDENT RESULT SYSTEM ==========")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Marks")
        print("5. Student Result")
        print("6. Class Statistics")
        print("7. Delete Student")
        print("8. Exit")
        print("============================================")

        user_choice = input("Enter your choice (1-8): ").strip()

        if user_choice == "1":
            register_new_student()
        elif user_choice == "2":
            display_roster()
        elif user_choice == "3":
            locate_student_entry()
        elif user_choice == "4":
            modify_student_marks()
        elif user_choice == "5":
            fetch_report_card()
        elif user_choice == "6":
            generate_class_statistics()
        elif user_choice == "7":
            remove_student_record()
        elif user_choice == "8":
            print("\nShutting down Student Result System. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please select a valid option between 1 and 8.")


if __name__ == "__main__":
    if authenticate_user():
        start_system_dashboard()