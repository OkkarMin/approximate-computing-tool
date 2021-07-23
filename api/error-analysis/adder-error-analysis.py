import ast
from http.server import BaseHTTPRequestHandler
from ErrorAnalyser import AdderErrorAnalyzer


def parse_bytes_to_dict(bytes_to_parse):
    """Given a byte string, parse it into a dict."""
    return ast.literal_eval(bytes_to_parse.decode("utf-8"))


def analyse_error(
    type_of_hardware_module,
    total_bits,
    inacc_bits,
):
    """Analyse the error and return a tuple of the error.

    Analyse error rates depending on the parameters given.

    Args:
        type_of_hardware_module (str): The type of hardware module.
        total_bits (int): The total number of bits.
        inacc_bits (int): The number of inaccurate bits.

    Returns:
        tuple: The errors in the tuple (AverageError, MeanAverageError, RootMeanSquareError)
    """
    if type_of_hardware_module == "HEAA":
        return AdderErrorAnalyzer.HEAA(total_bits, inacc_bits)
    elif type_of_hardware_module == "HOERAA":
        return AdderErrorAnalyzer.HOERAA(total_bits, inacc_bits)
    elif type_of_hardware_module == "HOAANED":
        return AdderErrorAnalyzer.HOAANED(total_bits, inacc_bits)
    elif type_of_hardware_module == "M-HERLOA":
        return AdderErrorAnalyzer.M_HERLOA(total_bits, inacc_bits)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Gets the size of data
        content_length = int(self.headers["Content-Length"])

        # Gets the data itself
        req_body_dict = parse_bytes_to_dict(self.rfile.read(content_length))

        # Generate the result
        type_of_hardware_module = req_body_dict["type_of_hardware_module"]
        total_bits = req_body_dict["total_bits"]
        inacc_bits = req_body_dict["inacc_bits"]
        result = analyse_error(
            type_of_hardware_module,
            total_bits,
            inacc_bits,
        )

        # Furnish the response
        average_error, mean_average_error, root_mean_square_error = result
        response = (
            f'{req_body_dict["type_of_hardware_module"]} with total_bits:{total_bits}, inaccurate_bits:{inacc_bits}\n\n'
            f"Average Error: {average_error}\n"
            f"Mean Absolute Error: {mean_average_error}\n"
            f"RootMeanSquareError: {root_mean_square_error}\n"
        )

        # Sends a response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

        return
