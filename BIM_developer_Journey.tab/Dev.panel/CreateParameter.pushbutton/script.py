# -*- coding: utf-8 -*-
__title__ = "Create Parameter"
__doc__ = """This script creates  parameter in the Revit project ."""

from Autodesk.Revit.DB import (
    ExternalDefinitionCreationOptions,
    InstanceBinding,
    BuiltInParameterGroup,
    Transaction,
    CategorySet,
    SpecTypeId
)
from rpw.ui.forms import FlexForm, Label, TextBox, Separator, Button
from Autodesk.Revit.UI import TaskDialog

def add_new_shared_parameter(doc, param_name, group_name="Custom Group"):
    """Creates a new shared parameter and binds it to applicable categories."""
    app = doc.Application
    shared_param_file = app.OpenSharedParameterFile()

    if not shared_param_file:
        raise ValueError("Shared parameter file is not set. Please configure it in Revit.")

    # Check if the group exists in the shared parameter file
    group = shared_param_file.Groups.get_Item(group_name)
    if not group:
        # Create the group if it doesn't exist
        group = shared_param_file.Groups.Create(group_name)

    # Check if the parameter already exists in the group
    external_def = group.Definitions.get_Item(param_name)
    if not external_def:
        # Create a new parameter definition
        options = ExternalDefinitionCreationOptions(param_name, SpecTypeId.String.Text)
        external_def = group.Definitions.Create(options)

    # Check if the parameter is already bound to the document
    binding_map = doc.ParameterBindings
    existing_key, existing_binding = None, None
    it = binding_map.ForwardIterator()
    it.Reset()
    while it.MoveNext():
        if it.Key.Name == param_name:
            existing_key, existing_binding = it.Key, it.Current
            break

    if existing_key and existing_binding:
        TaskDialog.Show("Info", "Parameter '{}' already exists in the document.".format(param_name))
        return param_name  # Parameter already exists in the document

    # Bind the parameter to applicable categories
    with Transaction(doc, "Bind Parameter {} to Categories".format(param_name)) as tx:
        tx.Start()
        try:
            category_set = CategorySet()
            for cat in doc.Settings.Categories:
                if cat.AllowsBoundParameters:
                    category_set.Insert(cat)

            if not category_set:
                raise ValueError("No categories allow bound parameters.")

            # Bind the parameter as an instance parameter
            instance_binding = doc.Application.Create.NewInstanceBinding(category_set)
            binding_map.Insert(external_def, instance_binding, BuiltInParameterGroup.PG_DATA)
        except Exception as e:
            tx.RollBack()
            raise e
        tx.Commit()

    TaskDialog.Show("Success", "Parameter '{}' has been created and bound successfully.".format(param_name))
    return param_name

def main():
    doc = __revit__.ActiveUIDocument.Document

    # Define WPF form components
    components = [
        Label('Enter parameter name:'),
        TextBox('param_name'),
        Separator(),
        Button('Submit')
    ]

    # Display the form
    form = FlexForm('Create New Shared Parameter', components)
    form.show()

    # Retrieve user input
    user_inputs = form.values
    if user_inputs and 'param_name' in user_inputs:
        param_name = user_inputs['param_name']
        if param_name.strip():  # Ensure the parameter name is not empty
            add_new_shared_parameter(doc, param_name)
        else:
            TaskDialog.Show("Error", "Parameter name cannot be empty.")
    else:
        TaskDialog.Show("Cancelled", "No parameter name was entered.")

main()

