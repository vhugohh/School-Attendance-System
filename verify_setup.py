import utils
import os

print("Testing database initialization...")
utils.init_db()
print("DB Initialized.")

print("Testing student registration...")
utils.register_student("TEST001", "Test Student", "1A")
print("Student registered.")

print("Testing attendance recording...")
success, msg = utils.record_attendance("TEST001")
print(f"Record result: {success}, Message: {msg}")

if not success:
    print("FAILED: Attendance should have been recorded.")

print("Testing duplicate attendance...")
success, msg = utils.record_attendance("TEST001")
print(f"Record result: {success}, Message: {msg}")
if success:
    print("FAILED: Duplicate attendance should be prevented.")

print("Testing data retrieval...")
df = utils.get_attendance_data()
print("Data retrieved:")
print(df)

if len(df) > 0 and df.iloc[0]['id'] == 'TEST001':
    print("VERIFICATION SUCCESSFUL")
else:
    print("VERIFICATION FAILED: Data mismatch")
