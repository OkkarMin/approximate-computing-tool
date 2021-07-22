from .AdderSumCalc import (
    accurate_sum_calc,
    HEAA_sum_calc,
    HOERAA_sum_calc,
    HOAANED_sum_calc,
    M_HERLOA_sum_calc,
)
import pyverilog.vparser.ast as vast
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator


def generate_verilog_code(
    type_of_hardware_module,
    total_bits,
    inacc_bits,
):
    """Generate verilog code for the FPGA Adder

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

    verilog_code = None

    ### We will have to re-visit this section later
    inp_a = "a"
    inp_b = "b"
    input_clk = "clk"
    output_sum = "sum"

    paramlist = vast.Paramlist(())

    if total_bits > 1:
        a_vec = vast.Ioport(
            vast.Input(
                inp_a,
                vast.Width(vast.IntConst(ascii(total_bits - 1)), vast.IntConst("0")),
            )
        )
        b_vec = vast.Ioport(
            vast.Input(
                inp_b,
                vast.Width(vast.IntConst(ascii(total_bits - 1)), vast.IntConst("0")),
            )
        )
    elif total_bits == 1:
        a_vec = vast.Ioport(vast.Input(inp_a))
        b_vec = vast.Ioport(vast.Input(inp_b))

    clk = vast.Ioport(vast.Input(input_clk))
    sum_vec = vast.Ioport(
        vast.Output(
            output_sum, vast.Width(vast.IntConst(ascii(total_bits)), vast.IntConst("0"))
        ),
        vast.Reg(
            output_sum, vast.Width(vast.IntConst(ascii(total_bits)), vast.IntConst("0"))
        ),
    )
    portlist = vast.Portlist([a_vec, b_vec, clk, sum_vec])

    input_a = inp_a + "_inp"
    input_b = inp_b + "_inp"

    if total_bits > 1:
        reginp1 = vast.Reg(
            input_a,
            vast.Width(vast.IntConst(ascii(total_bits - 1)), vast.IntConst("0")),
        )
        reginp2 = vast.Reg(
            input_b,
            vast.Width(vast.IntConst(ascii(total_bits - 1)), vast.IntConst("0")),
        )
    elif total_bits == 1:
        reginp1 = vast.Reg(input_a)
        reginp2 = vast.Reg(input_b)

    reginp = [reginp1, reginp2]

    Left_a = vast.Lvalue(vast.Identifier(input_a))
    Right_a = vast.Rvalue(vast.Identifier(inp_a))
    inp_a_2_reg = vast.NonblockingSubstitution(Left_a, Right_a)

    Left_b = vast.Lvalue(vast.Identifier(input_b))
    Right_b = vast.Rvalue(vast.Identifier(inp_b))
    inp_b_2_reg = vast.NonblockingSubstitution(Left_b, Right_b)

    inp_2_reg = [inp_a_2_reg, inp_b_2_reg]
    item1 = [
        vast.Always(
            vast.Sens(vast.Identifier(input_clk), type="posedge"), vast.Block(inp_2_reg)
        )
    ]

    if type_of_hardware_module == "Accurate Adder":
        item2 = accurate_sum_calc(total_bits, input_a, input_b, input_clk, output_sum)
    elif type_of_hardware_module == "HEAA":
        item2 = HEAA_sum_calc(
            total_bits, inacc_bits, input_a, input_b, input_clk, output_sum
        )
    elif type_of_hardware_module == "HOERAA":
        item2 = HOERAA_sum_calc(
            total_bits, inacc_bits, input_a, input_b, input_clk, output_sum
        )
    elif type_of_hardware_module == "HOAANED":
        item2 = HOAANED_sum_calc(
            total_bits, inacc_bits, input_a, input_b, input_clk, output_sum
        )
    elif type_of_hardware_module == "M-HERLOA":
        item2 = M_HERLOA_sum_calc(
            total_bits, inacc_bits, input_a, input_b, input_clk, output_sum
        )

    if type_of_hardware_module == "Accurate_Adder":
        file = f"Accurate_Adder_{total_bits}_bits"
    else:
        file = f"{type_of_hardware_module}_{total_bits}_bits_{inacc_bits}_inacc"

    items = reginp + item1 + item2

    ast = vast.ModuleDef(file, paramlist, portlist, items)

    codegen = ASTCodeGenerator()
    verilog_code = codegen.visit(ast)

    return verilog_code
