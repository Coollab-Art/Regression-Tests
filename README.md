# Coollab Regression Tester

A regression testing application designed to visually compare image exports from different versions of the **Coollab** application.

---

## 🧪 How It Works

This tool automatically compares **reference images** with **newly exported images** from your `.coollab` projects to detect any potential visual differences.

---

## 📁 Initial Setup

1. **Add your Coollab projects**
   
   Place `.coollab` files to test in:

   ```
   assets/projects/
   ```

2. **Launch the application**
    
    Simply run:

   ```bash
   main.py
   ```

3. **Specify the path to your Coollab executable**

   The first time you run the app, it will ask for your **Coollab** executable path. This will be saved for future sessions.

   > 📅 If no reference images have been exported yet, the specified Coollab version will be used to generate them automatically.

---

## ▶️ Running Tests

Once the application and Coollab are both running (in the background for Coollab) :

* `.coollab` files are detected automatically.
* You can:

  * **Test all projects at once** ✅
  * **Test a specific project** via the replay button 🔄️
  * **Change the Coollab version** by updating the path at the top of the interface and launching all tests

---

## 🛠️ Managing Reference Images

To **re-export reference images**:

* Use the dedicated button at the bottom of the interface
* Or **right-click** on the desired project

---

## 🔎 Test Results

Once a project is tested:

* A **score** will appear, indicating image similarity (reference vs export)
* Score colors help quickly identify differences:

  * 🟢 Low score → very similar images
  * 🔴 High score → significant differences detected

---

## 🖼️ Visualizing Differences

Click on a tested project to:

* View:

  * The **reference** image
  * The **exported** image
  * The **difference image** (computed diff)
* Navigate between views using keys:

  * `E` → Exported
  * `R` → Reference (Original)
  * `T` → Threshold (Difference)
* Use `Spacebar` to quickly toggle between reference and exported images
* Use the **color picker** to inspect image colors

---

## 🧼 Auto Cleanup

* When closing the application:

  * Coollab shuts down automatically
  * All **test-exported images** are deleted
  * **Reference images** are kept

---

## 👨‍💻 Authors

Created by **[Elvin Kauffmann](https://github.com/ShadowsHood)** with support from **[Jules Fouchy](https://github.com/JulesFouchy)**

Coollab © — All rights reserved.
