import json
import os
from pathlib import Path

def load_schema(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def format_ref(ref):
    return ref.split('/')[-1]

def get_schema_type(schema):
    if not schema:
        return 'any'
    if '$ref' in schema:
        return format_ref(schema['$ref'])
    if 'type' in schema:
        t = schema['type']
        if t == 'array':
            items = schema.get('items', {})
            return f"[{get_schema_type(items)}]"
        return t
    return 'object'

def format_parameters(parameters):
    if not parameters:
        return ""
    
    lines = ["#### Parameters", "| Name | In | Type | Required | Description |", "|---|---|---|---|---|"]
    for param in parameters:
        name = param.get('name', '')
        in_ = param.get('in', '')
        schema = param.get('schema', {})
        type_ = get_schema_type(schema)
        required = "Yes" if param.get('required', False) else "No"
        desc = param.get('description', '').replace('\n', ' ')
        lines.append(f"| {name} | {in_} | {type_} | {required} | {desc} |")
    return "\n".join(lines) + "\n"

def format_request_body(request_body):
    if not request_body:
        return ""
    
    content = request_body.get('content', {})
    json_content = content.get('application/json', {})
    schema = json_content.get('schema', {})
    
    if not schema:
        return ""
        
    ref = schema.get('$ref')
    if ref:
        return f"#### Request Body\nType: `{format_ref(ref)}`\n"
    
    return "#### Request Body\n(Inline schema)\n"

def format_responses(responses):
    if not responses:
        return ""
    
    lines = ["#### Responses", "| Code | Description | Schema |", "|---|---|---|"]
    for code, details in responses.items():
        desc = details.get('description', '').replace('\n', ' ')
        content = details.get('content', {})
        json_content = content.get('application/json', {})
        schema = json_content.get('schema', {})
        type_ = get_schema_type(schema)
        lines.append(f"| {code} | {desc} | {type_} |")
    return "\n".join(lines) + "\n"

def generate_markdown(schema, output_file):
    info = schema.get('info', {})
    title = info.get('title', 'API Documentation')
    description = info.get('description', '')
    version = info.get('version', '')
    
    md = [f"# {title}", f"Version: {version}", "", description, "", "## Endpoints"]
    
    paths = schema.get('paths', {})
    
    # Group by tags
    tagged_endpoints = {}
    
    for path, methods in paths.items():
        for method, details in methods.items():
            tags = details.get('tags', ['Uncategorized'])
            for tag in tags:
                if tag not in tagged_endpoints:
                    tagged_endpoints[tag] = []
                tagged_endpoints[tag].append((path, method, details))
                
    for tag in sorted(tagged_endpoints.keys()):
        md.append(f"### {tag}")
        for path, method, details in tagged_endpoints[tag]:
            summary = details.get('summary', f"{method.upper()} {path}")
            desc = details.get('description', '')
            operation_id = details.get('operationId', '')
            
            md.append(f"#### {summary}")
            md.append(f"`{method.upper()} {path}`")
            if desc:
                md.append(f"\n{desc}\n")
            
            md.append(format_parameters(details.get('parameters', [])))
            md.append(format_request_body(details.get('requestBody')))
            md.append(format_responses(details.get('responses', {})))
            md.append("---\n")
            
    # Add Components/Schemas section
    md.append("## Schemas")
    components = schema.get('components', {})
    schemas = components.get('schemas', {})
    
    for name, schema_details in schemas.items():
        md.append(f"### {name}")
        type_ = schema_details.get('type', 'object')
        md.append(f"Type: `{type_}`")
        
        props = schema_details.get('properties', {})
        if props:
            md.append("\n| Property | Type | Description |")
            md.append("|---|---|---|")
            for prop_name, prop_details in props.items():
                prop_type = get_schema_type(prop_details)
                prop_desc = prop_details.get('description', '').replace('\n', ' ')
                md.append(f"| {prop_name} | {prop_type} | {prop_desc} |")
        md.append("\n")

    with open(output_file, 'w') as f:
        f.write("\n".join(md))

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    schema_path = base_dir / "apps" / "control-plane" / "schema.json"
    output_path = base_dir / "API_REFERENCE.md"
    
    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}")
        exit(1)
        
    print(f"Loading schema from {schema_path}...")
    schema = load_schema(schema_path)
    
    print(f"Generating documentation to {output_path}...")
    generate_markdown(schema, output_path)
    print("Done!")
