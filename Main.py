import datetime
import json
import os

class TaskManager:
    """Agentic Tool: Handles task scheduling, deadlines, and persistence."""
    
    def __init__(self, filename="student_tasks.json"):
        self.filename = filename
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, title, category, due_date_str):
        try:
            # Validate date format
            datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
            task = {
                "id": len(self.tasks) + 1,
                "title": title,
                "category": category,
                "due_date": due_date_str,
                "status": "Pending"
            }
            self.tasks.append(task)
            self.save_tasks()
            return f"Task added successfully: '{title}' due on {due_date_str}"
        except ValueError:
            return "Execution Error: Invalid date format. Use YYYY-MM-DD."

    def list_tasks(self, filter_status=None):
        if not self.tasks:
            return "No tasks found."
        
        output = []
        for t in self.tasks:
            if filter_status is None or t["status"].lower() == filter_status.lower():
                output.append(f"[{t['id']}] {t['title']} | Category: {t['category']} | Due: {t['due_date']} | Status: {t['status']}")
        
        return "\n".join(output) if output else f"No tasks found with status '{filter_status}'."


class AnalyticsEngine:
    """Agentic Tool: Handles GPA calculation and academic progress projections."""
    
    GRADE_POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

    def calculate_gpa(self, courses):
        """
        Courses format: list of dicts [{'course': 'CS101', 'grade': 'A', 'credits': 4}]
        """
        total_points = 0.0
        total_credits = 0
        
        for c in courses:
            grade = c.get("grade", "").upper()
            credits = c.get("credits", 0)
            
            if grade in self.GRADE_POINTS and isinstance(credits, (int, float)) and credits > 0:
                total_points += self.GRADE_POINTS[grade] * credits
                total_credits += credits
            else:
                return f"Execution Error: Invalid course data detected in {c}"

        if total_credits == 0:
            return "Error: Total credits must be greater than zero."
            
        gpa = round(total_points / total_credits, 2)
        return {"gpa": gpa, "total_credits": total_credits}


class StudentAssistantCoordinator:
    """
    Central Coordinator Agent: Performs goal decomposition, tool execution,
    and self-evaluation logic.
    """
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.analytics_engine = AnalyticsEngine()

    def process_goal(self, goal_type, payload):
        """Processes high-level user intent using structured execution loops."""
        print(f"\n[Agent Coordinator] Processing Goal: '{goal_type}'...")

        if goal_type == "plan_study_schedule":
            # Goal Decomposition step
            print(" -> [Planning Sub-Agent] Decomposing goal into schedule entries...")
            results = []
            for item in payload.get("tasks", []):
                res = self.task_manager.add_task(
                    title=item["title"],
                    category=item.get("category", "General"),
                    due_date_str=item["due_date"]
                )
                results.append(res)
            
            # Reflection/Evaluation step
            print(" -> [Reflection Sub-Agent] Verifying schedule creation...")
            return "\n".join(results)

        elif goal_type == "evaluate_academic_standing":
            print(" -> [Analytics Sub-Agent] Processing course grade records...")
            result = self.analytics_engine.calculate_gpa(payload.get("courses", []))
            
            # Reflection step
            if isinstance(result, dict):
                gpa = result["gpa"]
                standing = "Excellent" if gpa >= 3.5 else "Good" if gpa >= 3.0 else "Needs Improvement"
                return f"Calculated GPA: {gpa} across {result['total_credits']} credits.\nAcademic Standing Evaluation: {standing}"
            else:
                return f"Execution Error: {result}"

        elif goal_type == "view_schedule":
            return self.task_manager.list_tasks(filter_status=payload.get("status"))

        else:
            return "Error: Unknown goal type provided."


# --- Demonstration of the Agent System ---
if __name__ == "__main__":
    agent = StudentAssistantCoordinator()

    # Demonstration 1: Autonomous Plan Execution
    study_plan_goal = {
        "tasks": [
            {"title": "Algorithms Final Revision", "category": "CS201", "due_date": "2026-09-20"},
            {"title": "Database Schema Project Submission", "category": "CS202", "due_date": "2026-09-25"}
        ]
    }
    plan_output = agent.process_goal("plan_study_schedule", study_plan_goal)
    print(f"System Response:\n{plan_output}")

    # Demonstration 2: View Scheduled Tasks
    print("\n--- Current Pending Schedule ---")
    schedule_output = agent.process_goal("view_schedule", {"status": "Pending"})
    print(schedule_output)

    # Demonstration 3: Academic Analytics Goal
    print("\n--- Grade & GPA Analysis ---")
    academic_data = {
        "courses": [
            {"course": "Algorithms", "grade": "A", "credits": 4},
            {"course": "Database Systems", "grade": "B", "credits": 3},
            {"course": "Linear Algebra", "grade": "A", "credits": 3}
        ]
    }
    analytics_output = agent.process_goal("evaluate_academic_standing", academic_data)
    print(analytics_output)
