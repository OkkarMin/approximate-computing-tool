import { useState } from "react";

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

const demoCode = `import React from 'react';
import { Button } from '@mantine/core';

function Demo() {
  return <Button>Hello</Button>
}`;

export const VerilogCodeGenerator = () => {
  const [visible, setVisible] = useState(false);
  const [result, setResult] = useState();

  return (
    <Container style={{ marginTop: 10 }}>
      <Grid grow="true">
        <Col span={3}>
          <RadioGroup
            variant="vertical"
            label="Type of Verilog Code"
            color="dark"
            required
          >
            <Radio value="1">FPGA Adder</Radio>
            <Radio value="2">ASIC Adder</Radio>
            <Radio value="3">ASIC Multiplier</Radio>
          </RadioGroup>

          <RadioGroup
            variant="vertical"
            label="Type of Hardware Module"
            color="dark"
            required
            style={{ marginTop: 20 }}
          >
            <Radio value="1">HEAA</Radio>
            <Radio value="2">HOERAA</Radio>
            <Radio value="3">HOAANED</Radio>
            <Radio value="4">M-HERLOA</Radio>
          </RadioGroup>

          <NumberInput
            id="total-bits" // see https://mantine.dev/core/number-input/#server-side-rendering
            defaultValue={4}
            placeholder="[4, 32]"
            min={4}
            max={32}
            type="number"
            label="Total bits"
            description="From 4 to 32, step is 1"
            required
            style={{ marginTop: 20 }}
          />

          <Group grow="true" style={{ marginTop: 10 }}>
            <NumberInput
              id="accurate-bits"
              defaultValue={4}
              min={4}
              max={32}
              type="number"
              label="Accurate bits"
              description="From 4 to 32, step is 1"
              required
            />
            <NumberInput
              id="inaccurate-bits"
              defaultValue={4}
              min={4}
              max={32}
              type="number"
              label="Inaccurate bits"
              description="From 4 to 32, step is 1"
              required
            />
          </Group>

          <Button
            color="dark"
            fullWidth
            onClick={() => {
              setTimeout(() => {
                setVisible((v) => !v);
                setResult(true);
              }, 3000);

              setVisible((v) => !v);
            }}
            style={{ marginTop: 30 }}
          >
            Generate
          </Button>
        </Col>

        <Divider orientation="vertical" />

        <Col span={6} style={{ position: "relative" }}>
          <LoadingOverlay visible={visible} loaderProps={{ color: "dark" }} />
          {result ? (
            <Prism
              language="verilog"
              withLineNumbers
              copyLabel="Copy code to clipboard"
              copiedLabel="Code copied to clipboard"
            >
              {demoCode}
            </Prism>
          ) : (
            <Text>⬅ Chose options and click 'Generate'</Text>
          )}
        </Col>
      </Grid>
    </Container>
  );
};
