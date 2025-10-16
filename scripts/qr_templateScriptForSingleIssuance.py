import json
from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
import time
import yaml
import sys
import copy
from formio.default_components import default_components, submit, recipient_first_name_field, recipient_last_name_field, recipient_email_component, recipient_phone_component, full_name, phone, email

def read_svg(svg_path):
    with open(svg_path, 'r') as f:
        svg_content = f.read()
    return svg_content

def read_yaml_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config
def POST(url, headers, json_data):
    retry_count = 0
    max_retries = 5 

    while retry_count < max_retries:
        response = requests.post(url, headers=headers, json=json_data)
        if response.status_code == 201:
            print("Request successful")
            form_id = response.json().get('_id')
            return form_id
        elif response.status_code == 400:
            error_msg = response.json().get('message', '')
            if "must be unique" in error_msg:
                timestamp = datetime.now().strftime("%d/%m/%Y-%H/%M/%S")
                json_data['title'] += f'-{timestamp}'
                json_data['name'] += f'-{timestamp}'
                json_data['path'] += f'-{timestamp}'
                retry_count += 1
            else:
                print("Form validation failed:", error_msg)
                return
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return

    print(f"Exceeded maximum retry limit of {max_retries}")

def get_components(texts, images, default_components, user_inputs, new_attributes):
    components = []
    componentsSub = []

    seen_keys = set()
    seen_base_fields = set()

    # Add components based on user inputs
    if 'email_choice' in user_inputs:
        email_choice = user_inputs['email_choice']
        if email_choice == '1':
            componentsSub.append(recipient_email_component)
        elif email_choice == '2':
            componentsSub.append(email)
        elif email_choice == '3':
            custom_name = user_inputs.get('email_custom_name')
            default_value = user_inputs.get('email_default_value')
            componentsSub.append({
                'key': custom_name,
                'label': custom_name,
                'type': 'textfield',
                'validate': {
                    'required': True,
                    'maxLength': 55
                },
                'defaultValue': default_value
            })

    if 'phone_choice' in user_inputs:
        phone_choice = user_inputs['phone_choice']
        if phone_choice == '1':
            componentsSub.append(recipient_phone_component)
        elif phone_choice == '2':
            componentsSub.append(phone)
        elif phone_choice == '3':
            custom_name = user_inputs.get('phone_custom_name')
            default_value = user_inputs.get('phone_default_value')
            componentsSub.append({
                'key': custom_name,
                'label': custom_name,
                'type': 'textfield',
                'validate': {
                    'required': True,
                    'maxLength': 10
                },
                'defaultValue': default_value
            })

    if 'name_choice' in user_inputs:
        name_choice = user_inputs['name_choice']
        if name_choice == '1':
            componentsSub.append(recipient_first_name_field)
            componentsSub.append(recipient_last_name_field)
        elif name_choice == '2':
            componentsSub.append(full_name)
        elif name_choice == '3':
            custom_name = user_inputs.get('name_custom_name')
            default_value = user_inputs.get('name_default_value')
            componentsSub.append({
                'key': custom_name,
                'label': custom_name,
                'type': 'textfield',
                'validate': {
                    'required': True,
                    'maxLength': 40
                },
                'defaultValue': default_value
            })

    # Add new attributes to components
    for attr in new_attributes:
        componentsSub.append({
            'key': attr["key"],
            'label': attr["key"],
            'type': 'textfield',
            'validate': {
                'required': attr["is_required"],
                'maxLength': attr["max_characters"]
            },
            'defaultValue': attr["default"]
        })

    # Process existing fields from SVG
    for field in texts:
        data_key = field.get('data-key')
        if not data_key:
            continue

        if '_row' in data_key:
            continue
        
        if data_key in seen_base_fields:
            continue

        seen_base_fields.add(data_key)

        field_type = field.get('data-type').lower()
        label = field.get('data-label') 
        key = field.get('data-key') 
        default_value = field.get('data-default-value')  
        default_form_type = field.get('data-form-type')

        if field_type in default_components:  
            component = default_components[field_type].copy()
            component['label'] = label
            component['key'] = data_key
            if field_type == 'date' and default_value:
                component['defaultDate'] = default_value
            elif default_value:
                component['defaultValue'] = default_value

            if data_key == 'recipientName':
                first_name_component = copy.deepcopy(component)
                first_name_component['key'] = 'recipientFirstName'
                first_name_component['label'] = 'Recipient First Name'
                first_name_component['validate']['pattern']= "^[a-zA-Z .-]+$"
                if default_value:
                    component['defaultValue'] = default_value.split(" ")
                    first_name_component['defaultValue'] = default_value.split(" ")[0]
                last_name_component = copy.deepcopy(component)
                last_name_component['key'] = 'recipientLastName'
                last_name_component['label'] = 'Recipient Last Name'
                last_name_component['validate']['pattern']= "^[a-zA-Z .-]+$"
                if default_value:
                    component['defaultValue'] = default_value.split(" ")
                    last_name_component['defaultValue'] = default_value.split(" ")[1]

                if default_form_type == "template":   
                    components.append(first_name_component)
                    components.append(last_name_component)
                elif default_form_type == "subject": 
                    componentsSub.append(first_name_component)
                    componentsSub.append(last_name_component)

            else:
                if default_form_type == "template":   
                    components.append(component)
                elif default_form_type == "subject": 
                    componentsSub.append(component)

    for field in images:
        field_type = field.get('data-type').lower()
        label = field.get('data-label')
        dataName = field.get('data-name') 
        key = field.get('data-key')  
        default_form_type = field.get('data-form-type')
        description = field.get('data-description')

        if key in seen_keys:  
            continue

        seen_keys.add(key)

        if field_type in default_components:
            component = default_components[field_type].copy()
            component['dataName'] = dataName
            component['key'] = key
            component['label'] = label
            if description:
                component['descriptionValue'] = description

            if default_form_type == "template":
                components.append(component)
            elif default_form_type == "subject":
                componentsSub.append(component)        

    return components, componentsSub

def create_json_data_template(components, form_name_temp):
    json_dataTemplate = {
        'title': form_name_temp,
        'display': 'form',
        'type': 'form',
        'name': form_name_temp,
        'path': form_name_temp,
        'components': components,
        'submissionAccess': [
                    {
                        "type": "create_all",
                        "roles": []
                    },
                    {
                        "type": "read_all",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "update_all",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "delete_all",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "create_own",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "read_own",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "update_own",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "delete_own",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    }
                ]
        }
    return json_dataTemplate

def create_json_data_subject(componentsSub, form_name_sub):
    json_dataSubject = {
    'title': form_name_sub,
    'display': 'form',
    'type': 'form',
    'name': form_name_sub,
    'path': form_name_sub,
    'components': componentsSub,
    'submissionAccess': [
                    {
                        "type": "create_all",
                        "roles": []
                    },
                    {
                        "type": "read_all",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "update_all",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "delete_all",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "create_own",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "read_own",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "update_own",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    },
                    {
                        "type": "delete_own",
                        "roles": [
                            "64b62e90ffda434186556d58"
                        ]
                    }
                ],

    }
    return json_dataSubject

def collect_user_inputs(name_found, email_found, phone_found):
    user_inputs = {}

    # Ask about recipient email
    if not email_found:
        print("Do you want recipient email?")
        print("1. recipient_email")
        print("2. email")
        print("3. Any other name")
        print("4. Do not want anything")
        choice = input("Please select (1/2/3/4): ")
        user_inputs['email_choice'] = choice
        if choice == '3':
            custom_name = input("Enter the custom name for email: ")
            default_value = input("Enter the default value for email: ")
            user_inputs['email_custom_name'] = custom_name
            user_inputs['email_default_value'] = default_value

    # Ask about recipient phone
    if not phone_found:
        print("Do you want recipient phone?")
        print("1. recipient_phone")
        print("2. phone")
        print("3. Any other name")
        print("4. Do not want anything")
        choice = input("Please select (1/2/3/4): ")
        user_inputs['phone_choice'] = choice
        if choice == '3':
            custom_name = input("Enter the custom name for phone: ")
            default_value = input("Enter the default value for phone: ")
            user_inputs['phone_custom_name'] = custom_name
            user_inputs['phone_default_value'] = default_value

    # Ask about recipient name
    if not name_found:
        print("Do you want recipient name?")
        print("1. recipient_name")
        print("2. full_name")
        print("3. Any other name")
        print("4. Do not want anything")
        choice = input("Please select (1/2/3/4): ")
        user_inputs['name_choice'] = choice
        if choice == '3':
            custom_name = input("Enter the custom name for recipient: ")
            default_value = input("Enter the default value for recipient: ")
            user_inputs['name_custom_name'] = custom_name
            user_inputs['name_default_value'] = default_value

    return user_inputs

def extract_text_fields_subject_properties(texts_subject_properties_tspan, user_inputs):
    text_fields_subject_properties = []
    recipient_email_exists = False 
    email_exists = False
    recipient_phone_exists = False
    phone_exists = False
    recipient_name_exists = False
    full_name_exists = False

    field_line_counts = {}

    for t in texts_subject_properties_tspan:
        data_key = t.get('data-key')
        if data_key:
            if '_row' in data_key:
                base_name = data_key.split('_row')[0]
                field_line_counts[base_name] = field_line_counts.get(base_name, 1) + 1
            else:
                field_line_counts[data_key] = field_line_counts.get(data_key, 1)

    for t in texts_subject_properties_tspan:
        data_type = t.get('data-type')
        data_key = t.get('data-key')
        data_max_characters = t.get('max-characters')
        data_default_value = t.get('data-default-value')
        data_format = t.get('data-format')

        if '_row' in data_key:
            continue

        number_of_lines = field_line_counts.get(data_key, 1)

        if data_type and data_default_value and data_key=='recipientName' and data_max_characters: #! For text fields having recipientName
            recipient_name_exists = True
            name_parts = data_default_value.split()
            recipient_first_name = name_parts[0] if len(name_parts) > 0 else ""
            recipient_last_name = name_parts[1] if len(name_parts) > 1 else ""

            text_fields_subject_properties.append(('recipientFirstName', {
                'type': 'string',
                'max_characters': data_max_characters if data_max_characters else 10,
                'default': recipient_first_name,
                'number_of_lines': 1
            }))
            text_fields_subject_properties.append(('recipientLastName', {
                'type': 'string',
                'max_characters': data_max_characters if data_max_characters else 10,
                'default': recipient_last_name,
                'number_of_lines': 1
            }))
        elif data_type and data_default_value and data_key == 'fullName' and data_max_characters:
            full_name_exists = True
            text_fields_subject_properties.append(('fullName', {
                'type': 'string',
                'max_characters': data_max_characters,
                'default': data_default_value,
                'number_of_lines': 1
            }))
        elif data_type and data_default_value and data_key == 'recipientEmail' and data_max_characters:
            recipient_email_exists = True
            text_fields_subject_properties.append(('recipientEmail', {
                'type': 'string',
                'max_characters': data_max_characters,
                'default': data_default_value,
                'number_of_lines': 1
            }))
        elif data_type and data_default_value and data_key == 'email' and data_max_characters:
            email_exists = True
            text_fields_subject_properties.append(('email', {
                'type': 'string',
                'max_characters': data_max_characters,
                'default': data_default_value,
                'number_of_lines': 1
            }))
        elif data_type and data_default_value and data_key == 'recipientPhone' and data_max_characters:
            recipient_phone_exists = True
            text_fields_subject_properties.append(('recipientPhone', {
                'type': 'string',
                'max_characters': data_max_characters,
                'default': data_default_value,
                'number_of_lines': 1
            }))
        elif data_type and data_default_value and data_key == 'phone' and data_max_characters:
            phone_exists = True
            text_fields_subject_properties.append(('phone', {
                'type': 'string',
                'max_characters': data_max_characters,
                'default': data_default_value,
                'number_of_lines': 1
            }))
        elif data_type and data_default_value and data_key!='recipientName' and data_max_characters and not data_format: #! For text fields except recipientName
            text_field = {
                'type': 'string',
                'max_characters': data_max_characters,
                'default': data_default_value,
                'number_of_lines': number_of_lines
            }
            text_fields_subject_properties.append((data_key, text_field))
        elif data_type and data_key and data_default_value and data_format: #! Now, only for date format
            text_field = {
                'type': 'date',
                'format': data_format,
                'default': data_default_value,
                'number_of_lines': 1
            }
            text_fields_subject_properties.append((data_key, text_field))

    if not recipient_email_exists and not email_exists:
        email_choice = user_inputs.get('email_choice')

        if email_choice == '1':
            recipient_email_component = {
                'type': 'string',
                'max_characters': 55,
                'default': "john1234@example.com",
                'number_of_lines': 1
            }
            text_fields_subject_properties.append(("recipientEmail", recipient_email_component))
        elif email_choice == '2':
            text_fields_subject_properties.append(("email", {
                'type': 'string',
                'max_characters': 55,
                'default': "example@example.com",
                'number_of_lines': 1
            }))
        elif email_choice == '3':
            custom_name = user_inputs.get('email_custom_name')
            default_value = user_inputs.get('email_default_value')
            text_fields_subject_properties.append((custom_name, {
                'type': 'string',
                'max_characters': 55,
                'default': default_value,
                'number_of_lines': 1
            }))

    if not recipient_phone_exists and not phone_exists:
        phone_choice = user_inputs.get('phone_choice')
        if phone_choice == '1':
            recipient_phone_component = {
                'type': 'string',
                'max_characters': 10,
                'default': "1234567890",
                'number_of_lines': 1
            }
            text_fields_subject_properties.append(("recipientPhone",recipient_phone_component))
        elif phone_choice == '2':
            text_fields_subject_properties.append(("phone", {
                'type': 'string',
                'max_characters': 10,
                'default': "1234567890",
                'number_of_lines': 1
            }))
        elif phone_choice == '3':
            custom_name = user_inputs.get('phone_custom_name')
            default_value = user_inputs.get('phone_default_value')
            text_fields_subject_properties.append((custom_name, {
                'type': 'string',
                'max_characters': 10,
                'default': default_value,
                'number_of_lines': 1
            }))

    if not recipient_name_exists and not full_name_exists:
        name_choice = user_inputs.get('name_choice')
        if name_choice == '1':
            recipient_first_name_component = {
                'type': 'string',
                'max_characters': 20,
                'default': "John",
                'number_of_lines': 1
            }
            text_fields_subject_properties.append(("recipientFirstName",recipient_first_name_component))
            recipient_last_name_component = {
                'type': 'string',
                'max_characters': 20,
                'default': "Doe",
                'number_of_lines': 1
            }
            text_fields_subject_properties.append(("recipientLastName",recipient_last_name_component))
        elif name_choice == '2':
            text_fields_subject_properties.append(("fullName", {
                'type': 'string',
                'max_characters': 40,
                'default': "John Doe",
                'number_of_lines': 1
            }))
        elif name_choice == '3':
            custom_name = user_inputs.get('name_custom_name')
            default_value = user_inputs.get('name_default_value')
            text_fields_subject_properties.append((custom_name, {
                'type': 'string',
                'max_characters': 40,
                'default': default_value,
                'number_of_lines': 1
            }))

    return text_fields_subject_properties


def extract_image_fields_subject_properties(images_schema):
    image_fields_subject_properties = []
    for i in images_schema:
        data_type = i.get('data-type')
        data_key = i.get('data-key')
        data_max_size = i.get('max-size')

        if data_type and data_key and data_max_size:
            image_field = {
                'type': 'file',
                'max_size': data_max_size,
                'default': 'base64 string'
            }
            image_fields_subject_properties.append((data_key, image_field))
    return image_fields_subject_properties
    

# Context# Context# Context# Context# Context# Context# Context
def extract_image_fields_context(images_schema) : 
    image_fields_context = []
    for i in images_schema:
        data_type = i.get('data-type')
        data_label = i.get('data-label')
        data_key = i.get('data-key')
        if data_type and data_label and data_key:
            image_field = {
                "key":data_key,
                "value" : "schema:Text"
            }
            image_fields_context.append(image_field)
    return image_fields_context

def extract_text_fields_context(texts_context, user_inputs):
    text_fields_context = []
    seen_base_fields = set()
    recipient_email_exists = False 
    email_exists = False
    recipient_phone_exists = False
    phone_exists = False
    recipient_name_exists = False
    full_name_exists = False

    for t in texts_context:
        data_key = t.get('data-key')
        if not data_key:
            continue
        if '_row' in data_key:
            continue
            
        data_type = t.get('data-type')
        data_label = t.get('data-label')

        if data_key not in seen_base_fields:
            seen_base_fields.add(data_key)
            text_field = {
                "key": data_key,
                "value": "schema:Text"
            }
            text_fields_context.append(text_field)
        if data_type and data_label and data_key:
            if data_key == 'recipientEmail':
                recipient_email_exists = True
            elif data_key == 'email':
                email_exists = True
            elif data_key == 'recipientPhone':
                recipient_phone_exists = True
            elif data_key == 'phone':
                phone_exists = True
            elif data_key == 'recipientName':
                recipient_name_exists = True
            elif data_key == 'fullName':
                full_name_exists = True
            text_field = {
                "key":data_key,
                "value" : "schema:Text"
            }
            text_fields_context.append(text_field)

    if not recipient_email_exists and not email_exists:
        email_choice = user_inputs.get('email_choice')

        if email_choice == '1':
            recipient_email_component = {
                "key":"recipientEmail",
                "value" : "schema:Text"
            }
            text_fields_context.append(recipient_email_component)
        elif email_choice == '2':
            text_fields_context.append({
                "key": "email",
                "value": "schema:Text"
            })
        elif email_choice == '3':
            custom_name = user_inputs.get('email_custom_name')
            text_fields_context.append({
                "key": custom_name,
                "value": "schema:Text"
            })

    if not recipient_phone_exists and not phone_exists:
        phone_choice = user_inputs.get('phone_choice')
        if phone_choice == '1':
            recipient_phone_component = {
                "key":"recipientPhone",
                "value" : "schema:Text"
            }
            text_fields_context.append(recipient_phone_component)
        elif phone_choice == '2':
            text_fields_context.append({
                "key": "phone",
                "value": "schema:Text"
            })
        elif phone_choice == '3':
            custom_name = user_inputs.get('phone_custom_name')
            text_fields_context.append({
                "key": custom_name,
                "value": "schema:Text"
            })

    if not recipient_name_exists and not full_name_exists:
        name_choice = user_inputs.get('name_choice')
        if name_choice == '1':
            recipient_name_component = {
                "key":"recipientName",
                "value" : "schema:Text"
            }
            text_fields_context.append(recipient_name_component)
        elif name_choice == '2':
            text_fields_context.append({
                "key": "fullName",
                "value": "schema:Text"
            })
        elif name_choice == '3':
            custom_name = user_inputs.get('name_custom_name')
            text_fields_context.append({
                "key":  custom_name,
                "value": "schema:Text"
            })

    return text_fields_context

def create_json_schema(folder_name, text_fields_context, image_fields_context):
    context = {
        "@version": 1.1,
        "@protected": True,
        "id": "@id",
        "schema": "https://schema.org/",
        folder_name: {
            "@id": "iri:3425",
            "@context": {
                "@version": 1.1,
                "id": "@id",
            }
        }
    }
    for item in text_fields_context:
        context[folder_name]["@context"][item["key"]] = item["value"]
    for item in image_fields_context:
        context[folder_name]["@context"][item["key"]] = item["value"]

    return context

def create_schema_dataset(json_data_context):
    json_dataset_context ={
                "@context":json_data_context
            }
    return json_dataset_context

# Schema# Schema# Schema# Schema# Schema# Schema# Schema# Schema
def extract_image_fields_schema(images_schema):
    image_fields_schema = []
    for i in images_schema:
        data_type = i.get('data-type')
        data_label = i.get('data-label')
        data_key = i.get('data-key')
        data_description = i.get('data-description')
        if data_type and data_label and data_key and data_description:
            image_field = {
                'type': 'string',
                'description': data_description
            }
            image_fields_schema.append((data_key, image_field))
    return image_fields_schema

def extract_text_fields_schema(texts_schema, user_inputs, new_attributes=None):
    text_fields_schema = []
    seen_base_fields = set()

    recipient_email_exists = False 
    email_exists = False
    recipient_phone_exists = False
    phone_exists = False
    recipient_name_exists = False
    full_name_exists = False

    for t in texts_schema:
        data_key = t.get('data-key')
        if not data_key:
            continue

        if '_row' in data_key:
            continue

        data_type = t.get('data-type')
        data_label = t.get('data-label')
        data_description = t.get('data-description')
        data_required = t.get('data-required', 'True').lower() == 'true'

        if data_key not in seen_base_fields:
            seen_base_fields.add(data_key)

        if data_type and data_label and data_key:
            if data_key == 'recipientEmail':
                recipient_email_exists = True
            elif data_key == 'email':
                email_exists = True
            elif data_key == 'recipientPhone':
                recipient_phone_exists = True
            elif data_key == 'phone':
                phone_exists = True
            elif data_key == 'recipientName':
                recipient_name_exists = True
            elif data_key == 'fullName':
                full_name_exists = True
            text_field = {
                'type': 'string',
                'description': data_description if data_description else f"{data_key} for the certificate",
                'is_required': data_required
            }
            text_fields_schema.append((data_key, text_field))

    if not recipient_email_exists and not email_exists:
        email_choice = user_inputs.get('email_choice')
        if email_choice == '1':
            recipient_email_component = {
                'type': 'string',
                'description': "Email for the certificate",
                'is_required': True
            }
            text_fields_schema.append(("recipientEmail", recipient_email_component))
        elif email_choice == '2':
            text_fields_schema.append(("email", {
                'type': 'string',
                'description': "Email for the certificate",
                'is_required': True
            }))
        elif email_choice == '3':
            custom_name = user_inputs.get('email_custom_name')
            text_fields_schema.append((custom_name, {
                'type': 'string',
                'description': custom_name + " for the certificate",
                'is_required': True
            }))

    if not recipient_phone_exists and not phone_exists:
        phone_choice = user_inputs.get('phone_choice')
        if phone_choice == '1':
            recipient_phone_component = {
                'type': 'string',
                'description': "Phone number for the certificate",
                'is_required': True
            }
            text_fields_schema.append(("recipientPhone",recipient_phone_component))
        elif phone_choice == '2':
            text_fields_schema.append(("phone", {
                'type': 'string',
                'description': "Phone number for the certificate",
                'is_required': True
            }))
        elif phone_choice == '3':
            custom_name = user_inputs.get('phone_custom_name')
            text_fields_schema.append((custom_name, {
                'type': 'string',
                'description': custom_name + " for the certificate",
                'is_required': True
            }))

    if not recipient_name_exists and not full_name_exists:
        name_choice = user_inputs.get('name_choice')
        if name_choice == '1':
            recipient_name_component = {
                'type': 'string',
                'description': "Recipient Name for the certificate",
                'is_required': True
            }
            text_fields_schema.append(("recipientName",recipient_name_component))
        elif name_choice == '2':
            text_fields_schema.append(("fullName", {
                'type': 'string',
                'description': "Full Name for the certificate",
                'is_required': True
            }))
        elif name_choice == '3':
            custom_name = user_inputs.get('name_custom_name')
            text_fields_schema.append((custom_name, {
                'type': 'string',
                'description': custom_name + " for the certificate",
                'is_required': True
            }))

    if new_attributes:
        for attr in new_attributes:
            text_fields_schema.append((attr["key"], {
                'type': 'string',
                'description': attr["description"],
                'is_required': attr["is_required"]
            }))

    return text_fields_schema

def create_json_context(folder_name, text_fields_schema, image_fields_schema, certificate_description):
    schema = {
        "type": "https://w3c-ccg.github.io/vc-json-schemas/",
        "version": "1.0.0",
        "id": "",
        "name": folder_name,
        "author": "",
        "authored": "",
        "schema": {
            "$id": folder_name.replace(" ", "-"),
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "description": certificate_description,
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": True
        },
        "tags": [
            "tag1",
            "tag2"
        ],
        "status": "DRAFT"
    }

    for key, field in text_fields_schema:
        field_copy = field.copy()
        if 'is_required' in field_copy:
            if field_copy['is_required']:
                schema["schema"]["required"].append(key)
            del field_copy['is_required']
        schema["schema"]["properties"][key] = field_copy

    for key, field in image_fields_schema:
        field_copy = field.copy()
        if 'is_required' in field_copy:
            if field_copy['is_required']:
                schema["schema"]["required"].append(key)
            del field_copy['is_required']
        schema["schema"]["properties"][key] = field_copy

    schema["schema"]["required"] = list(set(schema["schema"]["required"]))

    return schema

def create_context_dataset(json_data_schema):
    json_dataset_schema = {
        "schema": json_data_schema
    }
    return json_dataset_schema

def create_qr_code_json(images_schema_qr):
    for i in images_schema_qr:
        data_qr_type = i.get('data-qr-type')
        data_qr_style = i.get('data-qr-style')
        data_qr_color1 = i.get('data-qr-color1')
        data_qr_color2 = i.get('data-qr-color2')
        data_qr_height = i.get('height')
        data_qr_width = i.get('width')
        if data_qr_type and data_qr_color1 and data_qr_color2:
            qr_field_2 = {
                'width': data_qr_width,
                'height': data_qr_height,
                'dotsOptions':{
                'type': data_qr_style,
                data_qr_type:{
                    'colorStops':[
                        {
                'color1': data_qr_color1,
                        },
                        {
                'color2': data_qr_color2,
                        }
                    ]
                }
                }
            }
            return qr_field_2
        if data_qr_type and data_qr_color1:
            qr_field_1 = {
                'width': data_qr_width,
                'height': data_qr_height,
                'dotsOptions':{
                'type': data_qr_style,
                'color1': data_qr_color1,

                }
            }
            return qr_field_1
    return {}

def create_json_data_certificate(folder_name, temp, subj,json_schema,json_context,  certificate_name, certificate_description, qr_code_json, json_data_subject_properties):
    json_data_d = {
    "credential_schema":json_schema,
    "credential_context":json_context,
    "template_form_id":temp,
    "subject_form_id":subj,
    "folder_name": folder_name,
    "credential_name":certificate_name,
    "description":certificate_description,
    "qr_code_options":qr_code_json,
    "subject_properties":json_data_subject_properties
    }
    json_data = json.dumps(json_data_d, indent=4)
    return json_data


def create_json_subject_properties(text_fields_subject_properties, image_fields_subject_properties):
    schema_subject_properties = {
        
    }

    for key, field in text_fields_subject_properties:
        schema_subject_properties[key] = field

    for key, field in image_fields_subject_properties:
        schema_subject_properties[key] = field

    return schema_subject_properties


def create_subject_properties_dataset(json_data_subject_properties):
    json_dataset_subject_properties = {
        "schema": json_data_subject_properties
    }
    return json_dataset_subject_properties

def prompt_for_new_data_attributes():
    new_attributes = []
    while True:
        print("Do you want to add new data-attributes?")
        print("1. Yes")
        print("2. No")
        choice = input("Please select (1/2): ")

        if choice == '1':
            attribute_name = input("Enter the data-attribute name: ")
            max_characters = input("Enter the maximum number of characters (e.g., 55): ")
            default_value = input("Enter the default value: ")
            description = input("Enter the description: ")
            number_of_lines = input("Enter the number of lines needed (default is 1): ")
            
            print("Should this field be required?")
            print("1. Yes")
            print("2. No")
            required_choice = input("Please select (1/2): ")
            is_required = True if required_choice == '1' else False
            
            # Set default if no input provided
            number_of_lines = int(number_of_lines) if number_of_lines else 1

            new_attribute = {
                "key": attribute_name,
                "value": "schema:Text",
                'type': 'string',
                'max_characters': int(max_characters),
                'default': default_value,
                'description': description,
                'number_of_lines': number_of_lines,
                'is_required': is_required
            }
            new_attributes.append(new_attribute)
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please select 1 or 2.")
    return new_attributes

def process_svg_files_in_folder(folder_path, dry_run=True, config_file="../scripts/config.yaml"):
    svg_path = None
    for file in os.listdir(folder_path):
        if file.startswith("templateVariables") and file.endswith(".svg"):
            svg_path = os.path.join(folder_path, file)
            print("svg_path : ", svg_path)
            break
    

    if svg_path:
        GREEN = '\033[92m'
        RESET = '\033[0m'
        RED = '\033[91m'
        VIOLET = '\033[95m'
        BLUE = '\033[94m'
        folder_name = os.path.basename(os.path.dirname(svg_path))
        folder_path = os.path.dirname(svg_path)
        svg_content = read_svg(svg_path)
        soup = BeautifulSoup(svg_content, 'xml')
        print("the folder_name is : ", folder_name)
        print("The folder path is : ", folder_path)

        config_file = read_yaml_config(config_file)
        form_url = config_file["dpi"]["form_url"]
        app_url = config_file["dpi"]["app_url"]
        
        folder_config_file = os.path.join(folder_path, 'config.yaml')
        folder_config = read_yaml_config(folder_config_file)

        certificate_name = folder_config.get('certificate_name', 'Certificate')
        print("certificate_name : ", certificate_name)
        certificate_description = folder_config.get('certificate_description', 'Certificate')
        print("certificate_description : ", certificate_description)

        # ! Check if SVG contains 'fullName', 'recipientName', 'email', 'recipientEmail', 'phone', 'recipientPhone' or not !
        name_keys_to_extract = ['fullName', 'recipientName']
        email_keys_to_extract = ['email', 'recipientEmail']
        phone_keys_to_extract = ['phone', 'recipientPhone']
        name_found = soup.find_all(['text', 'tspan'], {'data-key': name_keys_to_extract})
        email_found = soup.find_all(['text', 'tspan'], {'data-key': email_keys_to_extract})
        phone_found = soup.find_all(['text', 'tspan'], {'data-key': phone_keys_to_extract})
        user_inputs = collect_user_inputs(name_found, email_found, phone_found)

        # ! Prompt for new data attributes
        new_attributes = prompt_for_new_data_attributes()

        # ! Find the text Fields(including text and tspan) in the svg
        texts = soup.find_all('text', {'data-form-type': ['template', 'subject']})
        texts = texts + soup.find_all('tspan', {'data-form-type': ['template', 'subject']})
        # ! Find the images in the svg
        images = soup.find_all('image', {'data-form-type': ['template', 'subject']})

        # ! Find the text Fields(including text and tspan) in the svg for Schema
        texts_schema_text = soup.find_all('text', {'data-form-type': 'subject'})
        texts_schema_tspan = texts_schema_text + soup.find_all('tspan', {'data-form-type': 'subject'})
        
        # ! Find the text Fields(including text and tspan) in the svg for Context
        texts_context_text = soup.find_all('text', {'data-form-type': 'subject'})
        texts_context_tspan = texts_context_text + soup.find_all('tspan', {'data-form-type': 'subject'})

        # ! Find the text Fields(including text and tspan) in the svg for Subject Properties
        texts_subject_properties_text = soup.find_all('text', {'data-form-type': 'subject'})
        texts_subject_properties_tspan = texts_subject_properties_text + soup.find_all('tspan', {'data-form-type': 'subject'})

        # print("The sujcet properties for subjcet _properties are : ", texts_subject_properties_tspan)

        # ! Find the images which has Photo in svg
        images_schema = soup.find_all('image', {'data-type': 'photo'})
        images_schema_qr = soup.find_all('image', {'data-qr-type': 'gradient'}) if soup.find_all('image', {'data-qr-type': 'gradient'}) else soup.find_all('image', {'data-qr-type': 'linear'})

        qr_code_json = create_qr_code_json(images_schema_qr)
        
        # ! These are the Text & Image field in Schema 
        text_fields_schema = extract_text_fields_schema(texts_schema_tspan, user_inputs, new_attributes)

        for attr in new_attributes:
            text_fields_schema.append((attr["key"], {
                'type': 'string',
                'description': attr["description"]
            }))
        image_fields_schema = extract_image_fields_schema(images_schema)

        # ! These are the Text & Image field in Context
        text_fields_context = extract_text_fields_context(texts_context_tspan, user_inputs)

        # Add new attributes to context
        for attr in new_attributes:
            text_fields_context.append({
                "key": attr["key"],
                "value": "schema:Text"
            })
        image_fields_context = extract_image_fields_context(images_schema)

        # ! These are the Text & Image field in Subject Properties
        text_fields_subject_properties = extract_text_fields_subject_properties(texts_subject_properties_tspan, user_inputs)

        # Add new attributes to subject properties
        for attr in new_attributes:
            text_fields_subject_properties.append((attr["key"], {
                'type': 'string',
                'max_characters': attr["max_characters"],
                'default': attr["default"],
                'number_of_lines': attr["number_of_lines"]
            }))
        image_fields_subject_properties = extract_image_fields_subject_properties(images_schema)
        # print(f"{RED}The Image field Subject Properties is : \n {image_fields_subject_properties}{RESET}")


        # ! Default components for Form.io 
        
        components = []
        componentsSub = []  

        # ! The Form.io Updated Components for Template & Subject fields
        components, componentsSub = get_components(texts,images, default_components, user_inputs, new_attributes)

        # ! Name for Form.io
        data_name = folder_name.strip()
        form_name_sub = f'subject{data_name}'
        form_name_temp = f'template{data_name}'

        # ! Full Form.io component for Template & Subject
        json_data_template = create_json_data_template(components, form_name_temp)
        print(f"{GREEN}Full Form.io component for Template : \n {json_data_template}{RESET}")
        json_data_subject = create_json_data_subject(componentsSub, form_name_sub)
        print(f"{RED}Full Form.io component for Subject : \n {json_data_subject}{RESET}")

        # ! Creating Context
        json_data_context = create_json_context(folder_name, text_fields_schema, image_fields_schema, certificate_description)
        json_context = create_context_dataset(json_data_context)
        
        # ! Creating Schema.json
        json_data_schema = create_json_schema(folder_name, text_fields_context, image_fields_context)
        json_schema = create_schema_dataset(json_data_schema)

        # ! Creating Subject Properties
        json_data_subject_properties = create_json_subject_properties(text_fields_subject_properties, image_fields_subject_properties)
        components.append(submit)
        componentsSub.append(submit)


        def write_to_file(folder_path, file_name, data):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

        def create_json_files(folder_path, json_context, json_schema, json_data_subject_properties):
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            write_to_file(folder_path, "context.json", json_schema)
            write_to_file(folder_path, "sunbirdrc-schema.json", json_context)
            write_to_file(folder_path, "credential-subject-properties.json", json_data_subject_properties)

        create_json_files(folder_path, json_context, json_schema, json_data_subject_properties)

        # ! Creating Forms for Template & Subject
        headers_form = {
                'Accept': '*/*',
                'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
                'Content-Type': 'application/json',
                'x-jwt-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjY4ZTM4YWMyMzUyZTQwMTQxMDljMDM5NiJ9LCJmb3JtIjp7Il9pZCI6IjY4ZTM4YWMyMzUyZTQwMTQxMDljMDM2MSJ9LCJpYXQiOjE3NTk5ODg1NzAsImV4cCI6MTc2MDAwMjk3MH0.lW0W6-RBBKhnLIPUyqtFnZHCYg1hhT1rFEqhNxiZjPY'
                }
        temp = None 
        subj = None
        if not dry_run:
            temp = POST(form_url, headers_form, json_data_template)
            print(f"{BLUE}The Template form ID is : \n {temp}{RESET}")
        if not dry_run:
            subj = POST(form_url, headers_form, json_data_subject)
            print(f"{BLUE}The Subject form ID is : \n {subj}{RESET}")
        temp = temp if temp else ""
        subj = subj if subj else ""
        # ! OverAll JSON data for Certificates
        if not dry_run:
            json_data_certificate = create_json_data_certificate(
                folder_name, temp, subj, json_context, json_schema, certificate_name, certificate_description, qr_code_json, json_data_subject_properties
            )
        else:
            print(f"{VIOLET}Dry run: Skipping certificate creation.{RESET}")

        # ! API for Creating Certificates
        headers_template = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer MKJf1qgg1IBvJ6FdiLsFEZsPTpjch4BrUXyrJ'       #(DPI)
        }
        if not dry_run:
            response = requests.post(url=app_url, headers=headers_template, data=json_data_certificate)

            if response.status_code == 200:
                print("Request successful")
                print(response.json())
            else:
                print(f"Request failed with status code: {response.status_code}")
                print(response.text)

if __name__ == "__main__":
    folder_path = '../IdCard08' 
    config_file = "../scripts/config.yaml"
    dry_run = False if sys.argv[1].lower() == "false" else True

    process_svg_files_in_folder(folder_path, dry_run, config_file)


# For Dry Run : 
# python3 qr_templateScriptForSingleIssuance.py true

# For Actual API Call :
# python3 qr_templateScriptForSingleIssuance.py false