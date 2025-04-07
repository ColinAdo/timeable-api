# 🚀 How to Use the System

This section walks you through how to use the Automatic Timetable Generation System (ATGS) via the web interface.

---

## 🌐 Accessing the Frontend

Visit the frontend by navigating to:

```http://localhost:3000```


If you're using **Ngrok** for testing or sharing, use the generated HTTPS URL instead.

---

## 📁 Step 1: Upload Excel File

- Prepare an Excel file (`.xlsx`) containing unit information.
- The file should include:
  - Unit Code
  - Unit Name
  - Academic Year
  - Year & Semester (e.g., `Y1S1`, `Y2S2`, etc.)

### Example Excel Format:

| Unit Code | Unit Name             | Year & Semester |
|-----------|-----------------------|-----------------|
| BIT101    | Introduction to IT    | Y1S1            |
| BIT102    | Fundamentals of Logic | Y1S1            |

- Click the **"Upload File"** button.
- Choose your Excel file and confirm upload.

✅ **Tip**: Make sure the columns are correctly labeled and formatted to avoid backend validation errors.

---

## ⚙️ Step 2: Configure Constraints

- Enter the **time range to avoid** (e.g., 08:00 to 10:00).
- Set the **maximum units allowed per day** (default is `2` for each year-semester group).
- These constraints are used to ensure a student-friendly timetable.

---

## 🧬 Step 3: Generate Timetable

- After uploading the Excel file and setting constraints:
  - Click the **"Generate"** button.
  - The backend will process your data using a Genetic Algorithm and apply your constraints.
  - You should see a loading indicator during processing.

✅ **Tip**: If it takes a few seconds, be patient — this means your data is being optimized!

---

## 📥 Step 4: Download the Final Timetable

- Once generation is complete, a download link will appear.
- Click **"Download Timetable"** to save your `.xlsx` file.

✅ The downloaded Excel file will contain a clean timetable separated by Year & Semester.

---

## 🧪 Testing the Flow

To verify that everything works as expected:

- Visit the frontend at `http://localhost:3000`
- Upload a sample Excel file
- Apply your desired constraints
- Click **Generate**
- Confirm if the backend returns results or prompts download

---

## 🐞 Troubleshooting

| Issue                             | Possible Fix                                      |
|----------------------------------|---------------------------------------------------|
| File upload fails                | Ensure it's a `.xlsx` file with valid structure   |
| No download link after generate  | Check browser console or backend logs for errors |
| Backend doesn't respond          | Ensure API server is running on port `8000`      |
| Ngrok link not working           | Make sure your Ngrok tunnel is active and secure |

---

## 📌 Notes

- Redis must be running if you're using background processing.
- Ngrok should be re-run if your tunnel expires.
- You can reset and test with multiple Excel files.

---

