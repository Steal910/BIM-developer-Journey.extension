Material-Dependent Parameter for Autodesk Revit
🎯 Automate parameter assignment based on material properties 🎯

This Python script for Autodesk Revit allows you to dynamically create shared parameters and assign values to elements based on the materials they are associated with. It's a step towards leveraging automation in BIM workflows to improve efficiency and reduce errors.

🛠️ Features
Create shared parameters automatically if they don't exist in the project.
Assign parameter values based on material names matching user-defined criteria.
Flexible configuration through an intuitive WPF-based graphical interface.
📋 How It Works
The user provides:

Parameter Name – the name of the shared parameter to be created.
Criteria – partial names of materials to filter elements.
Values – the corresponding values to assign based on the criteria.
The script:

Checks if the parameter already exists and binds it to all applicable categories.
Iterates through elements in the project, evaluating their materials.
Assigns the appropriate value to the parameter based on the material name.
💻 How to Use
Open the script in Revit using pyRevit or any compatible Python environment.
Run the script to open the graphical interface.
Enter the parameter name, criteria, and values.
Click "Create and Assign Parameters" to execute the operation.
The parameter will be created, bound, and assigned to elements in the project based on material properties.
Feel free to test, adapt, and share your feedback to improve this tool further. Let's make BIM workflows smarter and more efficient! 🚀

#BIM #Python #Revit #Automation #MaterialProperties #BIMDeveloper
