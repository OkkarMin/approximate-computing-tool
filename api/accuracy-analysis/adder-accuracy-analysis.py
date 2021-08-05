import ast
from http.server import BaseHTTPRequestHandler
from AccuracyAnalyser import AdderAccuracyAnalyzer


def parse_bytes_to_dict(bytes_to_parse):
    """Given a byte string, parse it into a dict."""
    return ast.literal_eval(bytes_to_parse.decode("utf-8"))


def analyse_accuracy(
    type_of_hardware_module,
    total_bits,
    inacc_bits,
    adder_first_unsigned_number,
    adder_second_unsigned_number,
):
    """Analyse the accuracy and return a tuple of the accuracy.

    Analyse accuracy depending on the parameters given.

    Args:
        type_of_hardware_module (str): The type of hardware module.
        total_bits (int): The total number of bits.
        inacc_bits (int): The number of inaccurate bits.
        adder_first_unsigned_number (int): The first unsigned number to be added.
        adder_second_unsigned_number (int): The second unsigned number to be added.

    Returns:
        tuple: The accuracy in the tuple (AverageError, MeanAverageError, RootMeanSquareError)
    """

    # Change 'M-HERLOA' to 'M_HERLOA'
    type_of_hardware_module = (
        "M_HERLOA" if type_of_hardware_module == "M-HERLOA" else type_of_hardware_module
    )

    return AdderAccuracyAnalyzer.analyze(
        inacc_bits,
        total_bits,
        adder_first_unsigned_number,
        adder_second_unsigned_number,
        type_of_hardware_module,
    )


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
        adder_first_unsigned_number = req_body_dict["adder_first_unsigned_number"]
        adder_second_unsigned_number = req_body_dict["adder_second_unsigned_number"]
        result = analyse_accuracy(
            type_of_hardware_module,
            total_bits,
            inacc_bits,
            adder_first_unsigned_number,
            adder_second_unsigned_number,
        )

        # Furnish the response
        (
            accurate_adder_sum,
            inaccurate_adder_sum,
            inaccurate_adder_accuracy,
            type_of_accuracy_analysis_hardware,
        ) = result
        response = (
            f"Accurate Adder Sum: {accurate_adder_sum}\n"
            f"{type_of_accuracy_analysis_hardware} Adder Sum : {inaccurate_adder_sum}\n"
            f"{type_of_accuracy_analysis_hardware} Adder Accuracy: {inaccurate_adder_accuracy}\n"
        )

        # Sends a response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

        return
