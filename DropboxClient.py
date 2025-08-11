import dropbox

class DropboxClient:
    def __init__(self, token, folder_name):
        self.dbx = dropbox.Dropbox(token)
        self.user = self.dbx.users_get_current_account()
        if not folder_name.startswith('/'):
            self.folder_name = f"/{folder_name}"
        else:
            self.folder_name = folder_name
        self.template_id = None

    def find_file_path(self, file_name):
        try:
            result = self.dbx.files_search(self.folder_name, file_name)
            if result.matches:
                return result.matches[0].metadata.path_lower
            else:
                print(f"File '{file_name}' not found in folder '{self.folder_name}'.")
                return None
        except Exception as e:
            print(f"Error searching for file: {e}")
            return None
    
    def create_template(self):
        template_name = "Debate Metadata"
        fields = [
            dropbox.file_properties.PropertyFieldTemplate("assignment_name", dropbox.file_properties.PropertyType.string),
            dropbox.file_properties.PropertyFieldTemplate("description", dropbox.file_properties.PropertyType.string),
            dropbox.file_properties.PropertyFieldTemplate("due_date", dropbox.file_properties.PropertyType.string),
            dropbox.file_properties.PropertyFieldTemplate("status", dropbox.file_properties.PropertyType.string),
            dropbox.file_properties.PropertyFieldTemplate("assignee", dropbox.file_properties.PropertyType.string)
        ]
        try:
            template = self.dbx.file_properties_templates_add_for_user(template_name, "Tagging debate assignments", fields)
            self.template_id = template.template_id
        except dropbox.exceptions.ApiError as e:
            if e.error.is_template_already_exists():
                print(f"Template '{template_name}' already exists.")
                template = self.dbx.file_properties_templates_get_for_user(template_name)
                self.template_id = template.template_id
            else:
                print(f"Error creating property template: {e}")


    def add_metadata(self, file_name, metadata):
        self.create_template()

        properties = [
            dropbox.file_properties.PropertyField("assignment_name", metadata.get("Assignment", "")),
            dropbox.file_properties.PropertyField("description", metadata.get("Description", "")),
            dropbox.file_properties.PropertyField("due_date", metadata.get("Due Date", "")),
            dropbox.file_properties.PropertyField("status", metadata.get("Progress", "")),
            dropbox.file_properties.PropertyField("assignee", metadata.get("Assignee", ""))
        ]

        property_group = dropbox.file_properties.PropertyGroup(self.template_id, properties)

        file_path = self.find_file_path(file_name)

        if not file_path:
            print(f"File '{file_name}' not found.")
            return
        try:
            self.dbx.file_properties_properties_add(file_path, property_group)
            print(f"Metadata added to file: {file_path}")
        except Exception as e:
            print(f"Error adding metadata: {e}")
    
    def update_metadata(self, file_name, new_key, new_value):
        updates = [
            dropbox.file_properties.PropertyGroupUpdate(
                template_id=self.template_id,
                add_or_update_fields=[
                    dropbox.file_properties.PropertyField(name=new_key, value=new_value)
                ],
                remove_fields=[]
            )
        ]

        file_path = self.find_file_path(file_name)
        if not file_path:
            print(f"File '{file_name}' not found.")
            return
        try:
            self.dbx.file_properties_properties_update(file_path, update_rules=updates)
            print(f"Metadata updated for file: {file_path}")
        except Exception as e:
            print(f"Error updating metadata: {e}")