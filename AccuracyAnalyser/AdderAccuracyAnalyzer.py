from . import ApproxAdders


def analyze(
    inacc_bits,
    total_bits,
    adder_first_unsigned_number,
    adder_second_unsigned_number,
    type_of_accuracy_analysis_hardware,
):

    accurate_adder_sum = ApproxAdders.accurate_adder(
        adder_first_unsigned_number, adder_second_unsigned_number, total_bits
    )

    inaccurate_adder_sum = getattr(
        ApproxAdders, f"{type_of_accuracy_analysis_hardware}_approx"
    )(adder_first_unsigned_number, adder_second_unsigned_number, total_bits, inacc_bits)

    inaccurate_adder_accuracy = (
        1 - (abs(accurate_adder_sum - inaccurate_adder_sum) / accurate_adder_sum)
    ) * 100

    return (
        accurate_adder_sum,
        inaccurate_adder_sum,
        inaccurate_adder_accuracy,
        type_of_accuracy_analysis_hardware,
    )
