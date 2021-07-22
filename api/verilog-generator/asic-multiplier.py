import ast
from http.server import BaseHTTPRequestHandler
from VerilogCodeGenerators import VerilogMultiplierCode


def parse_bytes_to_dict(bytes_to_parse):
    """Given a byte string, parse it into a dict."""
    return ast.literal_eval(bytes_to_parse.decode("utf-8"))


def generate_verilog_code(
    type_of_hardware_module,
    multiplicand_bits,
    multiplier_bits,
    v_cut,
):
    """Generate verilog code for the ASIC multiplier

    Generate relevant verilog code depending on the parameters given.

    Args:
        type_of_hardware_module (str): The type of hardware module.
        multiplicand_bits (int): The number of bits of the multiplicand.
        multiplier_bits (int): The number of bits of the multiplier.
        v_cut (int): The value of the cut-off frequency.
            Only required for 'MxN PAAM01 with V-cut'

    Returns:
        str: Generated verilog code.
    """
    strategy = {
        "MxN Accurate Multiplier": VerilogMultiplierCode.accurate_MxN_multiplier(
            multiplicand_bits,
            multiplier_bits,
        ).to_verilog(),
        "MxN Accurate Binary Array Multiplier": VerilogMultiplierCode.accurate_MxN_binary_array_multiplier(
            multiplicand_bits,
            multiplier_bits,
        ).to_verilog(),
        "MxN PAAM01 with V-cut": VerilogMultiplierCode.PAAM01_V_cut_MxN_binary_array_multiplier(
            multiplicand_bits,
            multiplier_bits,
            v_cut,
        ).to_verilog(),
    }

    return strategy[type_of_hardware_module]


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Gets the size of data
        content_length = int(self.headers["Content-Length"])

        # Gets the data itself
        req_body_dict = parse_bytes_to_dict(self.rfile.read(content_length))

        # Generate the Verilog code
        verilog_code = generate_verilog_code(
            req_body_dict["type_of_hardware_module"],
            req_body_dict["multiplicand_bits"],
            req_body_dict["multiplier_bits"],
            # Assumption: payload will always contain v_cut to not raise KeyError
            req_body_dict["v_cut"],
        )

        # Sends a response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(verilog_code.encode())

        return
