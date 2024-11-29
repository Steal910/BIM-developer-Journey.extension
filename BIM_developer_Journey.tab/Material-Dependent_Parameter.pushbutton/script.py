# -*- coding: utf-8 -*-
__title__ = "Material-Dependent Parameter"
__doc__ = """Create and assign parameter values based on user input from WPF."""

# Importy z Autodesk Revit API
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    ExternalDefinitionCreationOptions,
    InstanceBinding,
    BuiltInParameterGroup,
    Transaction,
    CategorySet,
    SpecTypeId,
    StorageType
)
import Autodesk.Revit.DB as DB  # Alias dla Autodesk.Revit.DB

# Importy dla WPF
import wpf
from pyrevit import forms
import clr
import os

# Załadowanie referencji do systemowych bibliotek
clr.AddReference('System')
from System.Windows import Window
from Autodesk.Revit.UI import TaskDialog  # Import TaskDialog do wyświetlania komunikatu


class RecyclingWindow(Window):
    def __init__(self):
        current_directory = os.path.dirname(__file__)  # Pobranie ścieżki do katalogu skryptu
        xaml_path = os.path.join(current_directory, 'FourthButton.xaml')  # Połączenie katalogu i pliku
        wpf.LoadComponent(self, xaml_path)  # Załadowanie pliku XAML

    def OnSubmitClick(self, sender, event):
        """Obsługa kliknięcia przycisku 'Utwórz i przypisz parametry'."""
        param_name = self.ParamNameTextBox.Text
        value1 = self.Value1TextBox.Text
        value2 = self.Value2TextBox.Text
        value3 = self.Value3TextBox.Text
        criteria1 = self.Criteria1TextBox.Text
        criteria2 = self.Criteria2TextBox.Text

        # Uruchom funkcję tworzenia i przypisania parametru
        self.create_and_assign_parameter(param_name, criteria1, criteria2, value1, value2, value3)

        # Zamknięcie okna WPF
        self.Close()

        # Wyświetlenie komunikatu o sukcesie
        TaskDialog.Show("Sukces", "Parametr oraz jego wartości zostały utworzone.")

    def CloseButton_Click(self, sender, event):
        """Obsługa kliknięcia przycisku zamknięcia."""
        self.Close()

    def create_and_assign_parameter(self, param_name, criteria1, criteria2, value1, value2, value3):
        """Tworzy parametr i przypisuje wartości elementom w Revit."""
        doc = __revit__.ActiveUIDocument.Document

        # Upewnij się, że parametr istnieje lub został utworzony
        self.create_recycling_parameter(doc, param_name)
        self.assign_recycling_values(doc, param_name, criteria1, criteria2, value1, value2, value3)

    def create_recycling_parameter(self, doc, param_name):
        """Tworzy parametr współdzielony, jeśli jeszcze nie istnieje."""
        app = doc.Application
        shared_param_file = app.OpenSharedParameterFile()

        if not shared_param_file:
            TaskDialog.Show("Błąd", "Nie znaleziono pliku parametrów współdzielonych. Ustaw go w Revit.")
            return

        # Sprawdź, czy istnieje grupa "Custom Group" lub utwórz ją
        group_name = "Custom Group"
        group = shared_param_file.Groups.get_Item(group_name)
        if not group:
            group = shared_param_file.Groups.Create(group_name)

        # Sprawdź, czy definicja parametru już istnieje
        external_def = group.Definitions.get_Item(param_name)
        if not external_def:
            # Tworzenie nowej definicji parametru
            options = ExternalDefinitionCreationOptions(param_name, SpecTypeId.String.Text)
            external_def = group.Definitions.Create(options)

        # Sprawdź, czy parametr jest już przypisany do dokumentu
        binding_map = doc.ParameterBindings
        it = binding_map.ForwardIterator()
        it.Reset()

        while it.MoveNext():
            if it.Key.Name == param_name:
                return  # Parametr już istnieje

        # Tworzenie nowego parametru i przypisanie go do kategorii
        with Transaction(doc, "Bind Recycling Parameter") as tx:
            tx.Start()
            category_set = CategorySet()
            for cat in doc.Settings.Categories:
                if cat.AllowsBoundParameters:
                    category_set.Insert(cat)

            if not category_set:
                TaskDialog.Show("Błąd", "Brak kategorii pozwalających na przypisanie parametrów.")
                return

            instance_binding = doc.Application.Create.NewInstanceBinding(category_set)
            binding_map.Insert(external_def, instance_binding, BuiltInParameterGroup.PG_DATA)
            tx.Commit()

    def assign_recycling_values(self, doc, param_name, criteria1, criteria2, value1, value2, value3):
        """Przypisuje wartości parametru do elementów w zależności od ich materiału."""
        elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

        with Transaction(doc, "Assign Recycling Values") as tx:
            tx.Start()

            for element in elements:
                param = element.LookupParameter(param_name)
                if not param or param.IsReadOnly:
                    continue

                material_ids = element.GetMaterialIds(False)
                assigned_value = value3  # Domyślna wartość

                for material_id in material_ids:
                    material = doc.GetElement(material_id)
                    if material:
                        if criteria1.lower() in material.Name.lower():
                            assigned_value = value1
                            break
                        elif criteria2.lower() in material.Name.lower():
                            assigned_value = value2
                            break

                try:
                    if param.StorageType == StorageType.String:
                        param.Set(assigned_value)
                except Exception as e:
                    print("Error: {0}".format(e))

            tx.Commit()


# Uruchomienie okna WPF
window = RecyclingWindow()
window.ShowDialog()
