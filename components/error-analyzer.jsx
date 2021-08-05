import { useEffect, useState } from "react";

import { Prism } from "@mantine/prism";
import {
  Button,
  Col,
  Container,
  Divider,
  Grid,
  Group,
  LoadingOverlay,
  NumberInput,
  Radio,
  RadioGroup,
  Text,
} from "@mantine/core";

export const ErrorAnalyzer = () => {
  const [typeOfErrorAnalysis, setTypeOfErrorAnalysis] = useState(
    "Adder Error Analysis"
  );
  const [totalBits, setTotalBits] = useState(4);
  const [accurateBits, setAccurateBits] = useState(1);
  const [inAccurateBits, setInAccurateBits] = useState(3);
  const [multiplicandBits, setMultiplicandBits] = useState(4);
  const [multiplierBits, setMultiplierBits] = useState(4);
  const [vCut, setVCut] = useState(3);
  const [hardwareModule, setHardwareModule] = useState("HEAA");
  const [visible, setVisible] = useState(false);
  const [analysisResult, setAnalysisResult] = useState("");

  // Helper useEffect to set constraints for accurate and inaccurate bits
  useEffect(() => {
    setInAccurateBits(totalBits - accurateBits);
  }, [accurateBits]);

  useEffect(() => {
    setAccurateBits(totalBits - inAccurateBits);
  }, [inAccurateBits]);

  useEffect(() => {
    setAccurateBits(totalBits - inAccurateBits);
  }, [totalBits]);

  // On 'Analyse' button click, calls API to get the result of the error analysis
  const handleAnalyseButtonClick = async () => {
    setVisible((v) => !v);

    const payload = {
      type_of_hardware_module: hardwareModule,
      total_bits: totalBits,
      inacc_bits: inAccurateBits,
      multiplicand_bits: multiplicandBits,
      multiplier_bits: multiplierBits,
      v_cut: vCut,
    };

    const response = await fetch(
      `/api/error-analysis/${typeOfErrorAnalysis
        .toLocaleLowerCase()
        .replaceAll(" ", "-")}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      }
    );
    const analysisResult = await response.text();

    setAnalysisResult(analysisResult.trim());
    setVisible((v) => !v);
  };

  // Helper functions to display the correct hardware options
  const asicAdderHardwareOptions = () => (
    <RadioGroup
      variant="vertical"
      label="Type of Hardware Module"
      color="dark"
      required
      style={{ marginTop: 20 }}
      value={hardwareModule}
      onChange={setHardwareModule}
    >
      <Radio value="HEAA">HEAA</Radio>
      <Radio value="HOERAA">HOERAA</Radio>
      <Radio value="HOAANED">HOAANED</Radio>
      <Radio value="M-HERLOA">M-HERLOA</Radio>
    </RadioGroup>
  );

  // Helper functions to display the correct bits NumberInputs fields
  const totalBitsNumberInput = () => (
    <NumberInput
      id="total-bits" // see https://mantine.dev/core/number-input/#server-side-rendering
      value={totalBits}
      onChange={(val) => setTotalBits(val)}
      placeholder="[4, 32]"
      min={4}
      max={32}
      type="number"
      label="Total bits"
      description="From 4 to 32, step is 1"
      required
      style={{ marginTop: 20 }}
    />
  );

  const accurateInaccurateBitsNumberInput = () => (
    <Group grow="true" style={{ marginTop: 10 }}>
      <NumberInput
        id="accurate-bits"
        value={accurateBits}
        onChange={(val) => setAccurateBits(val)}
        min={1}
        max={totalBits - 3}
        type="number"
        label="Accurate bits"
        description="<= total_bits"
        required
      />
      <NumberInput
        id="inaccurate-bits"
        value={inAccurateBits}
        onChange={(val) => setInAccurateBits(val)}
        min={3}
        max={totalBits - 1}
        type="number"
        label="Inaccurate bits"
        description="From 3 to total_bits-1, step is 1"
        required
      />
    </Group>
  );

  return (
    <Container style={{ marginTop: 10 }}>
      <Grid grow="true">
        {/* Options Columns */}
        <Col span={3}>
          <RadioGroup
            variant="vertical"
            label="Type of Error Analysis"
            color="dark"
            required
            onChange={setTypeOfErrorAnalysis}
            value={typeOfErrorAnalysis}
          >
            <Radio value="Adder Error Analysis">Adder Error Analysis</Radio>
            <Radio value="Multiplier Error Analysis">
              Multiplier Error Analysis
            </Radio>
          </RadioGroup>

          {/* Display corresponding hardware options */}
          {typeOfErrorAnalysis == "Adder Error Analysis" &&
            asicAdderHardwareOptions()}

          {typeOfErrorAnalysis == "Multiplier Error Analysis" && (
            <RadioGroup
              variant="vertical"
              label="Type Hardware Module"
              color="dark"
              required
              onChange={setHardwareModule}
              defaultValue="MxN PAAM01 with V-Cut"
              value={hardwareModule}
              style={{ marginTop: 20 }}
            >
              <Radio value="MxN PAAM01 with V-Cut">MxN PAAM01 with V-Cut</Radio>
            </RadioGroup>
          )}

          {/* Display corresponding NumberInput fields*/}
          {typeOfErrorAnalysis == "Adder Error Analysis" &&
            totalBitsNumberInput()}
          {typeOfErrorAnalysis == "Adder Error Analysis" &&
            accurateInaccurateBitsNumberInput()}

          {typeOfErrorAnalysis == "Multiplier Error Analysis" && (
            <Group grow="true" style={{ marginTop: 10 }}>
              <NumberInput
                id="multiplicand-bits"
                value={multiplicandBits}
                onChange={(val) => setMultiplicandBits(val)}
                min={3}
                max={32}
                type="number"
                label="Multiplicand bits (M)"
                description="From 3 to 32, step is 1"
                required
              />
              <NumberInput
                id="multiplier-bits"
                value={multiplierBits}
                onChange={(val) => setMultiplierBits(val)}
                min={3}
                max={32}
                type="number"
                label="Multiplier bits (N)"
                description="From 3 to 32, step is 1"
                required
              />

              <NumberInput
                id="vcut"
                value={vCut}
                onChange={(val) => setVCut(val)}
                min={0}
                max={multiplicandBits}
                type="number"
                label="V-Cut (v)"
                description="0 <= v <= multiplicand_bits"
                required
              />
            </Group>
          )}

          <Button
            color="dark"
            fullWidth
            onClick={handleAnalyseButtonClick}
            style={{ marginTop: 30 }}
          >
            Analyse
          </Button>
        </Col>

        <Divider orientation="vertical" />

        {/* Analysis result column */}
        <Col span={6}>
          <LoadingOverlay visible={visible} loaderProps={{ color: "dark" }} />
          {analysisResult ? (
            <Prism
              language="verilog"
              withLineNumbers
              copyLabel="Copy code to clipboard"
              copiedLabel="Code copied to clipboard"
            >
              {analysisResult}
            </Prism>
          ) : (
            <Text>⬅ Chose options on left and click 'Generate'</Text>
          )}
        </Col>
      </Grid>
    </Container>
  );
};
