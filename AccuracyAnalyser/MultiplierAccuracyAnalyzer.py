from . import ApproxMultipliers


def analyze(
    multiplicand_bits,
    multiplier_bits,
    multiplier_first_unsigned_number,
    multiplier_second_unsigned_number,
    v_cut,
):
    accurate_multiplier_product = ApproxMultipliers.accurate_array_multiplier(
        multiplier_first_unsigned_number,
        multiplier_second_unsigned_number,
        multiplicand_bits,
        multiplier_bits,
    )

    inaccurate_multiplier_product = ApproxMultipliers.PAAM01(
        multiplier_first_unsigned_number,
        multiplier_second_unsigned_number,
        multiplicand_bits,
        multiplier_bits,
        v_cut,
    )

    inaccurate_multiplier_accuracy = (
        1
        - (
            abs(accurate_multiplier_product - inaccurate_multiplier_product)
            / accurate_multiplier_product
        )
    ) * 100

    return (
        accurate_multiplier_product,
        inaccurate_multiplier_product,
        inaccurate_multiplier_accuracy,
    )
