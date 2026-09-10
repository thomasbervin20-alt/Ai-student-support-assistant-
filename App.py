# ai_student_assistant.py - Complete AI Student Support Assistant

import json
import os
from datetime import datetime

class TaskPlannerAgent:
    """Sub-agent responsible for study tasks, scheduling, and persistence."""
    def __init__(self, storage_file="student_tasks.json"):
        self.storage_file = storage_file
        self.tasks = self._load_data()

    def _load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title, course, due_date):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "course": course,
            "due_date": due_date,
            "status": "Pending"
        }
        self.tasks.append(task)
        self.save_data()
        return f"Task '{title}' added successfully for {course}."

    def list_tasks(self):
        if not self.tasks:
            return "No upcoming tasks recorded."
        formatted = ["\n--- Pending Study Tasks ---"]
        for t in self.tasks:
            formatted.append(f"[{t['id']}] {t['course']}: {t['title']} | Due: {t['due_date']} | Status: {t['status']}")
        return "\n".join(formatted)


class AnalyticsAgent:
    """Sub-agent responsible for grade calculations and academic standings."""
    GRADE_MAP = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

    def compute_gpa(self, grade_records):
        total_points = 0.0
        total_credits = 0

        for record in grade_records:
            grade = record.get("grade", "").upper()
            credits = record.get("credits", 0)
            if grade in self.GRADE_MAP and credits > 0:
                total_points += self.GRADE_MAP[grade] * credits
                total_credits += credits

        if total_credits == 0:
            return "No valid course credits available for calculation."

        gpa = round(total_points / total_credits, 2)
        standing = "Honor Roll" if gpa >= 3.5 else "Good Standing" if gpa >= 2.5 else "Academic Warning"
        return f"Current GPA: {gpa} ({total_credits} total credits) | Standing: {standing}"


class StudentSupportCoordinator:
    """Central Assistant routing user intents and executing actions."""
    def __init__(self):
        self.planner = TaskPlannerAgent()
        self.analytics = AnalyticsAgent()

    def run_interactive(self):
        print("==========================================")
        print("  Welcome to AI Student Support Assistant ")
        print("==========================================")
        
        while True:
            print("\nOptions:")
            print("1. Add Study Task")
            print("2. View All Tasks")
            print("3. Calculate GPA")
            print("4. Exit")
            
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                title = input("Enter assignment/task title: ").strip()
                course = input("Enter course code (e.g., CS101): ").strip()
                due_date = input("Enter due date (YYYY-MM-DD): ").strip()
                result = self.planner.add_task(title, course, due_date)
                print(f"\n[AI Assistant]: {result}")
                
            elif choice == "2":
                print(self.planner.list_tasks())
                
            elif choice == "3":
                records = []
                print("\nEnter course grades (type 'done' when finished):")
                while True:
                    c_name = input("Course Name (or 'done'): ").strip()
                    if c_name.lower() == 'done':
                        break
                    grade = input("Grade (A/B/C/D/F): ").strip()
                    try:
                        credits = int(input("Credits (e.g., 3 or 4): ").strip())
                        records.append({"course": c_name, "grade": grade, "credits": credits})
                    except ValueError:
                        print("Invalid credit value. Skipping course entry.")
                
                result = self.analytics.compute_gpa(records)
                print(f"\n[AI Assistant]: {result}")
                
            elif choice == "4":
                print("\nGoodbye! Good luck with your studies.")
                break
            else:
                print("\nInvalid choice. Please pick between 1 and 4.")

if __name__ == "__main__":
    assistant = StudentSupportCoordinator()
    assistant.run_interactive()
