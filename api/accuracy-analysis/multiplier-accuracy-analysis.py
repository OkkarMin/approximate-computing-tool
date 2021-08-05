import ast
from http.server import BaseHTTPRequestHandler
from AccuracyAnalyser import MultiplierAccuracyAnalyzer


def parse_bytes_to_dict(bytes_to_parse):
    """Given a byte string, parse it into a dict."""
    return ast.literal_eval(bytes_to_parse.decode("utf-8"))


def analyse_accuracy(
    multiplicand_bits,
    multiplier_bits,
    multiplier_first_unsigned_number,
    multiplier_second_unsigned_number,
    v_cut,
):
    """Analyse the accuracy and return a tuple of the accuracy.

    Analyse accuracy depending on the parameters given.

    Args:
        multiplicand_bits (int): The number of multiplicand bits.
        multiplier_bits (int): The number of multiplier bits.
        multiplier_first_unsigned_number (int) : The first unsigned number to multiply.
        multiplier_second_unsigned_number (int) : The second unsigned number to multiply.
        v_cut (int) : Position of v_cut.

    Returns:
        tuple: The accuracy in the tuple (AverageError, MeanAverageError, RootMeanSquareError)
    """

    return MultiplierAccuracyAnalyzer.analyze(
        multiplicand_bits,
        multiplier_bits,
        multiplier_first_unsigned_number,
        multiplier_second_unsigned_number,
        v_cut,
    )


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Gets the size of data
        content_length = int(self.headers["Content-Length"])

        # Gets the data itself
        req_body_dict = parse_bytes_to_dict(self.rfile.read(content_length))

        # Generate the result
        multiplicand_bits = req_body_dict["multiplicand_bits"]
        multiplier_bits = req_body_dict["multiplier_bits"]
        multiplier_first_unsigned_number = req_body_dict[
            "multiplier_first_unsigned_number"
        ]
        multiplier_second_unsigned_number = req_body_dict[
            "multiplier_second_unsigned_number"
        ]
        v_cut = req_body_dict["v_cut"]

        result = analyse_accuracy(
            multiplicand_bits,
            multiplier_bits,
            multiplier_first_unsigned_number,
            multiplier_second_unsigned_number,
            v_cut,
        )

        # Furnish the response
        (
            accurate_multiplier_product,
            inaccurate_multiplier_product,
            inaccurate_multiplier_accuracy,
        ) = result
        response = (
            f"Accurate Multiplier Product : {accurate_multiplier_product}\n"
            f"PAAM01-Vcut Multiplier Product : {inaccurate_multiplier_product}\n"
            f"PAAM01-Vcut Multiplier Accuracy: {inaccurate_multiplier_accuracy}\n"
        )

        # Sends a response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

        return
