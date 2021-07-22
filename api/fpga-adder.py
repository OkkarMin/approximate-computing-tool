import ast
from http.server import BaseHTTPRequestHandler
from VerilogCodeGenerators import VerilogFPGAAdder


def parse_bytes_to_dict(bytes_to_parse):
    """Given a byte string, parse it into a dict."""
    return ast.literal_eval(bytes_to_parse.decode("utf-8"))


def generate_verilog_code(
    type_of_hardware_module,
    total_bits,
    inacc_bits,
):
    """Wrapper function to generate verilog code for the ASIC structural adder

    Generate relevant verilog code depending on the parameters given.

    Args:
        type_of_hardware_module (str): The type of hardware module.
        total_bits (int): The total number of bits.
        inacc_bits (int): The number of inaccurate bits that are not used.

    Returns:
        str: Generated verilog code.
    """

    return VerilogFPGAAdder.generate_verilog_code(
        type_of_hardware_module,
        total_bits,
        inacc_bits,
    )


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Gets the size of data
        content_length = int(self.headers["Content-Length"])

        # Gets the data itself
        req_body_dict = parse_bytes_to_dict(self.rfile.read(content_length))

        # Generate the Verilog code
        verilog_code = generate_verilog_code(
            req_body_dict["type_of_hardware_module"],
            req_body_dict["total_bits"],
            req_body_dict["inacc_bits"],
        )

        # Sends a response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(verilog_code.encode())

        return
