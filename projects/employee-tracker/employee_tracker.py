#!/usr/bin/env python3
"""Simple CSV employee tracker using fictional demo records only."""
import argparse
import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("employees.csv")
FIELDS = ["employee_id", "name", "department"]

def read_rows():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(rows):
    with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def list_employees():
    rows = read_rows()
    if not rows:
        print("No records found.")
        return
    print(f"{'ID':<12} {'NAME':<24} DEPARTMENT")
    print("-" * 55)
    for row in rows:
        print(f"{row['employee_id']:<12} {row['name']:<24} {row['department']}")

def search_employee(term):
    term = term.casefold()
    matches = [r for r in read_rows() if term in r["employee_id"].casefold() or term in r["name"].casefold()]
    if not matches:
        print("No matching demo employee found.")
        return
    for row in matches:
        print(f"{row['employee_id']} | {row['name']} | {row['department']}")

def add_employee(employee_id, name, department):
    rows = read_rows()
    employee_id = employee_id.strip()
    if any(r["employee_id"].casefold() == employee_id.casefold() for r in rows):
        raise SystemExit("That employee ID already exists.")
    rows.append({"employee_id": employee_id, "name": name.strip(), "department": department.strip()})
    write_rows(rows)
    print(f"Added demo record: {employee_id}")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list demo employee records")
    search = sub.add_parser("search", help="search by ID or name")
    search.add_argument("term")
    add = sub.add_parser("add", help="add a fictional demo record")
    add.add_argument("employee_id")
    add.add_argument("name")
    add.add_argument("department")
    args = parser.parse_args()
    if args.command == "list":
        list_employees()
    elif args.command == "search":
        search_employee(args.term)
    elif args.command == "add":
        add_employee(args.employee_id, args.name, args.department)

if __name__ == "__main__":
    main()
