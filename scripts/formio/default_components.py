default_components = {
        "textfield":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "inputType": "text",
                "inputMask": "",
                "label": "textfield",
                "key": "textField",
                "placeholder": "",
                "prefix": "",
                "suffix": "",
                "multiple": False,
                "defaultValue": "",
                "protected": False,
                "unique": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "spellcheck": True,
                "validate": {
                    "required": True,
                    "minLength": "",
                    "maxLength": "",
                    "pattern": "",
                    "custom": "",
                    "customPrivate": False
                },
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "type": "textfield",
                "labelPosition": "top",
                "inputFormat": "plain",
                "tags": [],
                "properties": {}
            },
        "date": {
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "Date",
                "key": "date",
                "placeholder": "",
                "format": "dd-MM-yyyy hh:mm a",
                "enableDate": True,
                "enableTime": False,
                "defaultDate": "",
                "datepickerMode": "day",
                "datePicker": {
                    "showWeeks": True,
                    "startingDay": 0,
                    "initDate": "",
                    "minMode": "day",
                    "maxMode": "year",
                    "yearRows": 4,
                    "yearColumns": 5,
                    "minDate": None,
                    "maxDate": None,
                    "datepickerMode": "day"
                },
                "timePicker": {
                    "hourStep": 1,
                    "minuteStep": 1,
                    "showMeridian": True,
                    "readonlyInput": False,
                    "mousewheel": True,
                    "arrowkeys": True
                },
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "validate": {
                    "required": True,
                    "custom": ""
                },
                "type": "datetime",
                "labelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
                },
            # "dateOfBirth":{
            #     "autofocus": False,
            #     "input": True,
            #     "tableView": True,
            #     "label": "Date Of Birth",
            #     "key": "dob",
            #     "placeholder": "",
            #     "format": "dd-MM-yyyy",
            #     "enableDate": True,
            #     "enableTime": False,
            #     "defaultDate": "",
            #     "datepickerMode": "day",
            #     "datePicker": {
            #         "showWeeks": True,
            #         "startingDay": 0,
            #         "initDate": "",
            #         "minMode": "day",
            #         "maxMode": "day",
            #         "yearRows": 4,
            #         "yearColumns": 5,
            #         "minDate": None,
            #         "maxDate": None,
            #         "datepickerMode": "day"
            #     },
            #     "timePicker": {
            #         "hourStep": 1,
            #         "minuteStep": 1,
            #         "showMeridian": True,
            #         "readonlyInput": False,
            #         "mousewheel": True,
            #         "arrowkeys": True
            #     },
            #     "protected": False,
            #     "persistent": True,
            #     "hidden": False,
            #     "clearOnHide": True,
            #     "validate": {
            #         "required": True,
            #         "custom": "var datePattern = 'YYYY-MM-DD';\nvar userShowPattern = 'DD-MM-YYYY';\nvar selectedDate = moment(data.dob).format(datePattern); \nvar today = moment().format(datePattern);\nif (moment(selectedDate).isSameOrBefore(today)) \n{ valid = True; \n// Validation passes \n} else { valid = `Date Of Birth cannot be more than ${moment().format(userShowPattern)}`;\n\n}// Validation fails, set custom error message }",
            #         "customMessage": ""
            #     },
            #     "type": "datetime",
            #     "labelPosition": "top",
            #     "tags": [],
            #     "conditional": {
            #         "show": "",
            #         "when": None,
            #         "eq": ""
            #     },
            #     "properties": {},
            #     "customConditional": "",
            #     "lockKey": True,
            #     "isNew": False
            # },
            "number":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "inputType": "number",
                "label": "Number",
                "key": "number",
                "placeholder": "",
                "prefix": "",
                "suffix": "",
                "defaultValue": "",
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "validate": {
                    "required": True,
                    "min": "",
                    "max": "",
                    "step": "any",
                    "integer": "",
                    "multiple": "",
                    "custom": ""
                },
                "type": "number",
                "labelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "password":{
                "autofocus": False,
                "input": True,
                "tableView": False,
                "inputType": "password",
                "label": "Password",
                "key": "password",
                "placeholder": "",
                "prefix": "",
                "suffix": "",
                "protected": True,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "type": "password",
                "labelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "textArea":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "Text Area",
                "key": "textArea",
                "placeholder": "",
                "prefix": "",
                "suffix": "",
                "rows": 3,
                "multiple": False,
                "defaultValue": "",
                "protected": False,
                "persistent": True,
                "hidden": False,
                "wysiwyg": False,
                "clearOnHide": True,
                "spellcheck": True,
                "validate": {
                    "required": True,
                    "minLength": "",
                    "maxLength": "",
                    "pattern": "",
                    "custom": ""
                },
                "type": "textarea",
                "labelPosition": "top",
                "inputFormat": "plain",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "signature":{
                "input": True,
                "tableView": True,
                "label": "Signature",
                "key": "signature",
                "placeholder": "",
                "footer": "Sign above",
                "width": "100%",
                "height": "150px",
                "penColor": "black",
                "backgroundColor": "rgb(245,245,235)",
                "minWidth": "0.5",
                "maxWidth": "2.5",
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "validate": {
                    "required": True
                },
                "type": "signature",
                "hideLabel": True,
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "currency":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "inputType": "text",
                "inputMask": "",
                "label": "Currency",
                "key": "currency",
                "placeholder": "",
                "prefix": "",
                "suffix": "",
                "defaultValue": "",
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "delimiter": True,
                "decimalLimit": 2,
                "requireDecimal": True,
                "validate": {
                    "required": True,
                    "multiple": "",
                    "custom": ""
                },
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "type": "currency",
                "labelPosition": "top",
                "tags": [],
                "properties": {}
            },
            "photo":
            {
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "File",
                "key": "file",
                "image": False,
                "imageSize": "200",
                "placeholder": "",
                "multiple": False,
                "defaultValue": "",
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "filePattern": "*",
                "fileMinSize": "0KB",
                "fileMaxSize": "1GB",
                "type": "file",
                "labelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {},
                "hideLabel": False,
                "validate": {
                    "required": True
                },
                "lockKey": True,
                "storage": "base64"
            },
            "logo":
            {
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "File",
                "key": "file",
                "image": False,
                "imageSize": "200",
                "placeholder": "",
                "multiple": False,
                "defaultValue": "",
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "filePattern": "*",
                "fileMinSize": "0KB",
                "fileMaxSize": "1GB",
                "type": "file",
                "labelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {},
                "hideLabel": False,
                "validate": {
                    "required": False
                },
                "lockKey": True,
                "storage": "base64"
            },
            "day":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "Day",
                "key": "day",
                "fields": {
                    "day": {
                        "type": "number",
                        "placeholder": "",
                        "required": True
                    },
                    "month": {
                        "type": "select",
                        "placeholder": "",
                        "required": True
                    },
                    "year": {
                        "type": "number",
                        "placeholder": "",
                        "required": True
                    }
                },
                "dayFirst": True,
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "validate": {
                    "custom": ""
                },
                "type": "day",
                "labelPosition": "top",
                "inputsLabelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "time":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "inputType": "time",
                "format": "HH:mm",
                "label": "Time",
                "key": "time",
                "placeholder": "",
                "prefix": "",
                "suffix": "",
                "defaultValue": "",
                "protected": False,
                "unique": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "type": "time",
                "labelPosition": "top",
                "inputFormat": "plain",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {},
                "isNew": False
            },
            "dateTime":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "Date Time",
                "key": "dateTime",
                "placeholder": "",
                "format": "yyyy-MM-dd hh:mm a",
                "enableDate": True,
                "enableTime": True,
                "defaultDate": "",
                "datepickerMode": "day",
                "datePicker": {
                    "showWeeks": True,
                    "startingDay": 0,
                    "initDate": "",
                    "minMode": "day",
                    "maxMode": "year",
                    "yearRows": 4,
                    "yearColumns": 5,
                    "minDate": None,
                    "maxDate": None,
                    "datepickerMode": "day"
                },
                "timePicker": {
                    "hourStep": 1,
                    "minuteStep": 1,
                    "showMeridian": True,
                    "readonlyInput": False,
                    "mousewheel": True,
                    "arrowkeys": True
                },
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "validate": {
                    "required": True,
                    "custom": ""
                },
                "type": "datetime",
                "labelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {},
                "isNew": False
            },
            "address":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "Address",
                "key": "address",
                "placeholder": "",
                "multiple": False,
                "protected": False,
                "clearOnHide": True,
                "unique": False,
                "persistent": True,
                "hidden": False,
                "map": {
                    "region": "",
                    "key": ""
                },
                "validate": {
                    "required": True
                },
                "type": "address",
                "labelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "checkbox":{
                "autofocus": False,
                "input": True,
                "inputType": "checkbox",
                "tableView": True,
                "label": "checkboxField",
                "dataGridLabel": False,
                "key": "checkboxField",
                "defaultValue": False,
                "protected": False,
                "persistent": True,
                "hidden": False,
                "name": "",
                "value": "",
                "clearOnHide": True,
                "validate": {
                    "required": True
                },
                "type": "checkbox",
                "labelPosition": "right",
                "hideLabel": True,
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "selectBoxes":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "Select Boxes",
                "key": "selectBoxes",
                "values": [
                    {
                        "value": "",
                        "label": "",
                        "shortcut": ""
                    }
                ],
                "inline": False,
                "protected": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "validate": {
                    "required": True
                },
                "type": "selectboxes",
                "labelPosition": "top",
                "optionsLabelPosition": "right",
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "select":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "label": "Select",
                "key": "select",
                "placeholder": "",
                "data": {
                    "values": [
                        {
                            "value": "",
                            "label": ""
                        }
                    ],
                    "json": "",
                    "url": "",
                    "resource": "",
                    "custom": ""
                },
                "dataSrc": "values",
                "valueProperty": "",
                "defaultValue": "",
                "refreshOn": "",
                "filter": "",
                "authenticate": False,
                "template": "<span>{{ item.label }}</span>",
                "multiple": False,
                "protected": False,
                "unique": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "validate": {
                    "required": True
                },
                "type": "select",
                "labelPosition": "top",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            "phone":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "inputType": "text",
                "inputMask": "",
                "label": "Phone Number",
                "key": "phoneNumber",
                "placeholder": "",
                "prefix": "",
                "suffix": "",
                "multiple": False,
                "defaultValue": "1234567890",
                "protected": False,
                "unique": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "spellcheck": True,
                "validate": {
                    "required": True,
                    "minLength": "",
                    "maxLength": "",
                    "pattern": "",
                    "custom": "const phoneRegex = /^(\\+\\d{1,2}\\s?)?(\\(?\\d{3}\\)?[\\s.-]?)?\\d{3}[\\s.-]?\\d{4}$/;\n\nif (input.trim() === \"\") {\n  valid = true; \n} else if (!phoneRegex.test(input)) {\n  valid = \"Enter a Valid Phone Number\";\n} else {\n  valid = true;\n}\n",
                    "customPrivate": False,
                    "customMessage": ""
                },
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "type": "textfield",
                "labelPosition": "top",
                "inputFormat": "plain",
                "tags": [],
                "properties": {}
            },
            "radio":{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "inputType": "radio",
                "label": "Radio",
                "key": "radio",
                "values": [
                    {
                        "value": "",
                        "label": "",
                        "shortcut": ""
                    }
                ],
                "defaultValue": "",
                "protected": False,
                "fieldSet": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "validate": {
                    "required": True,
                    "custom": "",
                    "customPrivate": False
                },
                "type": "radio",
                "labelPosition": "top",
                "optionsLabelPosition": "right",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {}
            },
            'email':{
                "autofocus": False,
                "input": True,
                "tableView": True,
                "inputType": "email",
                "label": "Email",
                "key": "email",
                "placeholder": "",
                "prefix": "",
                "suffix": "",
                "defaultValue": "",
                "protected": False,
                "unique": False,
                "persistent": True,
                "hidden": False,
                "clearOnHide": True,
                "kickbox": {
                    "enabled": False
                },
                "type": "email",
                "labelPosition": "top",
                "inputFormat": "plain",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {},
                "validate": {
                    "required": True
                }
            }
        
    }
submit = {
                "autofocus": False,
                "input": True,
                "label": "Submit",
                "tableView": False,
                "key": "submit",
                "size": "md",
                "leftIcon": "",
                "rightIcon": "",
                "block": False,
                "action": "submit",
                "disableOnInvalid": False,
                "theme": "primary",
                "type": "button",
                "tags": [],
                "conditional": {
                    "show": "",
                    "when": None,
                    "eq": ""
                },
                "properties": {},
                "customClass": "cw_btn_2 rounded-md"
            }


recipient_first_name_field = {
        "autofocus": False,
        "input": True,
        "tableView": True,
        "inputType": "text",
        "inputMask": "",
        "label": "Recipient First Name",
        "key": "recipientFirstName",
        "placeholder": "",
        "prefix": "",
        "suffix": "",
        "multiple": False,
        "defaultValue": "John",
        "protected": False,
        "unique": False,
        "persistent": True,
        "hidden": False,
        "clearOnHide": True,
        "spellcheck": True,
        "validate": {
            "required": True,
            "minLength": "",
            "maxLength": "",
            "pattern": "^[a-zA-Z .-]+$",
            "custom": "",
            "customPrivate": False
        },
        "conditional": {
            "show": "",
            "when": None,
            "eq": ""
        },
        "type": "textfield",
        "labelPosition": "top",
        "inputFormat": "plain",
        "tags": [],
        "properties": {}
            }
recipient_last_name_field ={
        "autofocus": False,
        "input": True,
        "tableView": True,
        "inputType": "text",
        "inputMask": "",
        "label": "Recipient Last Name",
        "key": "recipientLastName",
        "placeholder": "",
        "prefix": "",
        "suffix": "",
        "multiple": False,
        "defaultValue": "Doe",
        "protected": False,
        "unique": False,
        "persistent": True,
        "hidden": False,
        "clearOnHide": True,
        "spellcheck": True,
        "validate": {
            "required": True,
            "minLength": "",
            "maxLength": "",
            "pattern": "^[a-zA-Z .-]+$",
            "custom": "",
            "customPrivate": False
        },
        "conditional": {
            "show": "",
            "when": None,
            "eq": ""
        },
        "type": "textfield",
        "labelPosition": "top",
        "inputFormat": "plain",
        "tags": [],
        "properties": {}
        }

full_name = {
        "autofocus": False,
        "input": True,
        "tableView": True,
        "inputType": "text",
        "inputMask": "",
        "label": "Full Name",
        "key": "fullName",
        "placeholder": "",
        "prefix": "",
        "suffix": "",
        "multiple": False,
        "defaultValue": "John Doe",
        "protected": False,
        "unique": False,
        "persistent": True,
        "hidden": False,
        "clearOnHide": True,
        "spellcheck": True,
        "validate": {
            "required": True,
            "minLength": "",
            "maxLength": "",
            "pattern": "^[a-zA-Z .-]+$",
            "custom": "",
            "customPrivate": False
        },
        "conditional": {
            "show": "",
            "when": None,
            "eq": ""
        },
        "type": "textfield",
        "labelPosition": "top",
        "inputFormat": "plain",
        "tags": [],
        "properties": {}
            }

recipient_email_component = {
            "autofocus": False,
            "input": True,
            "tableView": True,
            "inputType": "email",
            "label": "Recipient Email",
            "key": "recipientEmail",
            "type": "email",
            "placeholder": "",
            "prefix": "",
            "suffix": "",
            "defaultValue": "example@gmail.com",
            "protected": False,
            "unique": False,
            "persistent": True,
            "hidden": False,
            "clearOnHide": True,
            "kickbox": {
                "enabled": False
            },
            "labelPosition": "top",
            "inputFormat": "plain",
            "tags": [],
            "conditional": {
                "show": "",
                "when": None,
                "eq": ""
            },
            "properties": {},
            "validate": {
                "required": True
            }
        }

email = {
            "autofocus": False,
            "input": True,
            "tableView": True,
            "inputType": "email",
            "label": "Email",
            "key": "email",
            "type": "email",
            "placeholder": "",
            "prefix": "",
            "suffix": "",
            "defaultValue": "example@gmail.com",
            "protected": False,
            "unique": False,
            "persistent": True,
            "hidden": False,
            "clearOnHide": True,
            "kickbox": {
                "enabled": False
            },
            "labelPosition": "top",
            "inputFormat": "plain",
            "tags": [],
            "conditional": {
                "show": "",
                "when": None,
                "eq": ""
            },
            "properties": {},
            "validate": {
                "required": True
            }
        }


recipient_phone_component = {
            "autofocus": False,
            "input": True,
            "tableView": True,
            "inputType": "text",
            "inputMask": "",
            "label": "Recipient Phone",
            "key": "recipientPhone",
            "placeholder": "",
            "prefix": "",
            "suffix": "",
            "multiple": False,
            "defaultValue": "9999999999",
            "protected": False,
            "unique": False,
            "persistent": True,
            "hidden": False,
            "clearOnHide": True,
            "spellcheck": True,
            "validate": {
                "required": False,
                "minLength": "",
                "maxLength": "",
                "pattern": "",
                "custom": "const phoneRegex = /^(\\+\\d{1,2}\\s?)?(\\(?\\d{3}\\)?[\\s.-]?)?\\d{3}[\\s.-]?\\d{4}$/;\n\nif (input.trim() === \"\") {\n  valid = true; \n} else if (!phoneRegex.test(input)) {\n  valid = \"Enter a Valid Phone Number\";\n} else {\n  valid = true;\n}\n",
                "customPrivate": False,
                "customMessage": ""
            },
            "conditional": {
                "show": "",
                "when": None,
                "eq": ""
            },
            "type": "textfield",
            "labelPosition": "top",
            "inputFormat": "plain",
            "tags": [],
            "properties": {}
        }

phone = {
            "autofocus": False,
            "input": True,
            "tableView": True,
            "inputType": "text",
            "inputMask": "",
            "label": "Phone",
            "key": "phone",
            "placeholder": "",
            "prefix": "",
            "suffix": "",
            "multiple": False,
            "defaultValue": "9999999999",
            "protected": False,
            "unique": False,
            "persistent": True,
            "hidden": False,
            "clearOnHide": True,
            "spellcheck": True,
            "validate": {
                "required": False,
                "minLength": "",
                "maxLength": "",
                "pattern": "",
                "custom": "const phoneRegex = /^(\\+\\d{1,2}\\s?)?(\\(?\\d{3}\\)?[\\s.-]?)?\\d{3}[\\s.-]?\\d{4}$/;\n\nif (input.trim() === \"\") {\n  valid = true; \n} else if (!phoneRegex.test(input)) {\n  valid = \"Enter a Valid Phone Number\";\n} else {\n  valid = true;\n}\n",
                "customPrivate": False,
                "customMessage": ""
            },
            "conditional": {
                "show": "",
                "when": None,
                "eq": ""
            },
            "type": "textfield",
            "labelPosition": "top",
            "inputFormat": "plain",
            "tags": [],
            "properties": {}
        }
