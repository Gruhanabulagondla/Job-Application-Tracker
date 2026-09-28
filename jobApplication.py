import sqlite3
from datetime import date

DATABASE = "jobs.db"

def connect():
    return sqlite3.connect(DATABASE)

def setup_database():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT DEFAULT 'Applied',
                applied_on TEXT,
                interview_date TEXT,
                notes TEXT
            )
        """)

def add_application():
    print("\n--- Add Job Application ---")

    company = input("Company name: ")
    role = input("Job role: ")

    print("\n1. Applied")
    print("2. Interview")
    print("3. Selected")
    print("4. Rejected")

    choice = input("Choose status: ")

    status_map = {
        "1": "Applied",
        "2": "Interview",
        "3": "Selected",
        "4": "Rejected"
    }

    status = status_map.get(choice, "Applied")

    interview_date = input("Interview date: ")
    notes = input("Notes: ")

    with connect() as con:
        con.execute("""
            INSERT INTO applications
            (company, role, status, applied_on, interview_date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company,
            role,
            status,
            str(date.today()),
            interview_date,
            notes
        ))

    print("\nApplication added successfully!")

def view_applications():
    print("\n--- Job Applications ---")

    with connect() as con:
        applications = con.execute("""
            SELECT id, company, role, status,
                   applied_on, interview_date, notes
            FROM applications
            ORDER BY id DESC
        """).fetchall()

    if not applications:
        print("No applications found.")
        return

    for app in applications:
        print("\n----------------------------")
        print("ID:", app[0])
        print("Company:", app[1])
        print("Role:", app[2])
        print("Status:", app[3])
        print("Applied on:", app[4])
        print("Interview date:", app[5])
        print("Notes:", app[6])

def update_status():
    print("\n--- Update Status ---")

    app_id = input("Enter application ID: ")

    print("1. Applied")
    print("2. Interview")
    print("3. Selected")
    print("4. Rejected")

    choice = input("Choose new status: ")

    status_map = {
        "1": "Applied",
        "2": "Interview",
        "3": "Selected",
        "4": "Rejected"
    }

    status = status_map.get(choice)

    if status is None:
        print("Invalid status.")
        return

    with connect() as con:
        cursor = con.execute("""
            UPDATE applications
            SET status = ?
            WHERE id = ?
        """, (status, app_id))

    if cursor.rowcount > 0:
        print("Status updated successfully!")
    else:
        print("Application not found.")

def delete_application():
    print("\n--- Delete Application ---")

    app_id = input("Enter application ID: ")

    with connect() as con:
        cursor = con.execute("""
            DELETE FROM applications
            WHERE id = ?
        """, (app_id,))

    if cursor.rowcount > 0:
        print("Application deleted successfully!")
    else:
        print("Application not found.")

def search_application():
    print("\n--- Search Application ---")

    keyword = input("Enter company or role: ")

    with connect() as con:
        applications = con.execute("""
            SELECT id, company, role, status
            FROM applications
            WHERE company LIKE ?
            OR role LIKE ?
        """, (
            "%" + keyword + "%",
            "%" + keyword + "%"
        )).fetchall()

    if not applications:
        print("No applications found.")
        return

    for app in applications:
        print(
            f"ID: {app[0]} | "
            f"Company: {app[1]} | "
            f"Role: {app[2]} | "
            f"Status: {app[3]}"
        )

def show_statistics():
    print("\n--- Application Statistics ---")

    with connect() as con:
        total = con.execute(
            "SELECT COUNT(*) FROM applications"
        ).fetchone()[0]

        applied = con.execute(
            "SELECT COUNT(*) FROM applications WHERE status='Applied'"
        ).fetchone()[0]

        interviews = con.execute(
            "SELECT COUNT(*) FROM applications WHERE status='Interview'"
        ).fetchone()[0]

        selected = con.execute(
            "SELECT COUNT(*) FROM applications WHERE status='Selected'"
        ).fetchone()[0]

        rejected = con.execute(
            "SELECT COUNT(*) FROM applications WHERE status='Rejected'"
        ).fetchone()[0]

    print("Total applications:", total)
    print("Applied:", applied)
    print("Interviews:", interviews)
    print("Selected:", selected)
    print("Rejected:", rejected)

def main():
    setup_database()

    while True:
        print("\n==============================")
        print("     JOB APPLICATION TRACKER")
        print("==============================")

        print("1. Add Application")
        print("2. View Applications")
        print("3. Update Status")
        print("4. Delete Application")
        print("5. Search Application")
        print("6. View Statistics")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_application()

        elif choice == "2":
            view_applications()

        elif choice == "3":
            update_status()

        elif choice == "4":
            delete_application()

        elif choice == "5":
            search_application()

        elif choice == "6":
            show_statistics()

        elif choice == "7":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()