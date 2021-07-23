import ast
from http.server import BaseHTTPRequestHandler
from ErrorAnalyser import MultiplierErrorAnalyzer


def parse_bytes_to_dict(bytes_to_parse):
    """Given a byte string, parse it into a dict."""
    return ast.literal_eval(bytes_to_parse.decode("utf-8"))


def analyse_error(
    type_of_hardware_module,
    multiplicand_bits,
    multiplier_bits,
    v_cut,
):
    """Analyse the error and return a tuple of the error.

    Analyse error rates depending on the parameters given.

    Args:
        type_of_hardware_module (str): The type of hardware module.
        total_bits (int): The total number of bits.
        inacc_bits (int): The number of inaccurate bits.

    Returns:
        tuple: The errors in tuple (AverageError, MeanAverageError, RootMeanSquareError)
    """
    if type_of_hardware_module == "MxN PAAM01 with V-Cut":
        return MultiplierErrorAnalyzer.PAAM01_VCut(
            multiplicand_bits,
            multiplier_bits,
            v_cut,
        )


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Gets the size of data
        content_length = int(self.headers["Content-Length"])

        # Gets the data itself
        req_body_dict = parse_bytes_to_dict(self.rfile.read(content_length))

        # Generate the result
        type_of_hardware_module = req_body_dict["type_of_hardware_module"]
        multiplicand_bits = req_body_dict["multiplicand_bits"]
        multiplier_bits = req_body_dict["multiplier_bits"]
        v_cut = req_body_dict["v_cut"]
        result = analyse_error(
            type_of_hardware_module,
            multiplicand_bits,
            multiplier_bits,
            v_cut,
        )

        # Furnish the response
        average_error, mean_average_error, root_mean_square_error = result
        response = (
            f'{req_body_dict["type_of_hardware_module"]} with M:{multiplicand_bits}, N:{multiplier_bits}, v:{v_cut}\n\n'
            f"Average Error: {average_error}\n"
            f"Mean Average Error: {mean_average_error}\n"
            f"RootMeanSquareError: {root_mean_square_error}\n"
        )

        # Sends a response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

        return
