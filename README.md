# XML Injection Tool (XMLit)

XMLit is a Python script that processes HTTP request files, converts the request body to XML format, and optionally performs XML External Entity (XXE) injection attacks. It provides a simple and customizable way to modify requests for testing and security assessment purposes.

## Features

- Converts HTTP request bodies to XML format
- Supports XML External Entity (XXE) injection attacks
- Allows customization of XML tag names and injected variables
- Saves modified requests to output files

## Requirements

- Python 3.6+
- Required packages: `argparse`, `xml.etree`

## Usage

1. Clone this repository or download the `xml_injection_tool.py` script.
2. Navigate to the directory containing the script in your terminal.

Run the script with the following command:

```bash
python xml_injection_tool.py -r change_email.req -x simple-xxe -t tag_name -v variable_value -w modified_change_email.req
```

Replace the arguments with appropriate values:

`-r` or `--request`: Input request file.<br/>
`-x` or `--attack_type`: Attack type (simple-xxe for XXE injection).<br/>
`-t` or `--tag_name`: XML tag name for injection.<br/>
`-v` or `--variable`: Variable to be injected.<br/>
`-w` or `--output_file`: Output file to save the modified request.<br/>

> Note: The `-x`, `-t`, and `-v` arguments are required for the simple-xxe attack type.

### Examples

Convert request body to XML format:

```bash
python xml_injection_tool.py -r change_email.req
```

Perform a simple XXE attack with a custom tag name and variable:
```bash
python xml_injection_tool.py -r change_email.req -x simple-xxe -t email -v "xxe_var"
```

Save the modified request to an output file:
```bash
python xml_injection_tool.py -r change_email.req -x simple-xxe -t email -v "xxe_var" -w modified_change_email.req 
```

## License

This project is licensed under the [MIT License](LICENSE).

